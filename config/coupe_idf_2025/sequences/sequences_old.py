# import base modules
import asyncio
import numpy as np
import traceback
import time

# import modules from sequence directory
from . import positions as pos
from . import recalages
from . import actuators_pneuma
from . import actuators_back
from . import robot_config as rc
from . import dynamic as dyn
from . import misc
from . import debug

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

global_long_speed = 0.6
global_turn_speed = 3.0
global_turn_speed_slow = 1.5
global_debug_action_timeout = 0.5
global_debug_timeout = 2.0

poses = None

def set_poses(_poses):
    global poses
    poses = _poses

@robot.sequence
async def action1():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_turn_speed_slow
    global global_debug_action_timeout
    global global_debug_timeout

    # depose baniere
    await actuators_back.ascenseur_arr_down()
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

    await actuators_back.bras_arr_standby()
    await actuators_back.ventouses_arr_ext_attrape()
    await actuators_back.ventouses_arr_int_attrape()

    # prise1
    try:
        await propulsion.trajectorySpline(action1_traj1, speed=0.8)
    except:
        await trajectory_spline_exception()
        await propulsion.pointTo(poses.Act1_traj1_finish, 5.0)
        await propulsion.moveToRetry(poses.Act1_traj1_finish, 1.0)
        #print ("DEBUG SLEEP 3600")
        #await asyncio.sleep(3600.0)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(0, global_turn_speed)
    await asyncio.sleep(0.2)
    try:
        await propulsion.translation(-0.13, 0.2)
    except:
        await asyncio.sleep(3)
        await propulsion.translation(-0.13, 0.2)
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_soulage()
    await asyncio.sleep(0.2)
    await asyncio.sleep(global_debug_action_timeout)

    # verrouillage planches
    await actuators_back.soulageur_arr_up()
    await actuators_back.bras_arr_prise_hard()
    await asyncio.sleep(0.2)
    await actuators_back.pump_arr_on()
    await asyncio.sleep(0.2)
    await actuators_back.bras_arr_transport()
    await asyncio.sleep(0.2)
    await actuators_back.soulageur_arr_transport()
    await asyncio.sleep(0.2)
    await asyncio.sleep(global_debug_action_timeout)

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    action1_traj2 = [
        (p0_x, p0_y, 0),
        poses.Act1_traj2_start,
        poses.Act1_traj2_wp1,
        poses.Act1_traj2_finish
    ]

    # prep construction
    try:
        await propulsion.trajectorySpline(action1_traj2, speed=global_long_speed)
    except:
        await trajectory_spline_exception()
        await propulsion.pointTo(poses.Act1_traj2_finish, 5.0)
        await propulsion.moveToRetry(poses.Act1_traj2_finish, 1.0)
        #print ("DEBUG SLEEP 3600")
        #await asyncio.sleep(3600.0)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(180, global_turn_speed_slow)
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.10, 0.15)
    await asyncio.sleep(0.2)
    await asyncio.sleep(global_debug_action_timeout)
    
    # construction
    await construction_goldo()
    await robot.setScore(robot.score + 4)
    await robot.setScore(robot.score + 8)
    
    try:
        await propulsion.translation(0.10, 0.15)
    except:
        await asyncio.sleep(3)
        await propulsion.translation(0.10, 0.15)
    await asyncio.sleep(0.2)

    await asyncio.sleep(global_debug_action_timeout)

@robot.sequence
async def action2():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_turn_speed_slow
    global global_debug_action_timeout
    global global_debug_timeout

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    action2_traj1 = [
        (p0_x, p0_y, 0),
        poses.Act2_traj1_start,
        poses.Act2_traj1_wp1,
        poses.Act2_traj1_finish
    ]

    # prise2
    await actuators_back.ascenseur_arr_down()
    await actuators_back.ventouses_arr_ext_attrape()
    await actuators_back.ventouses_arr_int_attrape()
    await asyncio.sleep(0.2)
    #await propulsion.trajectorySpline(action2_traj1, speed=global_long_speed)
    #await asyncio.sleep(0.2)
    #await propulsion.pointTo(poses.Act2_traj1_wp1, global_turn_speed)
    #await asyncio.sleep(0.2)
    #await propulsion.moveToRetry(poses.Act2_traj1_wp1, global_long_speed)
    #await asyncio.sleep(0.2)
    await propulsion.pointTo(poses.Act2_traj1_finish, 5.0)
    await asyncio.sleep(0.2)
    await propulsion.moveToRetry(poses.Act2_traj1_finish, 0.8)
    await asyncio.sleep(0.2)

    # prep construction
    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.1, 0.1)
    await asyncio.sleep(0.2)
    await actuators_back.bras_arr_prise_hard()
    await asyncio.sleep(0.2)
    await actuators_back.pump_arr_on()
    await asyncio.sleep(0.2)
    await actuators_back.bras_arr_transport()
    await asyncio.sleep(0.2)
    await actuators_back.soulageur_arr_transport()
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.20, 0.15)
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_soulage()
    await asyncio.sleep(0.2)
    
    # construction
    await construction_goldo()
    await robot.setScore(robot.score + 4)
    await robot.setScore(robot.score + 8)
    try:
        await propulsion.translation(0.20, 0.15)
    except:
        await asyncio.sleep(3)
        await propulsion.translation(0.20, 0.15)
    await asyncio.sleep(0.2)
    
    await asyncio.sleep(global_debug_action_timeout)

@robot.sequence
async def action3():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_turn_speed_slow
    global global_debug_action_timeout
    global global_debug_timeout

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    action3_traj1 = [
        (p0_x, p0_y, 0),
        poses.Act3_traj1_start,
        poses.Act3_traj1_wp1,
        poses.Act3_traj1_finish
    ]

    # prise3
    await actuators_back.ventouses_arr_ext_attrape()
    await actuators_back.ventouses_arr_int_attrape()
    await asyncio.sleep(0.2)
    #await propulsion.trajectorySpline(action3_traj1, speed=global_long_speed)
    #await asyncio.sleep(0.2)
    #await propulsion.pointTo(poses.Act3_traj1_wp1, global_turn_speed)
    #await asyncio.sleep(0.2)
    #await propulsion.moveToRetry(poses.Act3_traj1_wp1, global_long_speed)
    #await asyncio.sleep(0.2)
    await propulsion.pointTo(poses.Act3_traj1_finish, 5.0)
    await asyncio.sleep(0.2)
    await propulsion.moveToRetry(poses.Act3_traj1_finish, 0.8)
    await asyncio.sleep(0.2)
    
    if robot.side == pos.Side.Yellow:
        await propulsion.faceDirection(90, global_turn_speed)
    elif robot.side == pos.Side.Blue:
        await propulsion.faceDirection(-90, global_turn_speed)

    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.5)
    #await propulsion.translation(-0.1, 0.2)
    await propulsion.reposition(-0.115, 0.2)
    await asyncio.sleep(global_debug_action_timeout)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    await actuators_back.bras_arr_prise_hard()
    await asyncio.sleep(0.2)
    await actuators_back.pump_arr_on()
    await asyncio.sleep(0.2)
    await actuators_back.bras_arr_transport()
    await asyncio.sleep(0.2)
    await actuators_back.soulageur_arr_transport()
    await asyncio.sleep(0.2)
    await asyncio.sleep(0.5)

    # wooble..
    if robot.side == pos.Side.Yellow:
        await propulsion.faceDirection(95, global_turn_speed)
        await asyncio.sleep(0.2)
        await propulsion.faceDirection(85, global_turn_speed)
        await asyncio.sleep(0.2)
        await propulsion.faceDirection(90, global_turn_speed)
        await asyncio.sleep(0.2)
    elif robot.side == pos.Side.Blue:
        await propulsion.faceDirection(-95, global_turn_speed)
        await asyncio.sleep(0.2)
        await propulsion.faceDirection(-85, global_turn_speed)
        await asyncio.sleep(0.2)
        await propulsion.faceDirection(-90, global_turn_speed)
        await asyncio.sleep(0.2)

    # soulage..
    await actuators_back.ascenseur_arr_soulage()
    await asyncio.sleep(0.2)

    # deplacement vers la zone de construction3
    await propulsion.moveToRetry(poses.Act3_predepose, global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)

    # construction
    await propulsion.translation(-0.10, 0.15)
    await asyncio.sleep(0.2)
    await construction_goldo()
    await robot.setScore(robot.score + 4)
    await robot.setScore(robot.score + 8)
    
    try:
        await propulsion.translation(0.20, 0.15)
    except:
        await asyncio.sleep(3)
        await propulsion.translation(0.20, 0.15)
    await asyncio.sleep(0.2)
    
    await asyncio.sleep(global_debug_action_timeout)

@robot.sequence
async def action4():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    action4_traj1 = [
        (p0_x, p0_y, 0),
        poses.Act4_traj1_start,
        poses.Act4_traj1_wp3,
        poses.Act4_traj1_finish
    ]

    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.5)
    await actuators_back.ascenseur_arr_disable()

    # deplacement vers la zone d'attente finale
    # FIXME : DEBUG : no spline yet..
    #try:
    #    await propulsion.trajectorySpline(action4_traj1, speed=global_long_speed)
    #    await asyncio.sleep(0.2)
    #except:
    #    await propulsion.pointTo(poses.Act4_traj1_finish, global_turn_speed)
    #    await propulsion.moveToRetry(poses.Act4_traj1_finish, global_long_speed)
    await propulsion.pointTo(poses.Act4_traj1_finish, 5.0)
    await propulsion.moveToRetry(poses.Act4_traj1_finish, 1.0)

    await actuators_back.pump_arr_off()
    await actuators_pneuma.reset_valves()
    await actuators_pneuma.purge()

    await propulsion.faceDirection(0, global_turn_speed)
    await asyncio.sleep(0.2)

    print ("******************************************************")
    print ("* Attente finale")
    print ("******************************************************")
    # attente finale
    while misc.match_time()<95.0:
        await asyncio.sleep(1.0)

    # deplacement final
    await propulsion.moveToRetry(poses.Act4_final, global_long_speed)
    await robot.setScore(robot.score + 10)
    await asyncio.sleep(0.2)


@robot.sequence
async def action1_ZoneDL():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_turn_speed_slow
    global global_debug_action_timeout
    global global_debug_timeout

    # depose baniere
    # FIXME : TODO

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    action1_traj1 = [
        (p0_x, p0_y, 0),
        poses.Act1_ZoneDL_traj1_wp1,
        poses.Act1_ZoneDL_traj1_finish
    ]

    # prise1
    try:
        await propulsion.trajectorySpline(action1_traj1, speed=global_long_speed)
    except:
        await trajectory_spline_exception()
        await propulsion.pointTo(poses.Act1_ZoneDL_traj1_finish, global_turn_speed)
        await propulsion.moveToRetry(poses.Act1_ZoneDL_traj1_finish, global_long_speed)
    await actuators_back.bras_arr_standby()
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(0, global_turn_speed)
    await asyncio.sleep(0.2)
    await actuators_back.ventouses_arr_ext_attrape()
    await asyncio.sleep(0.2)
    await actuators_back.ventouses_arr_int_attrape()
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.12, 0.2)
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_soulage()
    await asyncio.sleep(0.2)
    await asyncio.sleep(global_debug_action_timeout)

    # verrouillage planches
    await actuators_back.soulageur_arr_up()
    await actuators_back.bras_arr_prise_hard()
    await asyncio.sleep(0.2)
    await actuators_back.pump_arr_on()
    await asyncio.sleep(0.2)
    await actuators_back.bras_arr_transport()
    await asyncio.sleep(0.2)
    await actuators_back.soulageur_arr_transport()
    await asyncio.sleep(0.2)
    await propulsion.translation(0.12, 0.2)
    await asyncio.sleep(global_debug_action_timeout)

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    action1_traj2 = [
        (p0_x, p0_y, 0),
        poses.Act1_ZoneDL_traj2_start,
        poses.Act1_ZoneDL_traj2_wp1,
        poses.Act1_ZoneDL_traj2_finish
    ]

    # prep construction
    if robot.side == pos.Side.Yellow:
        await propulsion.faceDirection(90, global_turn_speed)
    elif robot.side == pos.Side.Blue:
        await propulsion.faceDirection(-90, global_turn_speed)
    await asyncio.sleep(0.2)
    try:
        await propulsion.trajectorySpline(action1_traj2, speed=global_long_speed)
    except:
        await trajectory_spline_exception()
        await propulsion.pointTo(poses.Act1_ZoneDL_traj2_finish, global_long_speed)
        await propulsion.moveToRetry(poses.Act1_ZoneDL_traj2_finish, global_long_speed)
    await asyncio.sleep(0.2)
    if robot.side == pos.Side.Yellow:
        await propulsion.faceDirection(-90, global_turn_speed)
    elif robot.side == pos.Side.Blue:
        await propulsion.faceDirection(90, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.10, 0.15)
    await asyncio.sleep(0.2)
    await asyncio.sleep(global_debug_action_timeout)
    
    # construction
    await construction_goldo()
    await robot.setScore(robot.score + 4)
    await robot.setScore(robot.score + 8)
    
    await propulsion.translation(0.10, 0.15)
    await asyncio.sleep(0.2)

    await asyncio.sleep(global_debug_action_timeout)


@robot.sequence
async def action2_ZoneDL():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_turn_speed_slow
    global global_debug_action_timeout
    global global_debug_timeout

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    # prise2
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    await actuators_back.ventouses_arr_ext_attrape()
    await asyncio.sleep(0.2)
    await actuators_back.ventouses_arr_int_attrape()
    await asyncio.sleep(0.2)
    await propulsion.pointTo(poses.Act2_ZoneDL_preprise, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.moveToRetry(poses.Act2_ZoneDL_preprise, global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.12, 0.2)
    await asyncio.sleep(0.2)
    await actuators_back.bras_arr_prise_hard()
    await asyncio.sleep(0.2)
    await actuators_back.pump_arr_on()
    await asyncio.sleep(0.2)
    await actuators_back.bras_arr_transport()
    await asyncio.sleep(0.2)
    await actuators_back.soulageur_arr_transport()
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_soulage()
    await asyncio.sleep(0.2)
    await propulsion.translation(0.12, 0.2)
    await asyncio.sleep(0.2)
    await asyncio.sleep(global_debug_action_timeout)

    # deplacement vers la zone de contruction
    await propulsion.pointTo(poses.Act2_ZoneDL_predepose, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.moveToRetry(poses.Act2_ZoneDL_predepose, global_long_speed)
    await asyncio.sleep(0.2)

    # prep construction
    if robot.side == pos.Side.Yellow:
        await propulsion.faceDirection(-90, global_turn_speed)
    elif robot.side == pos.Side.Blue:
        await propulsion.faceDirection(90, global_turn_speed)
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.12, 0.1)
    await asyncio.sleep(0.2)
    
    # construction
    await construction_goldo()
    await robot.setScore(robot.score + 4)
    await robot.setScore(robot.score + 8)
    
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    await propulsion.translation(0.12, 0.15)
    await asyncio.sleep(0.2)
    
    await asyncio.sleep(global_debug_action_timeout)


@robot.sequence
async def action3_ZoneDL():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_turn_speed_slow
    global global_debug_action_timeout
    global global_debug_timeout

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    # prise3
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    await actuators_back.ventouses_arr_ext_attrape()
    await asyncio.sleep(0.2)
    await actuators_back.ventouses_arr_int_attrape()
    await asyncio.sleep(0.2)
    await propulsion.pointTo(poses.Act3_ZoneDL_preprise, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.moveToRetry(poses.Act3_ZoneDL_preprise, global_long_speed)
    await asyncio.sleep(0.2)
    if robot.side == pos.Side.Yellow:
        await propulsion.faceDirection(-90, global_turn_speed)
    elif robot.side == pos.Side.Blue:
        await propulsion.faceDirection(90, global_turn_speed)
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.12, 0.2)
    await asyncio.sleep(0.2)
    await actuators_back.bras_arr_prise_hard()
    await asyncio.sleep(0.2)
    await actuators_back.pump_arr_on()
    await asyncio.sleep(0.2)
    await actuators_back.bras_arr_transport()
    await asyncio.sleep(0.2)
    await actuators_back.soulageur_arr_transport()
    await asyncio.sleep(0.2)

    # wooble..
    if robot.side == pos.Side.Yellow:
        await propulsion.faceDirection(-95, global_turn_speed)
        await asyncio.sleep(0.2)
        await propulsion.faceDirection(-85, global_turn_speed)
        await asyncio.sleep(0.2)
        await propulsion.faceDirection(-90, global_turn_speed)
        await asyncio.sleep(0.2)
    elif robot.side == pos.Side.Blue:
        await propulsion.faceDirection(95, global_turn_speed)
        await asyncio.sleep(0.2)
        await propulsion.faceDirection(85, global_turn_speed)
        await asyncio.sleep(0.2)
        await propulsion.faceDirection(90, global_turn_speed)
        await asyncio.sleep(0.2)

    # soulage..
    await actuators_back.ascenseur_arr_soulage()
    await asyncio.sleep(0.2)
    #await propulsion.translation(0.12, 0.2)
    await propulsion.translation(0.06, 0.2)
    await asyncio.sleep(0.2)
    await asyncio.sleep(global_debug_action_timeout)

    # deplacement vers la zone de contruction (pas necessaire en fait..)
    #await propulsion.pointTo(poses.Act3_ZoneDL_predepose, global_turn_speed)
    #await asyncio.sleep(0.2)
    #await propulsion.moveToRetry(poses.Act3_ZoneDL_predepose, global_long_speed)
    #await asyncio.sleep(0.2)

    # prep construction
    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.18, 0.1)
    await asyncio.sleep(0.2)
    
    # construction
    await construction_goldo()
    await robot.setScore(robot.score + 4)
    await robot.setScore(robot.score + 8)
    
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.2)
    #await propulsion.translation(0.06, 0.15)
    #await asyncio.sleep(0.2)
    
    await asyncio.sleep(global_debug_action_timeout)


@robot.sequence
async def action4_ZoneDL():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    #action4_traj1 = [
    #    (p0_x, p0_y, 0),
    #    poses.Act4_ZoneDL_traj1_start,
    #    poses.Act4_ZoneDL_traj1_wp1,
    #    poses.Act4_ZoneDL_traj1_finish
    #]

    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(0.5)
    await actuators_back.ascenseur_arr_disable()

    # deplacement vers la zone d'attente finale
    # FIXME : DEBUG : no spline yet..
    #try:
    #    await propulsion.trajectorySpline(action4_traj1, speed=global_long_speed)
    #    await asyncio.sleep(0.2)
    #except:
    #    await propulsion.pointTo(poses.Act4_ZoneDL_traj1_finish, global_turn_speed)
    #    await propulsion.moveToRetry(poses.Act4_ZoneDL_traj1_finish, global_long_speed)
    await propulsion.pointTo(poses.Act4_ZoneDL_traj1_wp1, global_turn_speed)
    await propulsion.moveToRetry(poses.Act4_ZoneDL_traj1_wp1, global_long_speed)
    await propulsion.pointTo(poses.Act4_ZoneDL_traj1_finish, global_turn_speed)
    await propulsion.moveToRetry(poses.Act4_ZoneDL_traj1_finish, global_long_speed)

    await actuators_back.pump_arr_off()
    await actuators_pneuma.reset_valves()
    await actuators_pneuma.purge()

    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)

    print ("******************************************************")
    print ("* Attente finale")
    print ("******************************************************")
    # attente finale
    while misc.match_time()<92.0:
        await asyncio.sleep(1.0)

    # deplacement final
    await propulsion.moveToRetry(poses.Act4_ZoneDL_final, global_long_speed)
    await robot.setScore(robot.score + 10)
    await asyncio.sleep(0.2)

@robot.sequence
async def action1_ZoneA():
    global poses
    global global_long_speed
    global global_turn_speed
    global global_turn_speed_slow
    global global_debug_action_timeout
    global global_debug_timeout

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    action1_traj1 = [
        (p0_x, p0_y, 0),
        poses.Act1_ZoneA_traj1_start,
        poses.Act1_ZoneA_traj1_wp1,
        poses.Act1_ZoneA_traj1_finish
    ]

    # prise1
    try:
        await propulsion.trajectorySpline(action1_traj1, speed=global_long_speed)
    except:
        await trajectory_spline_exception()
        await propulsion.pointTo(poses.Act1_ZoneA_traj1_finish, global_turn_speed)
        await propulsion.moveToRetry(poses.Act1_ZoneA_traj1_finish, global_long_speed)
    await actuators_back.bras_arr_standby()
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)
    await actuators_back.ventouses_arr_ext_attrape()
    await asyncio.sleep(0.2)
    await actuators_back.ventouses_arr_int_attrape()
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.12, 0.2)
    await asyncio.sleep(0.2)
    await actuators_back.ascenseur_arr_soulage()
    await asyncio.sleep(0.2)
    await asyncio.sleep(global_debug_action_timeout)

    # verrouillage planches
    await actuators_back.soulageur_arr_up()
    await actuators_back.bras_arr_prise_hard()
    await asyncio.sleep(0.2)
    await actuators_back.pump_arr_on()
    await asyncio.sleep(0.2)
    await actuators_back.bras_arr_transport()
    await asyncio.sleep(0.2)
    await actuators_back.soulageur_arr_transport()
    await asyncio.sleep(0.2)
    # Pas necessaire!..
    #await propulsion.translation(0.12, 0.2)
    #await asyncio.sleep(global_debug_action_timeout)

    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y

    action1_traj2 = [
        (p0_x, p0_y, 0),
        poses.Act1_traj2_start,
        poses.Act1_traj2_wp1,
        poses.Act1_traj2_finish
    ]

    # prep construction
    try:
        await propulsion.trajectorySpline(action1_traj2, speed=global_long_speed)
    except:
        await trajectory_spline_exception()
        await propulsion.pointTo(poses.Act1_traj2_finish, global_turn_speed)
        await propulsion.moveToRetry(poses.Act1_traj2_finish, global_long_speed)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(180, global_turn_speed_slow)
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.10, 0.15)
    await asyncio.sleep(0.2)
    await asyncio.sleep(global_debug_action_timeout)
    
    # construction
    await construction_goldo()
    await robot.setScore(robot.score + 4)
    await robot.setScore(robot.score + 8)
    
    await propulsion.translation(0.10, 0.15)
    await asyncio.sleep(0.2)

    await asyncio.sleep(global_debug_action_timeout)


@robot.sequence
async def match_start_ZoneDA():
    global poses
    global test_speed_g
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout

    stop_actions = False

    if not stop_actions:
        print ("======================================================")
        print ("= Action1")
        print ("======================================================")
        try:
            await action1()
        except Exception as e:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print ("! Action1 FAILED")
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            await actuators_back.ascenseur_arr_soulage()
            await actuators_back.ventouses_arr_ext_lache()
            await actuators_back.ventouses_arr_int_lache()
            stop_actions = True
            traceback.print_exc()
            #print ("DEBUG SLEEP 3600")
            #await asyncio.sleep(3600.0)
        await asyncio.sleep(0.5)
    else:
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print ("! Action1 disabled")
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    if not stop_actions:
        print ("======================================================")
        print ("= Action2")
        print ("======================================================")
        try:
            await action2()
        except:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print ("! Action2 FAILED")
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            await actuators_back.ascenseur_arr_soulage()
            await actuators_back.ventouses_arr_ext_lache()
            await actuators_back.ventouses_arr_int_lache()
            stop_actions = True
        await asyncio.sleep(0.5)
    else:
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print ("! Action2 disabled")
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    #stop_actions = True

    if not stop_actions:
        print ("======================================================")
        print ("= Action3")
        print ("======================================================")
        try:
            await action3()
        except:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print ("! Action3 FAILED")
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            await actuators_back.ascenseur_arr_soulage()
            await actuators_back.ventouses_arr_ext_lache()
            await actuators_back.ventouses_arr_int_lache()
            stop_actions = True
        await asyncio.sleep(0.5)
    else:
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print ("! Action3 disabled")
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print ("======================================================")
    print ("= Action4")
    print ("======================================================")
    await action4()
    await asyncio.sleep(global_debug_timeout)


@robot.sequence
async def match_start_ZoneDL():
    global poses
    global test_speed_g
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout

    stop_actions = False

    await propulsion.faceDirection(180, 5.0)
    await propulsion.moveToRetry(poses.zone_dl_band, 0.6)
    await propulsion.faceDirection(180, 5.0) 
    await propulsion.reposition(-0.3, 0.2)
    await robot.setScore(20)
    await propulsion.reposition(0.3, 0.2)

    if not stop_actions:
        print ("======================================================")
        print ("= Action1 ZoneDL")
        print ("======================================================")
        try:
            await action1_ZoneDL()
        except:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print ("! Action1 ZoneDL FAILED")
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            await actuators_back.ascenseur_arr_soulage()
            await actuators_back.ventouses_arr_ext_lache()
            await actuators_back.ventouses_arr_int_lache()
            stop_actions = True
        await asyncio.sleep(0.5)
    else:
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print ("! Action1 ZoneDL disabled")
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T Action1 ZoneDL DONE : match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    #stop_actions = True

    if not stop_actions:
        print ("======================================================")
        print ("= Action2 ZoneDL")
        print ("======================================================")
        try:
            await action2_ZoneDL()
        except:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print ("! Action2 ZoneDL FAILED")
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            await actuators_back.ascenseur_arr_soulage()
            await actuators_back.ventouses_arr_ext_lache()
            await actuators_back.ventouses_arr_int_lache()
            stop_actions = True
        await asyncio.sleep(0.5)
    else:
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print ("! Action2 ZoneDL disabled")
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T Action2 ZoneDL DONE : match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    #stop_actions = True

    if not stop_actions:
        print ("======================================================")
        print ("= Action3 ZoneDL")
        print ("======================================================")
        try:
            await action3_ZoneDL()
        except:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print ("! Action3 ZoneDL FAILED")
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            await actuators_back.ascenseur_arr_soulage()
            await actuators_back.ventouses_arr_ext_lache()
            await actuators_back.ventouses_arr_int_lache()
            stop_actions = True
        await asyncio.sleep(0.5)
    else:
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print ("! Action3 ZoneDL disabled")
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T Action3 ZoneDL DONE : match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    #stop_actions = True

    print ("======================================================")
    print ("= Action4 ZoneDL")
    print ("======================================================")
    await action4_ZoneDL()
    await asyncio.sleep(global_debug_timeout)


@robot.sequence
async def match_start_ZoneA():
    global poses
    global test_speed_g
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout

    stop_actions = False

    if not stop_actions:
        print ("======================================================")
        print ("= Action1 ZoneA")
        print ("======================================================")
        try:
            await action1_ZoneA()
        except:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print ("! Action1 ZoneA FAILED")
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            await actuators_back.ascenseur_arr_soulage()
            await actuators_back.ventouses_arr_ext_lache()
            await actuators_back.ventouses_arr_int_lache()
            stop_actions = True
        await asyncio.sleep(0.5)
    else:
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print ("! Action1 ZoneA disabled")
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    if not stop_actions:
        print ("======================================================")
        print ("= Action2")
        print ("======================================================")
        try:
            await action2()
        except:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print ("! Action2 FAILED")
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            await actuators_back.ascenseur_arr_soulage()
            await actuators_back.ventouses_arr_ext_lache()
            await actuators_back.ventouses_arr_int_lache()
            stop_actions = True
        await asyncio.sleep(0.5)
    else:
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print ("! Action2 disabled")
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    #stop_actions = True

    if not stop_actions:
        print ("======================================================")
        print ("= Action3")
        print ("======================================================")
        try:
            await action3()
        except:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print ("! Action3 FAILED")
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            await actuators_back.ascenseur_arr_soulage()
            await actuators_back.ventouses_arr_ext_lache()
            await actuators_back.ventouses_arr_int_lache()
            stop_actions = True
        await asyncio.sleep(0.5)
    else:
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print ("! Action3 disabled")
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print ("======================================================")
    print ("= Action4")
    print ("======================================================")
    await action4()
    await asyncio.sleep(global_debug_timeout)


@robot.sequence
async def construction_goldo():
    global poses
    global test_speed_g
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout

    short_timeout = 0.1
    long_timeout = 0.3

    print ("Prise planches")
    await actuators_back.ascenseur_arr_soulage()
    await asyncio.sleep(short_timeout)
    await actuators_back.soulageur_arr_up()
    await asyncio.sleep(short_timeout)
    await actuators_back.pump_arr_on()
    await asyncio.sleep(short_timeout)
    await actuators_back.bras_arr_prise_hard()
    await asyncio.sleep(long_timeout)
    #await actuators_back.bras_arr_up()
    #await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)
    
    print ("Construction niveau 1")
    await actuators_back.ecarteur_arr_on()
    await asyncio.sleep(short_timeout)
    await actuators_back.bras_arr_standby()
    await asyncio.sleep(short_timeout)
    await actuators_back.ventouses_arr_int_lache()
    """
    await asyncio.sleep(short_timeout)
    await actuators_back.ventouses_arr_int_attrape()
    await asyncio.sleep(short_timeout)
    await actuators_back.ventouses_arr_int_lache()
    await asyncio.sleep(short_timeout)
    await actuators_back.ventouses_arr_int_attrape()
    await asyncio.sleep(short_timeout)
    await actuators_back.ventouses_arr_int_lache()
    """
    await asyncio.sleep(short_timeout)
    #await actuators_back.ventouses_arr_int_lache()
    await asyncio.sleep(long_timeout)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(short_timeout)
    await actuators_back.soulageur_arr_down()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)

    print ("Translation")
    await propulsion.translation(0.11, 0.15)
    await asyncio.sleep(short_timeout)
    await actuators_back.ecarteur_arr_off()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)

    print ("Construction niveau 2")
    await actuators_back.soulageur_arr_mid()
    await actuators_back.ascenseur_arr_stage2_high()
    await asyncio.sleep(long_timeout)
    await propulsion.translation(-0.13, 0.15)
    await asyncio.sleep(short_timeout)
    await actuators_back.bras_arr_prise()
    await asyncio.sleep(short_timeout)
    await actuators_back.ascenseur_arr_stage2_depose()
    await asyncio.sleep(short_timeout)
    await actuators_back.pump_arr_off()
    await asyncio.sleep(short_timeout)
    await actuators_back.ventouses_arr_ext_lache()
    await asyncio.sleep(1)
    await actuators_back.bras_arr_standby()

    print ("Fin")
    await propulsion.translation(0.22, 0.15)
    await asyncio.sleep(short_timeout)
    await actuators_back.bras_arr_standby()
    await actuators_back.soulageur_arr_down()
    await asyncio.sleep(short_timeout)
    await actuators_back.ascenseur_arr_standby()
    await asyncio.sleep(short_timeout)


async def trajectory_spline_exception():
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("    propulsion.trajectorySpline() EXCEPTION !")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    traceback.print_exc()
    print("  DISABLE DETECTION")
    await asyncio.sleep(0.2)
    propulsion.adversary_detection_enable = False
    print ("DEBUG SLEEP 1")
    await asyncio.sleep(1.0)
    print("  RESTART..")
    print("  PROPULSION DISABLE/ENABLE (to clear error)")
    await propulsion.setEnable(False)
    await asyncio.sleep(0.2)
    await propulsion.setEnable(True)
    await asyncio.sleep(0.2)
    await propulsion.setMotorsEnable(True)
    await asyncio.sleep(0.2)
    print("  re-clear error")
    await propulsion.clearError()
    await asyncio.sleep(0.2)
    print ("DEBUG SLEEP 1")
    await asyncio.sleep(1.0)
    #print ("DEBUG SLEEP 3600")
    #await asyncio.sleep(3600.0)

