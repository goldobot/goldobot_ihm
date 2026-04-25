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

# BLUE : ZONE 1
class BluePoses:
    # Poses de depart
    #Start_pose = (  0.082,  1.325,   0)
    Start_pose = (  0.320,  1.325,   0)

    # REAL
    First_grab_wp1  = (  0.510,  1.325,   0)
    First_grab_wp2  = (  0.560,  1.325,   0)
    First_grab_wp3  = (  0.610,  1.325,   0)
    First_grab_wp4  = (  0.660,  1.325,   0)

    First_push      = (  0.980,  1.325,   0)
    First_push_out  = (  1.100,  1.325,   0)

    First_return_wp = (  0.200,  1.200,   0)

    Inter_wp0       = (  0.500,  1.075,   0)
    Inter_wp1       = (  1.000,  1.075,   0)
    Inter_wp2       = (  1.720,  1.075,   0)
    Inter_test_wp   = (  1.600,  1.075,   0)

    Corner_wp       = (  1.850,  1.200, -60)

    Border_wp1      = (  1.850,  0.630, -90)
    Border_wp1_N    = (  1.850,  1.500, -90)

    Strat1_grab_wp1 = (  1.600,  1.084,  90)
    Strat1_drop_wp1 = (  1.634,  0.800,   0)

    Strat2_grab_wp1 = (  1.584,  0.400,   0)
    Strat2_drop_wp1 = (  1.441,  0.000,-180)

    Strat3_grab_wp1 = (  1.441,  0.350,-180)
    Strat3_drop_wp1 = (  1.441,  0.700,-180)

    Final_escape_wp = (  0.700,  1.300,-180)
    Final_pose_wp   = (  0.300,  1.300,-180)


# YELLOW : ZONE 2
class YellowPoses:
    # Poses de depart
    Start_pose = symetrie(BluePoses.Start_pose)

    # REAL
    First_grab_wp1  = symetrie(BluePoses.First_grab_wp1)
    First_grab_wp2  = symetrie(BluePoses.First_grab_wp2)
    First_grab_wp3  = symetrie(BluePoses.First_grab_wp3)
    First_grab_wp4  = symetrie(BluePoses.First_grab_wp4)

    First_push      = symetrie(BluePoses.First_push)
    First_push_out  = symetrie(BluePoses.First_push_out)

    First_return_wp = symetrie(BluePoses.First_return_wp)

    Inter_wp0       = symetrie(BluePoses.Inter_wp0)
    Inter_wp1       = symetrie(BluePoses.Inter_wp1)
    Inter_wp2       = symetrie(BluePoses.Inter_wp2)
    Inter_test_wp   = symetrie(BluePoses.Inter_test_wp)

    Corner_wp       = symetrie(BluePoses.Corner_wp)

    #Border_wp1      = symetrie(BluePoses.Border_wp1)
    Border_wp1      = (  1.850, -0.640, -90)
    Border_wp1_N    = symetrie(BluePoses.Border_wp1_N)

    Strat1_grab_wp1 = symetrie(BluePoses.Strat1_grab_wp1)
    Strat1_drop_wp1 = symetrie(BluePoses.Strat1_drop_wp1)

    Strat2_grab_wp1 = symetrie(BluePoses.Strat2_grab_wp1)
    Strat2_drop_wp1 = symetrie(BluePoses.Strat2_drop_wp1)

    Strat3_grab_wp1 = symetrie(BluePoses.Strat3_grab_wp1)
    Strat3_drop_wp1 = symetrie(BluePoses.Strat3_drop_wp1)

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
