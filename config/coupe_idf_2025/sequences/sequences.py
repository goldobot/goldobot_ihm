# import base modules
import asyncio
import numpy as np
import traceback
import time

# import modules from sequence directory
from . import positions as pos
from . import robot_config as rc
from . import recalages
from . import actuators_pneuma
from . import actuators_lift
from . import actuators_front
from . import actuators_back
from . import dynamic as dyn
from . import sequences_old as oldseq
from . import misc
from . import debug

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

global_long_speed = 0.6
global_turn_speed = 3.0
global_turn_speed_slow = 1.5
global_debug_action_timeout = 0.5
global_debug_timeout = 2.0

global_prise1_avail = True
global_prise2_avail = True

poses = None


@robot.sequence
async def prematch():

    global poses

    if robot.side == pos.Side.Yellow:
        poses = pos.YellowPoses
    elif robot.side == pos.Side.Blue:
        poses = pos.BluePoses
    else:
        raise RuntimeError('Side not set')
    oldseq.set_poses(poses)
    
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
    #robot._adversary_detection_enable = False
    propulsion.adversary_detection_enable = False
    await lidar.start()

    # Actionneurs ARR
    await asyncio.sleep(1)
    await actuators_back.bras_arr_standby()
    await asyncio.sleep(2)
    await actuators_back.ascenseur_arr_up()

    # Placement
    await recalages.recalage()

    await asyncio.sleep(1)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(1)
    await actuators_back.bras_arr_up()
    await actuators_back.soulageur_arr_down()

    # Actionneurs AV
    await actuators_front.ascenseur_av_homing()
    await asyncio.sleep(0.1)
    # securite!
    await actuators_front.ecarteur_int_av_off()
    await asyncio.sleep(0.1)
    await actuators_front.ascenseur_av_down()
    await asyncio.sleep(0.1)
    await actuators_front.bras_av_up()
    await asyncio.sleep(0.1)

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

    misc.init_match_time()

    await propulsion.setAccelerationLimits(1,1,20,20)
    #propulsion.adversary_detection_enable = True

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    # "OLD STATIC" STRATEGY
    #if   (robot.start_zone == 1) or (robot.start_zone == 6):
    #   await oldseq.match_start_ZoneDA()
    #elif (robot.start_zone == 2) or (robot.start_zone == 5):
    #   await oldseq.match_start_ZoneDL()
    #elif (robot.start_zone == 3) or (robot.start_zone == 4):
    #   await oldseq.match_start_ZoneA()

    # "DYNAMIC" STRATEGY
    # await dyn.dyn_strat()
    # await asyncio.sleep(1.0)
    # await dyn.dyn_action4()

    # "NEW NIV3" STRATEGY
    scan_task = asyncio.create_task(experimental_scan_playfield())
    await experimental_niv3_la_totale()

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    await lidar.stop()

@robot.sequence
async def experimental_init_time():
    misc.init_match_time()

@robot.sequence
async def experimental_scan_playfield():
    global poses
    global global_prise2_avail

    while misc.match_time()<95.0:
        prise_3 = poses.Act3_preprise

        detections = lidar.getDetections()
        if (len(detections)>0):
            first_det = detections[0]
            p0 = (-1, first_det.x, first_det.y)
            p1 = (0, poses.Act3_preprise[0], poses.Act3_preprise[1])
            dist = dyn.compute_dist(p0, p1)
            if (dist<0.4):
                global_prise2_avail = False

            # FIXME : DEBUG
            print ("===================")
            print ("first_det = {}".format(first_det))
            print ("p0 = {}".format(p0))
            print ("p1 = {}".format(p1))
            print ("dist = {}".format(dist))
            print ("global_prise2_avail = {}".format(global_prise2_avail))
            print ()

            p1 = (0, poses.Act2_traj1_finish[0], poses.Act2_traj1_finish[1])
            dist = dyn.compute_dist(p0, p1)
            if (dist<0.4):
                global_prise1_avail = False

        await asyncio.sleep(1.0)


@robot.sequence
async def experimental_niv3_la_totale():
    global poses

    short_timeout = 0.1
    long_timeout = 0.2

    long_speed = 1.0
    turn_speed = 5.0

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    print ("******************************************************")
    print ("* Depose baniere")
    print ("******************************************************")
    # depose baniere
    await actuators_back.ascenseur_arr_down()
    await propulsion.reposition(-0.07, 0.2)
    await robot.setScore(robot.score + 20)

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    print ("******************************************************")
    print ("* Construction1 niv3")
    print ("******************************************************")
    # construction1 niv3
    await experimental_prise1_double()
    await asyncio.sleep(long_timeout)
    await experimental_goto_construction1_niv3()
    await asyncio.sleep(long_timeout)
    await experimental_construction1_niv3()
    await asyncio.sleep(long_timeout)
    await robot.setScore(robot.score + 28)

    propulsion.adversary_detection_enable = True

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    print ("******************************************************")
    print ("* Construction2 niv3")
    print ("******************************************************")
    # construction2 niv3
    await experimental_prise2()
    await asyncio.sleep(long_timeout)
    await experimental_goto_construction2_niv3()
    await asyncio.sleep(long_timeout)
    await experimental_construction2_niv3()
    await asyncio.sleep(long_timeout)
    await actuators_back.pump_arr_off()
    await robot.setScore(robot.score + 28)

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    print ("******************************************************")
    print ("* Deplacement vers la zone d'attente finale")
    print ("******************************************************")
    # deplacement vers la zone d'attente finale
    propulsion.adversary_detection_enable = False

    await propulsion.pointTo(poses.Act4_traj1_finish, turn_speed)
    await propulsion.moveToRetry(poses.Act4_traj1_finish, long_speed)

    await actuators_back.pump_arr_off()
    await actuators_pneuma.reset_valves()
    await actuators_pneuma.purge()

    await propulsion.faceDirection(0, turn_speed)
    await asyncio.sleep(short_timeout)

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    print ("******************************************************")
    print ("* Attente finale")
    print ("******************************************************")
    # attente finale
    while misc.match_time()<95.0:
        await asyncio.sleep(1.0)

    # deplacement final
    await propulsion.moveToRetry(poses.Act4_final, long_speed)
    await asyncio.sleep(short_timeout)
    await robot.setScore(robot.score + 10)

@robot.sequence
async def experimental_prise1_double():
    global poses

    short_timeout = 0.1
    long_timeout = 0.3

    long_speed = 0.6
    #turn_speed = 10.0
    turn_speed = 2.0

    propulsion.adversary_detection_enable = False

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
async def experimental_goto_construction1_niv3():
    global poses

    short_timeout = 0.1
    long_timeout = 0.3

    long_speed = 0.6
    turn_speed = 2.0

    propulsion.adversary_detection_enable = True

    if poses == pos.YellowPoses:
        predepose_1 = (1.5, -0.25, 0)
    elif poses == pos.BluePoses:
        predepose_1 = (1.5,  0.25, 0)
    else:
        raise RuntimeError('Side not set')
    await propulsion.pointTo(predepose_1, turn_speed)
    await propulsion.moveToRetry(predepose_1, long_speed)
    await propulsion.faceDirection(180, turn_speed)
    await asyncio.sleep(short_timeout)

@robot.sequence
async def experimental_construction1_niv3():
    global poses

    short_timeout = 0.1
    long_timeout = 0.3

    long_speed = 0.5
    # FIXME : DEBUG
    #turn_speed = 1.4
    turn_speed = 4.0

    await actuators_back.construction_1_etage_arr()
    await asyncio.sleep(long_timeout)

    # FIXME : DEBUG
    #t1 = asyncio.create_task(actuators_front.construction_2_etages_av_avec_predepose())

    await propulsion.faceDirection(0, turn_speed)
    await asyncio.sleep(short_timeout)
    await propulsion.translation(0.03, long_speed)
    await asyncio.sleep(short_timeout)

    # FIXME : DEBUG
    #await t1
    await actuators_front.construction_2_etages_av()

    # FIXME : DEBUG
    #await actuators_front.depose_3_etages_av()
    await actuators_front.depose_3_etages_av_avec_predepose()
    await asyncio.sleep(short_timeout)

    await actuators_front.ecarteur_int_av_off()
    await asyncio.sleep(short_timeout)

    await propulsion.translation(-0.1, long_speed)
    await asyncio.sleep(long_timeout)

@robot.sequence
async def experimental_prise2():
    global poses
    global global_prise2_avail

    short_timeout = 0.1
    long_timeout = 0.3

    long_speed = 0.6
    turn_speed = 2.0

    # chix prise
    if global_prise2_avail:
        prise_3 = poses.Act3_preprise
        if poses == pos.YellowPoses:
            face_direction_3 = -90
        elif poses == pos.BluePoses:
            face_direction_3 =  90
        else:
            raise RuntimeError('Side not set')
    else:
        face_direction_3 = 180
        if poses == pos.YellowPoses:
            prise_3 = (0.525, -0.675, 0)
        elif poses == pos.BluePoses:
            prise_3 = (0.525,  0.675, 0)
        else:
            raise RuntimeError('Side not set')

    ## prise3 AV
    propulsion.adversary_detection_enable = True
    await propulsion.pointTo(prise_3, turn_speed)
    await propulsion.moveToRetry(prise_3, long_speed)
    await asyncio.sleep(short_timeout)
    await propulsion.faceDirection(face_direction_3, turn_speed)
    await asyncio.sleep(short_timeout)
    propulsion.adversary_detection_enable = False
    await actuators_front.prise_av()
    await asyncio.sleep(short_timeout)
    await propulsion.reposition(-0.2, 0.2)
    await asyncio.sleep(long_timeout)

@robot.sequence
async def experimental_goto_construction2_niv3():
    global poses

    short_timeout = 0.1
    long_timeout = 0.3

    long_speed = 0.6
    turn_speed = 2.0

    propulsion.adversary_detection_enable = True

    if poses == pos.YellowPoses:
        predepose_2 = (1.35, -0.25, 0)
    elif poses == pos.BluePoses:
        predepose_2 = (1.35,  0.25, 0)
    else:
        raise RuntimeError('Side not set')
    await propulsion.pointTo(predepose_2, turn_speed)
    await propulsion.moveToRetry(predepose_2, long_speed)
    await propulsion.faceDirection(180, turn_speed)
    await asyncio.sleep(short_timeout)

@robot.sequence
async def experimental_construction2_niv3():
    global poses

    short_timeout = 0.1
    long_timeout = 0.3

    long_speed = 0.5
    turn_speed = 5.0

    propulsion.adversary_detection_enable = False

    await actuators_back.construction_1_etage_bis_arr()
    await asyncio.sleep(long_timeout)

    await propulsion.faceDirection(0, turn_speed)
    await asyncio.sleep(short_timeout)
    await propulsion.translation(0.015, long_speed)
    await asyncio.sleep(short_timeout)

    await actuators_front.construction_2_etages_av()

    await actuators_front.depose_3_etages_av_avec_predepose()
    await asyncio.sleep(short_timeout)

    await actuators_front.ecarteur_int_av_off()
    await asyncio.sleep(long_timeout)

@robot.sequence
async def experimental_construction2_niv3_dynamic():
    global poses

    propulsion.adversary_detection_enable = False

    short_timeout = 0.1
    long_timeout = 0.3

    long_speed = 0.5
    turn_speed = 1.3

    await actuators_back.construction_1_etage_bis_arr()
    await asyncio.sleep(long_timeout)

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

