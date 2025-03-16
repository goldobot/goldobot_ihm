import numpy as np
from . import robot_config as rc

def symetrie(pose):
    if isinstance(pose, np.ndarray):
        if pose.shape[0] == 2:
            return np.array([pose[0], -pose[1]])
    return (pose[0], -pose[1], -pose[2])


class Side:
    Unknown = 0
    Green = 1
    Blue = 2


class GreenPoses:
    zone1_start_pose = (1.20,  1.20, -90)
    zone2_start_pose = (1.70, -0.35, 180)
    zone3_start_pose = (0.30, -1.05,   0)


class BluePoses:
    zone1_start_pose = (1.20, -1.20,  90)
    zone2_start_pose = (1.70,  0.35, 180)
    zone3_start_pose = (0.30,  1.05,   0)

@robot.sequence
async def print_start_zone():
    print("Start zone : " + str(robot.start_zone))

@robot.sequence
async def led_off():
    await robot.gpioSet('keyboard_led', False)

@robot.sequence
async def led_on():
    await robot.gpioSet('keyboard_led', True)
