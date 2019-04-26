import yaml
from collections import OrderedDict

robot_config = yaml.load(open('config/petit_robot.yaml'))
dynamixels_positions = OrderedDict()

def load_dynamixels_config():
    global dynamixels_positions
    lines = list(open('config/dynamixels_positions.txt', 'r'))
    dynamixels_positions = OrderedDict()
    for l in lines[1:]:
        cols = l.split(',')
        dynamixels_positions[cols[0]] =  [int(cols[1]), int(cols[2]), int(cols[3])]
    
load_dynamixels_config()

    