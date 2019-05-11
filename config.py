import yaml
from collections import OrderedDict
from parse_sequence import SequenceParser

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

#Full config format:
# Offsets table
# HAL config offset
# robot_config offset
# odometry_config offset
# propulsion_config offset
# arms_config offset
# sequences_config offset

def compile_config():
    pass

    