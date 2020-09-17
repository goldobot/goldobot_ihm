import yaml
from collections import OrderedDict
from parse_sequence import SequenceParser
import messages
import struct

from goldobot_ihm.hal_config import HALConfig

#servos = {s['name']:s['id'] for s in robot_config['servos']}

def align_buffer(buff):
    k = len(buff) % 8
    if k == 0:
        return buff
    else:
        return buff + b'\0' * (8-k)

class RobotConfig:
    def __init__(self, path):
        self.yaml = yaml.load(open(path + '/robot.yaml'),Loader=yaml.FullLoader)
        self.hal_config = HALConfig(yaml.load(open(path + '/hal.yaml'),Loader=yaml.FullLoader))
        self.path = path
        self.servo_nums = {s['name']:s['id'] for s in self.yaml['servos']}
        self.load_dynamixels_config()
        if 'dc_motors' in self.yaml:
            self.dc_motors_indices = {s['name']:s['id'] for s in self.yaml['dc_motors']}
        else:
            self.dc_motors_indices = {}
        if 'sensors' in self.yaml:
            self.sensors_indices = {s['name']:s['id'] for s in self.yaml['sensors']}
        else:
            self.sensors_indices = {}
        if 'gpios' in self.yaml:
            self.gpio_indices = {s['name']:s['id'] for s in self.yaml['gpios']}
        else:
            self.gpio_indices = {}
        self.load_sequences()
        
    def update_config(self):
        self.load_dynamixels_config()
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
        for f in self.yaml['sequence_files']:
            parser.parse_file(self.path + '/' + f)
        self.sequences = parser.compile()
        
    def compile(self):
        #RobotConfig
        robot_config_buffer = struct.pack('<ff',
            self.yaml['geometry']['front_length'],
            self.yaml['geometry']['back_length'])
            
        # hal config
        hal_config_buffer = self.hal_config.compile()
        
        #OdometryConfig
        odometry_config_buffer = messages.OdometryConfig(yaml=self.yaml['odometry']).serialize()
        
        #Propulsion config
        propulsion_config_buffer = messages.PropulsionControllerConfig(yaml=self.yaml['propulsion']).serialize()
        
        tid = {'ax12':2, 'mx28':3}
        #Arm servo configs
        arm_config_buffer = struct.pack('<H', len(self.yaml['dynamixels']))
        for s in self.yaml['dynamixels']:
            servo_buffer = struct.pack('<BBHHH', s['id'], tid[s['type']],0,0,0)
            arm_config_buffer += servo_buffer
        arm_config_buffer += b'\0' * 8 * (16-len(self.yaml['dynamixels']))
        arm_config_buffer += struct.pack('<HH', 32,len(self.dynamixels_torques))
        arm_config_buffer += b'\0' * 8
        
        arm_positions_buffer = b''.join([b''.join([struct.pack('<H', t) for t in s]) for s in self.dynamixels_positions.values()])
        arm_positions_buffer += b'\0' * (len(self.yaml['dynamixels']) * 2 * 64 - len(arm_positions_buffer))
        arm_torques_buffer = b''.join([b''.join([struct.pack('<H', t) for t in s]) for s in self.dynamixels_torques.values()])
        
        #Servo config buffer
        servos_config_buffer = struct.pack('<H', len(self.yaml['servos']))
        for s in self.yaml['servos']:
            servos_config_buffer += struct.pack('<BBHHH', s['id'], 1, s['cw_limit'], s['ccw_limit'], s['max_speed'])
        servos_config_buffer += b'\0' * (8 * (16 - len(self.yaml['servos'])))
        
        #16 uint16 header
        buff = b''
        offset = 32
        
        offset_hal_config = len(buff)
        buff = align_buffer(buff + hal_config_buffer)
        
        offset_robot_config = len(buff)
        buff = align_buffer(buff + robot_config_buffer)
        
        offset_odometry_config = len(buff)
        buff = align_buffer(buff + odometry_config_buffer)
        
        offset_propulsion_config = len(buff)
        buff = align_buffer(buff + propulsion_config_buffer)
        
        offset_arm_config = len(buff)
        buff = align_buffer(buff + arm_config_buffer)
        
        offset_servos_config = len(buff)
        buff = align_buffer(buff + servos_config_buffer)
        
        offset_arm_positions = len(buff)
        buff = align_buffer(buff + arm_positions_buffer)
        
        offset_arm_torques = len(buff)
        buff = align_buffer(buff + arm_torques_buffer)
        
        offset_sequences = len(buff)
        buff += self.sequences.binary        
        
        header = struct.pack('HHHHHHHHHHHHHHHH',
        offset_hal_config + 32,
        offset_robot_config + 32,
        offset_odometry_config + 32,
        offset_propulsion_config + 32,
        offset_arm_config + 32,
        offset_arm_positions + 32,
        offset_servos_config + 32,
        offset_sequences + 32,
        offset_arm_torques + 32,
        0,0,0,0,0,0,0)

        
        # add padding for alignment?
        self.binary = header + buff
        self.crc = compute_crc(self.binary)
        open(self.path+'/robot_config.bin', 'wb').write(self.binary)
        open(self.path+'/robot_config.crc', 'w').write(str(self.crc))
        sn = open(self.path+'/sequence_names.txt','w')
        for s in self.sequences.sequence_names:
            sn.write(s + '\n')
        sn.close()

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

    
