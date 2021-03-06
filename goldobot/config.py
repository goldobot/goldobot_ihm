import yaml
import pathlib
from collections import OrderedDict
from parse_sequence import SequenceParser
from goldobot import messages
import struct

import runpy
import inspect

from .hal_config import HALConfig

from goldobot import pb2
import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()

from google.protobuf.json_format import ParseDict


def align_buffer(buff):
    k = len(buff) % 8
    if k == 0:
        return buff
    else:
        return buff + b'\0' * (8-k)
        
class SequencesRobot(object):
    def __init__(self):
        self._sequences = {}
        self._sequence_names = []

    def sequence(self, func):
        self._sequences[func.__name__] = func
        self._sequence_names.append(func.__name__)
        #print(inspect.getfullargspec(func))
        

class RobotConfig:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.update_config()
        
        
    def update_config(self):
        #load nucleo config protobuf
        self.robot_config = _sym_db.GetSymbol('goldo.robot.RobotConfig')()
        nucleo_config = self.robot_config.nucleo
        self.yaml = yaml.load(open(self.path / 'nucleo.yaml'),Loader=yaml.FullLoader)
        
        ParseDict(yaml.load(open(self.path / 'hal.yaml'),Loader=yaml.FullLoader), self.robot_config, ignore_unknown_fields=True)
        ParseDict(yaml.load(open(self.path / 'nucleo.yaml'),Loader=yaml.FullLoader), self.robot_config, ignore_unknown_fields=True)
        ParseDict(yaml.load(open(self.path / 'robot.yaml'),Loader=yaml.FullLoader), self.robot_config, ignore_unknown_fields=True)
        self.hal_config = HALConfig(nucleo_config.hal)
        self.config_proto = nucleo_config
        
        self.strategy = yaml.load(open(self.path / 'map.yaml'),Loader=yaml.FullLoader)

        robot = SequencesRobot()
        runpy.run_path(self.path / 'sequences.py', {'robot': robot})
        self.robot_config.sequences_names.extend(robot._sequence_names)
        
        sequences_file = _sym_db.GetSymbol('goldo.robot.SequencesFile')()
        sequences_file.path = 'sequences.py'
        sequences_file.body = open(self.path / 'sequences.py').read()
        self.robot_config.sequences_files.extend([sequences_file])
        
        
        self.dc_motors_indices = {}
        self.sensors_indices = {s.name:s.id for s in self.config_proto.sensors}
        self.gpio_indices = {s.name:s.id for s in self.config_proto.hal.gpio}
        self.load_sequences()
        
    def load_dynamixels_config(self):
        lines = list(open(self.path + '/dynamixels_positions.txt', 'r'))
        self.dynamixels_positions = OrderedDict()
        for l in lines[1:]:
            if l.strip() == '':
                continue
            cols = l.split(',')
            self.dynamixels_positions[cols[0]] =  [int(c) for c in cols[1:]]
            
        self.dynamixels_torques = OrderedDict()
        lines = list(open(self.path + '/dynamixels_torques.txt', 'r'))
        for l in lines[1:]:
            if l.strip() == '':
                continue
            cols = l.split(',')
            self.dynamixels_torques[cols[0]] =  [int(c) for c in cols[1:]]
        
    def get_servo_index(self, name):
        return [s['name'] for s in self.yaml['servos']].index(name)
        
    def get_sensor_index(self, name):
        return self.sensors_indices[name]
        
    def get_gpio_index(self, name):
        return self.gpio_indices[name]
        
    def get_dc_motor_index(self, name):
        return self.dc_motors_indices[name]
        
    def get_arm_position_index(self, name):
        return list(self.dynamixels_positions.keys()).index(name)
        
    def load_sequences(self):
        parser = SequenceParser()
        parser.config = self
        #for f in self.yaml['sequence_files']:
        #    parser.parse_file(self.path + '/' + f)
        self.sequences = parser.compile()
        
    def compile(self):
        #RobotConfig
        robot_config_buffer = pb2.serialize(self.config_proto.robot)
        print(robot_config_buffer, len(robot_config_buffer))
        # hal config
        hal_config_buffer = self.hal_config.compile()        
    

        arm_config_buffer = b''
        
        arm_positions_buffer = b''
        arm_positions_buffer = b''
        arm_torques_buffer = b''
        #Servo config buffer
        servos_config_buffer = struct.pack('<H', len(self.config_proto.servos)) + b''.join([pb2.serialize(s) for s in self.config_proto.servos])
        
        self._offsets = []
        self._buffer = b''
        #16 uint16 header
        buff = b''
        offset = 32
        
        self._push_buffer(hal_config_buffer)       
        self._push_buffer(robot_config_buffer)
        self._push_buffer(pb2.serialize(self.config_proto.robot_simulator))
        self._push_buffer(pb2.serialize(self.config_proto.odometry))
        self._push_buffer(pb2.serialize(self.config_proto.propulsion))
        self._push_buffer(arm_config_buffer)
        self._push_buffer(servos_config_buffer)
        self._push_buffer(arm_positions_buffer)
        self._push_buffer(arm_torques_buffer)        
        self._push_buffer(self.sequences.binary)
        print(*(o + 32 for o in self._offsets + [0] * (16 - len(self._offsets))))
        header = struct.pack('HHHHHHHHHHHHHHHH', *(o + 32 for o in self._offsets + [0] * (16 - len(self._offsets))))
        
        # add padding for alignment?
        self.binary = header + self._buffer
        self.crc = compute_crc(self.binary)
        open(self.path / 'robot_config.bin', 'wb').write(self.binary)
        open(self.path / 'robot_config.crc', 'w').write(str(self.crc))
        sn = open(self.path / 'sequence_names.txt','w')
        for s in self.sequences.sequence_names:
            sn.write(s + '\n')
        sn.close()
        
        self.proto = _sym_db.GetSymbol('goldo.nucleo.robot.Config')(data=self.binary, crc=self.crc)
        self.proto.sequence_names.extend(self.sequences.sequence_names)
        
        _i = 0
        for s in self.config_proto.servos:
            self.proto.servo_ids[s.name] = _i
            _i += 1            
        for s in self.config_proto.sensors:
            self.proto.sensor_ids[s.name] = s.id
        self.proto.rplidar_config.CopyFrom(pb2.from_dict('goldo.nucleo.robot.RPLidarConfig', self.yaml['rplidar']))
    
    def _push_buffer(self, buffer):
        self._offsets.append(len(self._buffer))
        self._buffer = align_buffer(self._buffer + buffer)

#Full config format:
# Offsets table
# hal config offset
# robot_config offset
# odometry_config offset
# propulsion_config offset
# arms_config offset
# arms position config offset
# servos config offset
# sequences_config offset
# arms torque offset

def load_config(path):
    global robot_config
    robot_config = RobotConfig(path)
    
def compute_crc(buffer):
    crc = 0
    for b in buffer:
        x = crc >> 8 ^ b;
        x ^= x >> 4;
        crc = ((crc << 8) ^ (x << 12) ^ (x << 5) ^ x) & 0xffff;
    return crc

    
