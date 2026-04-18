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

# robot offset : 82 mm

# TODO : BLUE : ZONE 1
class BluePoses:
    # Poses de depart
    #Start_pose = (  0.082,  1.325,   0)
    Start_pose = (  0.320,  1.325,   0)

    # TEST
    TEST_wp1   = (  0.510,  1.325,   0)
    TEST_wp2   = (  0.560,  1.325,   0)
    TEST_wp3   = (  0.610,  1.325,   0)
    TEST_wp4   = (  0.660,  1.325,   0)
    TEST_wp5   = (  0.980,  1.325,   0)
    TEST_wp6   = (  0.830,  1.325,   0)
    TEST_wp7   = (  1.000,  1.075,  45)
    TEST_wp8   = (  1.700,  1.075,   0)
    TEST_wp9   = (  1.850,  1.200, -60)
    TEST_wp10  = (  1.850,  0.600, -90)
    TEST_wp10_N= (  1.850,  1.500, -90)
    TEST_wp11  = (  0.700,  1.300,-180)
    TEST_wp12  = (  0.300,  1.300,-180)

    # REAL
    First_grab_wp1  = (  0.510,  1.325,   0)
    First_grab_wp2  = (  0.560,  1.325,   0)
    First_grab_wp3  = (  0.610,  1.325,   0)
    First_grab_wp4  = (  0.660,  1.325,   0)

    First_push      = (  0.980,  1.325,   0)
    First_push_out  = (  1.100,  1.325,   0)

    First_return_wp = (  0.200,  1.200,   0)

    Inter_wp1       = (  1.000,  1.075,   0)
    Inter_wp2       = (  1.720,  1.075,   0)

    Corner_wp       = (  1.850,  1.200, -60)

    Border_wp1      = (  1.850,  0.620, -90)
    Border_wp1_N    = (  1.850,  1.500, -90)

    Final_escape_wp = (  0.700,  1.300,-180)
    Final_pose_wp   = (  0.300,  1.300,-180)


# TODO : YELLOW : ZONE 2
class YellowPoses:
    # Poses de depart
    Start_pose = symetrie(BluePoses.Start_pose)

    # TEST
    TEST_wp1   = symetrie(BluePoses.TEST_wp1)
    TEST_wp2   = symetrie(BluePoses.TEST_wp2)
    TEST_wp3   = symetrie(BluePoses.TEST_wp3)
    TEST_wp4   = symetrie(BluePoses.TEST_wp4)
    TEST_wp5   = symetrie(BluePoses.TEST_wp5)
    TEST_wp6   = symetrie(BluePoses.TEST_wp6)
    TEST_wp7   = symetrie(BluePoses.TEST_wp7)
    TEST_wp8   = symetrie(BluePoses.TEST_wp8)
    TEST_wp9   = symetrie(BluePoses.TEST_wp9)
    TEST_wp10  = symetrie(BluePoses.TEST_wp10)
    TEST_wp10_N= symetrie(BluePoses.TEST_wp10_N)
    TEST_wp11  = symetrie(BluePoses.TEST_wp11)
    TEST_wp12  = symetrie(BluePoses.TEST_wp12)

    # REAL
    First_grab_wp1  = symetrie(BluePoses.First_grab_wp1)
    First_grab_wp2  = symetrie(BluePoses.First_grab_wp2)
    First_grab_wp3  = symetrie(BluePoses.First_grab_wp3)
    First_grab_wp4  = symetrie(BluePoses.First_grab_wp4)

    First_push      = symetrie(BluePoses.First_push)
    First_push_out  = symetrie(BluePoses.First_push_out)

    First_return_wp = symetrie(BluePoses.First_return_wp)

    Inter_wp1       = symetrie(BluePoses.Inter_wp1)
    Inter_wp2       = symetrie(BluePoses.Inter_wp2)

    Corner_wp       = symetrie(BluePoses.Corner_wp)

    Border_wp1      = symetrie(BluePoses.Border_wp1)
    Border_wp1_N    = symetrie(BluePoses.Border_wp1_N)

    Final_escape_wp = symetrie(BluePoses.Final_escape_wp)
    Final_pose_wp   = symetrie(BluePoses.Final_pose_wp)


@robot.sequence
async def print_start_zone():
    print("Start zone : " + str(robot.start_zone))

@robot.sequence
async def led_off():
    await robot.gpioSet('keyboard_led', False)

@robot.sequence
async def led_on():
    await robot.gpioSet('keyboard_led', True)
