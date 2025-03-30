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

global_long_speed = 0.5
global_turn_speed = 5.0
global_debug_action_timeout = 2.0
global_debug_timeout = 2.0
global_T0 = 0.0
global_T = 0.0


@robot.sequence
async def prematch():

    global poses

# FIXME : DEBUG : inversion des couleurs : roustine temporaire le temps que Mehdi corrige l'IHM du robot
# FIXME : DEBUG : !!!!!!!!!!!!! CORRIGER !!!!!!!!!!!!!!
# FIXME : DEBUG : !!!!!!!!!!!!! CORRIGER !!!!!!!!!!!!!!
# FIXME : DEBUG : !!!!!!!!!!!!! CORRIGER !!!!!!!!!!!!!!
# FIXME : DEBUG : !!!!!!!!!!!!! CORRIGER !!!!!!!!!!!!!!
# FIXME : DEBUG : !!!!!!!!!!!!! CORRIGER !!!!!!!!!!!!!!
    if robot.side == pos.Side.Yellow:
        poses = pos.BluePoses
    elif robot.side == pos.Side.Blue:
        poses = pos.YellowPoses
    else:
        raise RuntimeError('Side not set')
# FIXME : DEBUG : !!!!!!!!!!!!! CORRIGER !!!!!!!!!!!!!!
# FIXME : DEBUG : !!!!!!!!!!!!! CORRIGER !!!!!!!!!!!!!!
# FIXME : DEBUG : !!!!!!!!!!!!! CORRIGER !!!!!!!!!!!!!!
# FIXME : DEBUG : !!!!!!!!!!!!! CORRIGER !!!!!!!!!!!!!!
# FIXME : DEBUG : !!!!!!!!!!!!! CORRIGER !!!!!!!!!!!!!!

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
# FIXME : DEBUG
    #await actuators.arms_initialize()

    # Placement
    await recalages.recalage()

    # Dummy score
    await robot.setScore(0)
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print ("$ Dummy score 0")
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    await robot.gpioSet('keyboard_led', True)

    return True


@robot.sequence
async def action1():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout
    global global_T0
    global global_T

    # depose baniere
    await propulsion.reposition(-0.1, 0.2)
    await asyncio.sleep(global_debug_action_timeout)

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    action1_traj1 = [
        (p0_x, p0_y, 0),
        poses.Act1_traj1_start,
        poses.Act1_traj1_wp1,
        poses.Act1_traj1_finish
    ]

    # prise1
    await propulsion.trajectorySpline(action1_traj1, speed=global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(0, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.1, 0.2)
    await asyncio.sleep(global_debug_action_timeout)
    await propulsion.translation(0.1, 0.2)
    await asyncio.sleep(global_debug_action_timeout)

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    action1_traj2 = [
        (p0_x, p0_y, 0),
        poses.Act1_traj2_start,
        poses.Act1_traj2_wp1,
        poses.Act1_traj2_finish
    ]

    # depose1
    await propulsion.trajectorySpline(action1_traj2, speed=global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.reposition(-0.1, 0.2)
    await asyncio.sleep(global_debug_action_timeout)
    await propulsion.translation(0.1, 0.2)
    await asyncio.sleep(global_debug_action_timeout)


@robot.sequence
async def action2():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout
    global global_T0
    global global_T

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    action2_traj1 = [
        (p0_x, p0_y, 0),
        poses.Act2_traj1_start,
        poses.Act2_traj1_wp1,
        poses.Act2_traj1_finish
    ]

    # prise2
    await propulsion.trajectorySpline(action2_traj1, speed=global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.1, 0.2)
    await asyncio.sleep(global_debug_action_timeout)

    # depose2
    await propulsion.moveToRetry(poses.Act2_predepose, global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.reposition(-0.1, 0.2)
    await asyncio.sleep(global_debug_action_timeout)
    await propulsion.translation(0.1, 0.2)
    await asyncio.sleep(global_debug_action_timeout)


@robot.sequence
async def action3():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout
    global global_T0
    global global_T

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    action3_traj1 = [
        (p0_x, p0_y, 0),
        poses.Act3_traj1_start,
        poses.Act3_traj1_wp1,
        poses.Act3_traj1_finish
    ]

    # prise3
    await propulsion.trajectorySpline(action3_traj1, speed=global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(90, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.1, 0.2)
    await asyncio.sleep(global_debug_action_timeout)
    await propulsion.translation(0.1, 0.2)
    await asyncio.sleep(global_debug_action_timeout)

    # depose3
    await propulsion.moveToRetry(poses.Act3_predepose, global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.reposition(-0.1, 0.2)
    await asyncio.sleep(global_debug_action_timeout)
    await propulsion.translation(0.1, 0.2)
    await asyncio.sleep(global_debug_action_timeout)

@robot.sequence
async def action4():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout
    global global_T0
    global global_T

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    action4_traj1 = [
        (p0_x, p0_y, 0),
        poses.Act4_traj1_start,
        poses.Act4_traj1_wp1,
        poses.Act4_traj1_wp2,
        poses.Act4_traj1_finish
    ]

    # deplacement vers la zone d'attente finale
    await propulsion.trajectorySpline(action4_traj1, speed=global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)

    print ("******************************************************")
    print ("* Attente finale")
    print ("******************************************************")
    # attente finale
    global_T = time.time()
    while (global_T-global_T0)<87.0:
        await asyncio.sleep(1.0)
        global_T = time.time()

    # deplacement final
    await propulsion.moveToRetry(poses.Act4_final, global_long_speed)
    await asyncio.sleep(0.2)


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

    global_T = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(global_T-global_T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    print ("======================================================")
    print ("= Action1")
    print ("======================================================")
    await action1()
    await asyncio.sleep(global_debug_timeout)

    print ("======================================================")
    print ("= Action2")
    print ("======================================================")
    await action2()
    await asyncio.sleep(10.0)

    print ("======================================================")
    print ("= Action3")
    print ("======================================================")
    await action3()
    await asyncio.sleep(global_debug_timeout)

    print ("======================================================")
    print ("= Action4")
    print ("======================================================")
    await action4()
    await asyncio.sleep(global_debug_timeout)

    global_T = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(global_T-global_T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")


