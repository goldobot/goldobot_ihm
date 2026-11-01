# Sequences principales 2026

# import base modules
import asyncio
import numpy as np

import time

# NOTE : prise_offset_back_robot = 0.305
# NOTE : robot_back_length       = 0.084
# NOTE : prise_offset            = 0.220

# import modules from sequence directory
from . import positions as pos
from . import robot_config as rc
from . import recalages
from . import actuators

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

poses = None

start_long_speed = 0.30
start_turn_speed = 2.0

global_long_speed = 0.55
#global_long_speed = 0.25
global_turn_speed = 2.8

global_short_sleep = 0.2
global_long_sleep  = 2.0

global_danger_threshold = 0.5

global_field_monitor = None
global_field_monitor_task = None

@robot.sequence
async def prematch():
    global poses
    global start_long_speed
    global start_turn_speed
    global global_long_speed
    global global_turn_speed
    global global_field_monitor
    global global_field_monitor_task

    if robot.side == 1: # YELLOW
        poses = pos.YellowPoses
    elif robot.side == 2: # BLUE
        poses = pos.BluePoses
    else:
        raise RuntimeError('Side not set')

    # Propulsion
    robot._adversary_detection_enable = False
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    
    # Actionneurs
    await actuators.arms_initialize()
    await asyncio.sleep(1.0)

    await actuators.arms_close()
    await asyncio.sleep(0.5)

    # Placement
    await recalages.recalage()
    await asyncio.sleep(0.5)

    # Dummy score
    await robot.setScore(42)
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print ("$ Dummy score 42")
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    await robot.gpioSet('keyboard_led', True)

    await propulsion.setAccelerationLimits(1,1,20,20)


    return True


@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """

    global poses
    global start_long_speed
    global start_turn_speed
    global global_long_speed
    global global_turn_speed
    global global_field_monitor
    global global_field_monitor_task

    T0 = time.time()

    await propulsion.setAccelerationLimits(1,1,20,20)

    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    #robot._adversary_detection_enable = True
    #await lidar.start()

    try:
        await action_0()
        await asyncio.sleep(0.1)
    except:
        print ("EXCEPTION!")
        await escape_procedure(poses.Final_escape_wp0)
        await asyncio.sleep(0.1)

    # FIXME : TODO

    await lidar.stop()

    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")


@robot.sequence
async def action_0():
    global poses
    global start_long_speed
    global start_turn_speed
    global global_long_speed
    global global_turn_speed

    print()
    print("=======")
    print("ACTION0")
    print("=======")
    print()

    #await actuators.arm_right_left_prep_take()
    await asyncio.sleep(0.5)

    await propulsion.pointTo(poses.Action0_traj0_wp1, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y
    Action0_traj0 = [
        (p0_x, p0_y, 0),
        poses.Action0_traj0_wp1,
        poses.Action0_traj0_wp2,
        poses.Action0_traj0_wp3
    ]
    await propulsion.trajectorySpline(Action0_traj0, speed=global_long_speed)
    await asyncio.sleep(0.1)

    await propulsion.faceDirection(poses.Start_pose[2], 1)
    await asyncio.sleep(0.1)

    # FIXME : TODO
    await asyncio.sleep(60.0)


#=================================================================================
# FIXME : TODO : put these in utility.py or something like that...

def compute_dist(p0, p1):
    delta_x = p1[0] - p0[0]
    delta_y = p1[1] - p0[1]
    return np.sqrt(delta_x*delta_x + delta_y*delta_y)

def is_danger():
    global global_danger_threshold
    detections = lidar.getDetections()
    if (len(detections)>0):
        first_det = detections[0]
        print ("Lidar detections : ")
        print (first_det)
        p0 = (propulsion.pose.position.x, propulsion.pose.position.y)
        p1 = (first_det.x, first_det.y)
        dist = compute_dist(p0, p1)
        if (dist<global_danger_threshold):
            return True
    return False

@robot.sequence
async def reset_and_reenable_propulsion():
    await propulsion.setEnable(False)
    await asyncio.sleep(0.2)
    await propulsion.setEnable(True)
    await asyncio.sleep(0.2)
    await propulsion.setMotorsEnable(True)
    await asyncio.sleep(0.2)
    await propulsion.clearError()
    await asyncio.sleep(0.2)

@robot.sequence
async def escape_procedure(escape_point):
    await actuators.pumps_off()
    await asyncio.sleep(0.1)
    await actuators.arms_close()
    await asyncio.sleep(0.1)
    for i in range (0,5):
        if (is_danger()):
            print ("DANGER!")
            await asyncio.sleep(1.0)
        else:
            await reset_and_reenable_propulsion()
            return
    # adversary refuses to go away.. try to go to the escape_point..
    await propulsion.pointTo(escape_point, global_long_speed)
    await asyncio.sleep(0.1)
    await propulsion.moveToRetry(escape_point, global_long_speed)
    await asyncio.sleep(0.1)





