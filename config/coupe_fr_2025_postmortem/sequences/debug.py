# import base modules
import asyncio
import numpy as np
import traceback
import time

# import modules from sequence directory
from . import misc
from . import positions as pos
from . import recalages
from . import actuators_pneuma
from . import actuators_lift
from . import actuators_front
from . import actuators_back
from . import robot_config as rc
from . import dynamic as dyn
from . import sequences_old as oldseq

import logging

LOGGER = logging.getLogger(__name__)

poses = None

@robot.sequence
async def debug_test_exception():
    MIAU

@robot.sequence
async def debug_test_print(*args):
    my_val = float(args[0])
    print ("my_val={}".format(my_val))

@robot.sequence
async def debug_propulsion_enable():
    await odrive.clearErrors()
    await asyncio.sleep(0.5)
    await propulsion.clearError()
    await asyncio.sleep(0.5)
    await propulsion.setAccelerationLimits(1,1,10,10)
    await asyncio.sleep(0.5)
    await propulsion.setMotorsEnable(True)
    await asyncio.sleep(0.5)
    await propulsion.setEnable(True)
    await asyncio.sleep(1)
    

@robot.sequence
async def debug_propulsion_disable():
    await propulsion.setMotorsEnable(False)
    await asyncio.sleep(0.5)
    await propulsion.setEnable(False)
    await asyncio.sleep(1)


@robot.sequence
async def debug_translation(*args):
    dist=float(args[0])
    print ("debug_translation : dist={}".format(dist))
    await propulsion.translation(dist, 0.2)
    
@robot.sequence
async def debug_reposition(*args):
    dist=float(args[0])
    print ("debug_reposition : dist={}".format(dist))
    await propulsion.reposition(dist, 0.2)
    
@robot.sequence
async def debug_face_dir_0(*args):
    await propulsion.faceDirection( 0, 2.0)

@robot.sequence
async def debug_face_dir_90(*args):
    await propulsion.faceDirection(90, 2.0)

@robot.sequence
async def debug_face_dir_180(*args):
    await propulsion.faceDirection(180, 2.0)

@robot.sequence
async def debug_face_dir_m90(*args):
    await propulsion.faceDirection(-90, 2.0)


@robot.sequence
async def debug_prep_test_goldo_back():
    # Pneuma
    await actuators_pneuma.reset_valves()
    await actuators_pneuma.start_compressor()
    await asyncio.sleep(1)

    # Propulsion
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await asyncio.sleep(1)
    
    # Actionneurs
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(1)
    await actuators_back.bras_arr_up()
    await actuators_back.soulageur_arr_down()

@robot.sequence
async def debug_prise_goldo_back():
    global poses
    global test_speed_g
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout

    short_timeout = 0.2
    long_timeout = 0.5

    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(short_timeout)
    await actuators_back.bras_arr_up()
    await actuators_back.soulageur_arr_down()

    print ("Pre-prise")
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(long_timeout)
    await actuators_back.ventouses_arr_ext_attrape()
    await asyncio.sleep(short_timeout)
    await actuators_back.ventouses_arr_int_attrape()
    await asyncio.sleep(short_timeout)
    await actuators_back.bras_arr_standby()
    await asyncio.sleep(short_timeout)
    await propulsion.translation(-0.20, 0.15)
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)

@robot.sequence
async def debug_test_construction_goldo_back():
    await debug_prise_goldo_back()
    await oldseq.construction_goldo()


@robot.sequence
async def debug_prep_test_goldo_front():

    # Pneuma
    await actuators_pneuma.reset_valves()
    await actuators_pneuma.start_compressor()

    # Propulsion
    await odrive.clearErrors()
    await asyncio.sleep(0.5)
    await propulsion.clearError()
    await asyncio.sleep(0.5)
    await propulsion.setAccelerationLimits(1,1,10,10)
    await asyncio.sleep(0.5)
    await propulsion.setMotorsEnable(True)
    await asyncio.sleep(0.5)
    await propulsion.setEnable(True)
    await asyncio.sleep(1)
    
    # Actionneurs
    await actuators_front.ascenseur_av_homing()
    await asyncio.sleep(1)
    await actuators_front.ascenseur_av_down()
    await asyncio.sleep(1)


@robot.sequence
async def debug_print_detections():
    detections = lidar.getDetections()
    print ("Lidar Detections:")
    for d in detections:
        print (d)

@robot.sequence
async def debug_print_sensors():
    print("SENSORS:")
    for k in sensors:
        print("  {} : {}".format(k,sensors[k]))

@robot.sequence
async def debug_stop_lidar():
    await lidar.stop()

@robot.sequence
async def debug_start_lidar():
    await lidar.start()


@robot.sequence
async def debug_test_prise_double():
    global poses
    poses = pos.YellowPoses

    short_timeout = 0.1
    long_timeout = 0.4

    long_speed = 0.5
    #turn_speed = 10.0
    turn_speed = 2.0

    ## prise1 AV
    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y
    action1_traj1 = [
        (p0_x, p0_y, 0),
        poses.Act1_traj1_start,
        poses.Act1_traj1_wp1,
        poses.Act1_traj1_finish
    ]
    try:
        await propulsion.trajectorySpline(action1_traj1, speed=long_speed)
    except:
        await oldseq.trajectory_spline_exception()
        await propulsion.pointTo(poses.Act1_traj1_finish, turn_speed)
        await propulsion.moveToRetry(poses.Act1_traj1_finish, long_speed)
    await asyncio.sleep(short_timeout)
    await propulsion.faceDirection(180, turn_speed)
    await asyncio.sleep(short_timeout)
    await actuators_front.prise_av()
    await asyncio.sleep(short_timeout)

    ## prise2 ARR
    await propulsion.pointTo(poses.Act2_traj1_finish, turn_speed, back=True)
    await asyncio.sleep(short_timeout)
    await propulsion.moveToRetry(poses.Act2_traj1_finish, long_speed)
    await asyncio.sleep(short_timeout)
    await propulsion.faceDirection(180, turn_speed)
    await asyncio.sleep(short_timeout)
    await actuators_back.prise_arr()
    await asyncio.sleep(long_timeout)

@robot.sequence
async def debug_prep_test_construction_niv3():
    global poses
    poses = pos.YellowPoses

    short_timeout = 0.1
    long_timeout = 0.4

    long_speed = 0.6
    turn_speed = 2.0

    predepose_1 = (1.5, -0.25, 0)
    await propulsion.pointTo(predepose_1, turn_speed)
    await propulsion.moveToRetry(predepose_1, long_speed)
    await propulsion.faceDirection(180, turn_speed)
    await asyncio.sleep(short_timeout)


@robot.sequence
async def debug_test_construction_niv3():
    global poses
    poses = pos.YellowPoses

    short_timeout = 0.1
    long_timeout = 0.4

    long_speed = 0.5
    turn_speed = 1.5

    await actuators_back.construction_1_etage_arr()
    await asyncio.sleep(long_timeout)

    #await propulsion.faceDirection(0, turn_speed)
    #await asyncio.sleep(short_timeout)
    #await propulsion.translation(0.03, long_speed)
    #await asyncio.sleep(long_timeout)

    #await actuators_front.construction_2_etages_av()
    #await asyncio.sleep(long_timeout)
    #await actuators_front.depose_3_etages_av_avec_predepose()
    #await asyncio.sleep(long_timeout)

    t1 = asyncio.create_task(actuators_front.construction_2_etages_av_avec_predepose())

    await propulsion.faceDirection(0, turn_speed)
    await asyncio.sleep(short_timeout)
    await propulsion.translation(0.03, long_speed)
    await asyncio.sleep(short_timeout)

    await t1

    await actuators_front.depose_3_etages_av()
    await asyncio.sleep(short_timeout)

    await actuators_front.ecarteur_int_av_off()
    await asyncio.sleep(short_timeout)

    await propulsion.translation(-0.1, long_speed)
    await asyncio.sleep(long_timeout)

@robot.sequence
async def debug_test_prise_finale():
    global poses
    poses = pos.YellowPoses

    short_timeout = 0.2
    long_timeout = 0.5

    long_speed = 0.5
    #turn_speed = 10.0
    turn_speed = 2.0

    ## prise3 AV
    await propulsion.pointTo(poses.Act3_preprise, turn_speed)
    await propulsion.moveToRetry(poses.Act3_preprise, long_speed)
    await asyncio.sleep(short_timeout)
    await propulsion.faceDirection(-90, turn_speed)
    await asyncio.sleep(short_timeout)
    await actuators_front.prise_av()
    await asyncio.sleep(short_timeout)
    await propulsion.reposition(-0.2, 0.2)
    await asyncio.sleep(long_timeout)

@robot.sequence
async def debug_prep_test_construction_finale():
    global poses
    poses = pos.YellowPoses

    short_timeout = 0.1
    long_timeout = 0.4

    long_speed = 0.6
    #turn_speed = 20.0
    turn_speed = 2.0

    predepose_finale = (1.35, -0.25, 0)
    await propulsion.pointTo(predepose_finale, turn_speed)
    await propulsion.moveToRetry(predepose_finale, long_speed)
    await propulsion.faceDirection(180, turn_speed)
    await asyncio.sleep(short_timeout)
    #await propulsion.translation(-0.25, long_speed)
    #await asyncio.sleep(short_timeout)

@robot.sequence
async def debug_test_construction_finale():
    global poses
    poses = pos.YellowPoses

    short_timeout = 0.1
    long_timeout = 0.4

    long_speed = 0.5
    #turn_speed = 5.0
    turn_speed = 1.5

    await actuators_back.construction_1_etage_bis_arr()
    await asyncio.sleep(long_timeout)

    #await propulsion.faceDirection(0, turn_speed)
    #await asyncio.sleep(short_timeout)
    #await propulsion.translation(0.03, long_speed)
    #await asyncio.sleep(long_timeout)

    #await actuators_front.construction_2_etages_av()
    #await asyncio.sleep(long_timeout)
    #await actuators_front.depose_3_etages_av_avec_predepose()
    #await asyncio.sleep(long_timeout)

    t1 = asyncio.create_task(actuators_front.construction_2_etages_av_avec_predepose())

    await propulsion.faceDirection(0, turn_speed)
    await asyncio.sleep(short_timeout)
    await propulsion.translation(0.015, long_speed)
    await asyncio.sleep(short_timeout)

    await t1

    await actuators_front.depose_3_etages_av()
    await asyncio.sleep(short_timeout)

    await actuators_front.ecarteur_int_av_off()
    await asyncio.sleep(long_timeout)

@robot.sequence
async def debug_test_construction_dynamique():
    global poses
    poses = pos.YellowPoses

    short_timeout = 0.2
    long_timeout = 0.5

    long_speed = 0.5
    #turn_speed = 5.0
    turn_speed = 1.5

    await propulsion.faceDirection(180, turn_speed)
    await asyncio.sleep(short_timeout)

    misc.init_match_time()

    t1 = asyncio.create_task(actuators_front.construction_2_etages_av_avec_predepose())

    await propulsion.faceDirection(0, turn_speed)
    await asyncio.sleep(long_timeout)

    await t1

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")


@robot.sequence
async def debug_prep_test_niv3_la_totale():
    global poses
    poses = pos.YellowPoses

    short_timeout = 0.2
    long_timeout = 0.5

    # Pneuma
    await actuators_pneuma.reset_valves()
    await actuators_pneuma.start_compressor()
    await asyncio.sleep(1)

    # Propulsion
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,20,20)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await asyncio.sleep(short_timeout)
    await propulsion.setPose([poses.ZoneDA_start_pose[0], poses.ZoneDA_start_pose[1]], 180)
    await asyncio.sleep(short_timeout)
    
    # Actionneurs ARR
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(short_timeout)
    await actuators_back.bras_arr_up()
    await actuators_back.soulageur_arr_down()
    await asyncio.sleep(short_timeout)

    # Actionneurs AV
    await actuators_front.ascenseur_av_homing()
    await asyncio.sleep(short_timeout)
    await actuators_front.ascenseur_av_down()
    await asyncio.sleep(short_timeout)
    await actuators_front.bras_av_up()
    await asyncio.sleep(short_timeout)


@robot.sequence
async def debug_test_niv3_la_totale():
    global poses
    poses = pos.YellowPoses

    short_timeout = 0.1
    long_timeout = 0.4

    long_speed = 1.0
    turn_speed = 5.0

    print ("DEBUG TIMEOUT")
    await asyncio.sleep(10.0)
    print ("GO!")

    #await debug_prep_test_niv3_la_totale()
    #await asyncio.sleep(long_timeout)

    misc.init_match_time()

    await debug_test_prise_double()
    await asyncio.sleep(long_timeout)
    await debug_prep_test_construction_niv3()
    await asyncio.sleep(long_timeout)
    await debug_test_construction_niv3()
    await asyncio.sleep(long_timeout)
    await debug_test_prise_finale()
    await asyncio.sleep(long_timeout)
    await debug_prep_test_construction_finale()
    await asyncio.sleep(long_timeout)
    await debug_test_construction_finale()
    await asyncio.sleep(long_timeout)
    await actuators_back.pump_arr_off()

    await propulsion.pointTo(poses.Act4_traj1_finish, turn_speed)
    await propulsion.moveToRetry(poses.Act4_traj1_finish, long_speed)

    await actuators_back.pump_arr_off()
    await actuators_pneuma.reset_valves()
    await actuators_pneuma.purge()

    await propulsion.faceDirection(0, turn_speed)
    await asyncio.sleep(short_timeout)

    await propulsion.moveToRetry(poses.Act4_final, long_speed)
    await asyncio.sleep(short_timeout)

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

