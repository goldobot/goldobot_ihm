import numpy as np
#from . import robot_config as rc

def symetrie(pose):
    if isinstance(pose, np.ndarray):
        if pose.shape[0] == 2:
            return np.array([pose[0], -pose[1]])
    return (pose[0], -pose[1], -pose[2])


class Side:
    Unknown = 0
    Green = 1
    Blue = 2


# robot offset : 82 mm

# BLUE : ZONE 1
class BluePoses:
    # Poses de depart
    Start_pose        = (  1.000,  1.200,  -90)

    # TEST PROTO
    Action0_traj0_wp1 = (  1.000,  1.000,  -90)
    Action0_traj0_wp2 = (  1.500,  0.500,  -90)
    Action0_traj0_wp3 = (  1.500,  0.300,  -90)

    Final_escape_wp0  = (  1.000,  1.000,   90)
    Final_escape_wp1  = (  1.000,  1.200,   90)
    Final_pose_wp     = (  1.000,  1.200,   90)


# YELLOW : ZONE 2
class YellowPoses:
    # Poses de depart
    Start_pose        = symetrie(BluePoses.Start_pose)

    # REAL
    Action0_traj0_wp1 = symetrie(BluePoses.Action0_traj0_wp1)
    Action0_traj0_wp2 = symetrie(BluePoses.Action0_traj0_wp2)
    Action0_traj0_wp3 = symetrie(BluePoses.Action0_traj0_wp3)

    Final_escape_wp0  = symetrie(BluePoses.Final_escape_wp0)
    Final_escape_wp1  = symetrie(BluePoses.Final_escape_wp1)
    Final_pose_wp     = symetrie(BluePoses.Final_pose_wp)


@robot.sequence
async def print_start_zone():
    print("Start zone : " + str(robot.start_zone))

@robot.sequence
async def led_off():
    await robot.gpioSet('keyboard_led', False)

@robot.sequence
async def led_on():
    await robot.gpioSet('keyboard_led', True)
