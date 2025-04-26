# Sequences de la Coupe de France 2023 - gardees pour test & debug

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

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

global_long_speed = 0.5
global_turn_speed = 3.0
global_turn_speed_slow = 1.5
global_debug_action_timeout = 0.5
global_debug_timeout = 2.0
global_T0 = 0.0
global_T = 0.0


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

    # Pneuma
    await actuators_pneuma.reset_valves()
    await actuators_pneuma.start_compressor()

    # Propulsion
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    
    # Lidar
    robot._adversary_detection_enable = False
    await lidar.start()

    # Actionneurs
    await asyncio.sleep(1)
    await actuators_dyna.bras_standby()
    await asyncio.sleep(2)
    await actuators_dyna.ascenseur_up()

    # Placement
    await recalages.recalage()

    await asyncio.sleep(1)
    await actuators_dyna.ascenseur_down()
    await asyncio.sleep(1)
    await actuators_dyna.bras_up()
    await actuators_dyna.soulageur_down()

    # Dummy score
    await robot.setScore(0)
    await robot.gpioSet('keyboard_led', True)

    return True


@robot.sequence
async def action1():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_turn_speed_slow
    global global_debug_action_timeout
    global global_debug_timeout
    global global_T0
    global global_T

    # depose baniere
    await actuators_dyna.ascenseur_down()
    await propulsion.reposition(-0.07, 0.2)
    await robot.setScore(robot.score + 20)
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
    try:
        await propulsion.trajectorySpline(action1_traj1, speed=global_long_speed)
    except:
        await propulsion.pointTo(poses.Act1_traj1_finish, global_turn_speed)
        await propulsion.moveToRetry(poses.Act1_traj1_finish, global_long_speed)
    await actuators_dyna.bras_standby()
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(0, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.11, 0.2)
    await asyncio.sleep(global_debug_action_timeout)

    # verrouillage planches
    await actuators_dyna.soulageur_up()
    await actuators_dyna.bras_prise()
    await asyncio.sleep(0.2)
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
    await propulsion.faceDirection(180, global_turn_speed_slow)
    await asyncio.sleep(0.2)
    await asyncio.sleep(global_debug_action_timeout)
    
    # relacher
    await actuators_dyna.ascenseur_soulage()
    await actuators_dyna.bras_standby()
    await actuators_dyna.soulageur_down()
    await actuators_pneuma.ventouses_ext_on()
    await actuators_pneuma.ventouses_int_on()
    await propulsion.translation(0.1, 0.2)
    await robot.setScore(robot.score + 4)
    await asyncio.sleep(global_debug_action_timeout)
    await actuators_pneuma.ventouses_ext_off()
    await actuators_pneuma.ventouses_int_off()
    await actuators_dyna.ascenseur_down()
    
@robot.sequence
async def action2():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_turn_speed_slow
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
    #await propulsion.trajectorySpline(action2_traj1, speed=global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.moveToRetry(poses.Act2_traj1_wp1, global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.pointTo(poses.Act2_traj1_finish, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.moveToRetry(poses.Act2_traj1_finish, global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)
    await actuators_dyna.ascenseur_down()
    await propulsion.translation(-0.1, 0.1)
    await asyncio.sleep(global_debug_action_timeout)
    await actuators_dyna.bras_prise()
    await actuators_dyna.soulageur_up()
    

    # depose2
    await propulsion.faceDirection(180, global_turn_speed_slow)
    await asyncio.sleep(0.2)
    await propulsion.moveToRetry(poses.Act2_predepose, global_long_speed)
    await asyncio.sleep(global_debug_action_timeout)
    await actuators_dyna.ascenseur_soulage()
    await asyncio.sleep(0.2)
    await actuators_pneuma.ventouses_ext_on()
    await actuators_pneuma.ventouses_int_on()
    await actuators_dyna.bras_standby()
    await actuators_dyna.soulageur_down()

    await propulsion.translation(0.1, 0.2)

    await actuators_pneuma.ventouses_ext_off()
    await actuators_pneuma.ventouses_int_off()
    await actuators_dyna.ascenseur_down()

    await robot.setScore(robot.score + 4)

    await asyncio.sleep(global_debug_action_timeout)


@robot.sequence
async def action3():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_turn_speed_slow
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
    #await propulsion.trajectorySpline(action3_traj1, speed=global_long_speed)
    #await asyncio.sleep(0.2)
    await propulsion.moveToRetry(poses.Act3_traj1_wp1, global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.pointTo(poses.Act3_traj1_finish, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.moveToRetry(poses.Act3_traj1_finish, global_long_speed)
    await asyncio.sleep(0.2)
    
    if robot.side == pos.Side.Yellow:
        await propulsion.faceDirection(90, global_turn_speed)
    elif robot.side == pos.Side.Blue:
        await propulsion.faceDirection(-90, global_turn_speed)

    await asyncio.sleep(0.2)
    await actuators_dyna.ascenseur_down()
    await asyncio.sleep(0.2)
    #await propulsion.translation(-0.1, 0.2)
    await propulsion.reposition(-0.115, 0.2)
    await asyncio.sleep(global_debug_action_timeout)
    await actuators_dyna.ascenseur_down()
    await actuators_dyna.bras_prise()
    await actuators_dyna.soulageur_up()
    await asyncio.sleep(0.2)
    await actuators_dyna.ascenseur_up_high()

    # depose3
    await propulsion.moveToRetry(poses.Act3_predepose, global_long_speed)
    await actuators_dyna.ascenseur_down()
    await asyncio.sleep(1)
    await actuators_dyna.ascenseur_up()
    await asyncio.sleep(2)
    await propulsion.faceDirection(180, 0.8)
    await actuators_dyna.ascenseur_up()
    await asyncio.sleep(0.2)
    await propulsion.reposition(-0.08, 0.2)
    await asyncio.sleep(global_debug_action_timeout)
    await asyncio.sleep(0.2)
    await actuators_pneuma.ventouses_ext_on()
    await actuators_pneuma.ventouses_int_on()
    await actuators_dyna.bras_standby()
    await actuators_dyna.soulageur_down()

    await propulsion.translation(0.1, 0.2)
    await asyncio.sleep(global_debug_action_timeout)

    await actuators_pneuma.ventouses_ext_off()
    await actuators_pneuma.ventouses_int_off()
    await robot.setScore(robot.score + 8)

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
        poses.Act4_traj1_wp3,
        poses.Act4_traj1_finish
    ]

    # deplacement vers la zone d'attente finale
    try:
        await propulsion.trajectorySpline(action4_traj1, speed=global_long_speed)
        await asyncio.sleep(0.2)
    except:
        await propulsion.pointTo(poses.Act4_traj1_finish, global_turn_speed)
        await propulsion.moveToRetry(poses.Act4_traj1_finish, global_long_speed)

    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)

    await actuators_dyna.ascenseur_down()
    await asyncio.sleep(1.5)
    await actuators_dyna.ascenseur_disable()

    print ("******************************************************")
    print ("* Attente finale")
    print ("******************************************************")
    # attente finale
    global_T = time.time()
    while (global_T-global_T0)<92.0:
        await asyncio.sleep(1.0)
        global_T = time.time()

    # deplacement final
    await propulsion.moveToRetry(poses.Act4_final, global_long_speed)
    await robot.setScore(robot.score + 10)
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
    robot._adversary_detection_enable = True

    global_T = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(global_T-global_T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    print ("======================================================")
    print ("= Action1")
    print ("======================================================")
    try:
        await action1()
    except:
        await actuators_dyna.ascenseur_soulage()
        await actuators_pneuma.ventouses_ext_on()
        await actuators_pneuma.ventouses_int_on()
        await propulsion.pointTo(poses.Act1_traj2_finish, global_turn_speed)
        await propulsion.moveToRetry(poses.Act1_traj2_finish, global_long_speed)
        await actuators_pneuma.ventouses_ext_off()
        await actuators_pneuma.ventouses_int_off()
        await actuators_dyna.ascenseur_down()
    await asyncio.sleep(0.5)
    
    print ("======================================================")
    print ("= Action2")
    print ("======================================================")
    try:
        await action2()

        print ("======================================================")
        print ("= Action3")
        print ("======================================================")
        await action3()
    except:
        await actuators_dyna.ascenseur_soulage()
        await actuators_pneuma.ventouses_ext_on()
        await actuators_pneuma.ventouses_int_on()
        await propulsion.pointTo(poses.Act3_predepose, global_turn_speed)
        await propulsion.moveToRetry(poses.Act3_predepose, global_long_speed)
        await actuators_pneuma.ventouses_ext_off()
        await actuators_pneuma.ventouses_int_off()
        await actuators_dyna.ascenseur_down()
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
    await lidar.stop()
    #await actuators_pneuma.reset_valves()

@robot.sequence
async def construction():
    
    global poses
    global test_speed_g
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout
    global global_T0
    global global_T

    await actuators_dyna.soulageur_up()
    await actuators_dyna.bras_prise()
    #TODO : Pompe

    await actuators_pneuma.ecarteur_on()
    await asyncio.sleep(0.4)
    await actuators_pneuma.ventouses_int_on()

    await propulsion.translation(0.05, global_long_speed)
    await actuators_pneuma.ecarteur_off()
    await actuators_pneuma.ventouses_int_off()
    await actuators_dyna.soulageur_down()
    await asyncio.sleep(0.2)

    await propulsion.translation(-0.05, global_long_speed)
    await actuators_dyna.ascenseur_stage2()
    await actuators_pneuma.ventouses_ext_off()
    #TODO : Pompe release

    await propulsion.translation(0.1, global_long_speed)
    await actuators_dyna.bras_standby()
    await actuators_dyna.ascenseur_standby()
