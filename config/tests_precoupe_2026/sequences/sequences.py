# Sequences de la Coupe de France 2023 - gardees pour test & debug

# import base modules
import asyncio
import numpy as np

import time

# import modules from sequence directory
from . import positions as pos
from . import recalages
from . import actuators
from . import robot_config as rc

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

global_long_speed = 0.4
global_turn_speed = 2.0

@robot.sequence
async def prematch():

    global poses

    if robot.side == 1: # YELLOW
        poses = pos.YellowPoses
    elif robot.side == 2: # BLUE
        poses = pos.BluePoses
    else:
        raise RuntimeError('Side not set')

    # Propulsion
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    
    # Lidar
    robot._adversary_detection_enable = False
# FIXME : DEBUG
    #await lidar.start()

    # Actionneurs
    await actuators.arms_initialize()

    await asyncio.sleep(5.0)

    # Placement
# FIXME : DEBUG
    await recalages.recalage()

    # Dummy score
    await robot.setScore(42)
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print ("$ Dummy score 42")
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    await robot.gpioSet('keyboard_led', True)

    return True


@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """

    T0 = time.time()

    await propulsion.setAccelerationLimits(1,1,20,20)

    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    # FIXME : TODO
    await propulsion.moveTo(poses.TEST_wp1, global_long_speed)
    await asyncio.sleep(4.0)
    await propulsion.moveTo(poses.TEST_wp2, global_long_speed)
    await asyncio.sleep(4.0)
    await propulsion.moveTo(poses.TEST_wp3, global_long_speed)
    await asyncio.sleep(4.0)
    await propulsion.moveTo(poses.TEST_wp4, global_long_speed)
    await asyncio.sleep(4.0)

    await propulsion.moveTo(poses.TEST_wp5, global_long_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp6, global_long_speed)
    await asyncio.sleep(1.0)

    await propulsion.pointTo(poses.TEST_wp7, global_turn_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp7, global_long_speed)
    await asyncio.sleep(1.0)

    await propulsion.pointTo(poses.TEST_wp8, global_turn_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp8, global_long_speed)
    await asyncio.sleep(1.0)

    await propulsion.pointTo(poses.TEST_wp9, global_turn_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp9, global_long_speed)
    await asyncio.sleep(1.0)

    await propulsion.pointTo(poses.TEST_wp10_N, global_turn_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp10, global_long_speed)
    await asyncio.sleep(10.0)

    await propulsion.pointTo(poses.TEST_wp11, global_turn_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp11, global_long_speed)
    await asyncio.sleep(1.0)

    await propulsion.pointTo(poses.TEST_wp12, global_turn_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp12, global_long_speed)
    await asyncio.sleep(1.0)

    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")


