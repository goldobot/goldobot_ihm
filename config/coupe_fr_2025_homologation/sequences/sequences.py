# import base modules
import asyncio
import numpy as np

import time

# import modules from sequence directory
from . import positions as pos
from . import recalages
from . import actuators_pneuma
from . import actuators_dyna
from . import robot_config as rc
from . import dynamic as dyn

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

global_long_speed = 0.6
global_turn_speed = 3.0
global_turn_speed_slow = 1.5
global_debug_action_timeout = 0.5
global_debug_timeout = 2.0
global_T0 = 0.0
global_T = 0.0


@robot.sequence
async def print_sensors():
    print("SENSORS:")
    for k in sensors:
        print("  {} : {}".format(k,sensors[k]))

@robot.sequence
async def prematch():

    global poses

    if robot.side == pos.Side.Yellow:
        poses = pos.YellowPoses
    elif robot.side == pos.Side.Blue:
        poses = pos.BluePoses
    else:
        raise RuntimeError('Side not set')
    
    await lidar.stop()

    # Propulsion
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    
    # Lidar
    propulsion.adversary_detection_enable = False
    await lidar.start()

    # Placement
    await recalages.recalage()

    # Dummy score
    await robot.setScore(0)
    await robot.gpioSet('keyboard_led', True)

    return True

@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """
    global poses
    global test_speed_g
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout
    global global_T0
    global global_T

    global_T0 = time.time()

    await propulsion.setAccelerationLimits(1,1,20,20)
    propulsion.adversary_detection_enable = True

    global_T = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(global_T-global_T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    await propulsion.reposition(-0.1, 0.4)
    for i in range(10):
        try:
            await propulsion.translation(0.20, 0.4)
            break
        except:
            asyncio.sleep(1)

    await robot.setScore(20)

    await propulsion.pointTo(poses.Act4_traj1_finish, 6)
    await propulsion.moveToRetry(poses.Act4_traj1_finish, 0.4)
    await asyncio.sleep(0.5)
    await propulsion.moveToRetry(poses.ZoneDA_start_pose, 0.4)
    await asyncio.sleep(0.5)
    await propulsion.moveToRetry(poses.Act4_traj1_finish, 0.4)
    global_T = time.time()
    while (global_T - global_T0) < 95:
        global_T = time.time()
        await asyncio.sleep(1)
    await propulsion.moveToRetry(poses.Act4_final, 0.4)
    
    await robot.setScore(robot.score + 10)

    global_T = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(global_T-global_T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    await lidar.stop()

@robot.sequence
async def get_detections():
    detections = lidar.getDetections()
    print ("Lidar Detections:")
    for d in detections:
        print (d)

