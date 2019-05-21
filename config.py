import yaml
from collections import OrderedDict
from parse_sequence import SequenceParser
import messages
import struct

robot_config = yaml.load(open('config/petit_robot.yaml'))
dynamixels_positions = OrderedDict()

servos = {s['name']:s['id'] for s in robot_config['servos']}

def load_dynamixels_config():
    global dynamixels_positions
    lines = list(open('config/dynamixels_positions.txt', 'r'))
    dynamixels_positions = OrderedDict()
    for l in lines[1:]:
        cols = l.split(',')
        dynamixels_positions[cols[0]] =  [int(cols[1]), int(cols[2]), int(cols[3])]
        
def load_sequence():
    global compiled_sequences
    parser = SequenceParser()
    parser.parse_file('constants.txt')
    parser.parse_file('sequence.txt')
    compiled_sequences = parser.compile()
    
load_dynamixels_config()

def align_buffer(buff):
    k = len(buff) % 8
    if k == 0:
        return buff
    else:
        return buff + b'\0' * (8-k)

class RobotConfig:
    def __init__(self, path):
        self.yaml = yaml.load(open(path + '/robot.yaml'))
        self.path = path
        
    def load_dynamixels_config(self):
        lines = list(open(self.path + '/dynamixels_positions.txt', 'r'))
        self.dynamixels_positions = OrderedDict()
        for l in lines[1:]:
            cols = l.split(',')
            self.dynamixels_positions[cols[0]] =  [int(cols[1]), int(cols[2]), int(cols[3])]
        
    def compile(self):
        #RobotConfig
        robot_config_buffer = struct.pack('<ff',
            self.yaml['geometry']['front_length'],
            self.yaml['geometry']['back_length'])        
        
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
        arm_config_buffer += struct.pack('<HH', 32,8)
        arm_config_buffer += b'\0' * 8
        
        #Servo config buffer
        servos_config_buffer = struct.pack('<H', len(self.yaml['servos']))
        for s in self.yaml['servos']:
            servos_config_buffer += struct.pack('<BBHHH', s['id'], 1, 0, 0, s['max_speed'])
        servos_config += b'\0' * (8 * (16 - len(self.yaml['servos'])))
        
        #16 uint16 header
        buff = b''
        offset = 32
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
        
        
        header = struct.pack('HHHHHHHHHHHHHHHH',
        offset_robot_config + 32,
        offset_odometry_config + 32,
        offset_propulsion_config + 32,
        offset_arm_config + 32,
        offset_arm_positions + 32,
        offset_servos_config + 32,
        0,
        0,
        0,0,0,0,0,0,0,0)

        
        # add padding for alignment?
        self.binary = header + buff
        

#Full config format:
# Offsets table
# HAL config offset
# robot_config offset
# odometry_config offset
# propulsion_config offset
# arms_config offset
# sequences_config offset

def compile_config_binary():
    pass

    