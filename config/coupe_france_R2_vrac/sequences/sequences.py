# import base modules
import asyncio
import numpy as np

# import modules from sequence directory
from . import pince
from . import positions as pos
from . import recalages
from . import robot_config as rc
from . import barillet
from . import gateau
from . import utils

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

check_areas_b = True
assiette_1 = True
assiette_2 = True
assiette_3 = True
jaune_1 = True
rose_1 = True
jaune_2 = True
rose_2 = True
five_secs_limit = False
in_zone = False

#Task pour verifier si un robot prend les gateaux marrons
async def check_areas():
    global assiette_1
    global rose_1
    global jaune_1
    global assiette_2
    global assiette_3
    global rose_2
    global jaune_2
    global check_areas_b
    while check_areas_b:
        if lidar.objectInDisk(poses.marron_assiette_1, 0.20):
            assiette_1 = False
        if lidar.objectInDisk(poses.marron_assiette_2, 0.20):
            assiette_2 = False
        if lidar.objectInDisk(poses.marron_assiette_3, 0.20):
            assiette_2 = False
        if lidar.objectInDisk(poses.rose_1, 0.20):
            rose_1 = False
        if lidar.objectInDisk(poses.rose_2, 0.20):
            rose_2 = False
        if lidar.objectInDisk(poses.jaune_1, 0.20):
            jaune_1 = False
        if lidar.objectInDisk(poses.jaune_2, 0.20):
            jaune_2 = False
        await asyncio.sleep(0.3)


@robot.sequence
async def prematch():

    global poses

    if robot.side == pos.Side.Blue:
        poses = pos.BluePoses
    elif robot.side == pos.Side.Green:
        poses = pos.GreenPoses
    else:
        raise RuntimeError('Side not set')

    # Propulsion
    await lidar.stop()
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    await pneumatic.lcd_off()
    await pneumatic.led_on()
    await barillet.reset_valves()
    await barillet.start_compressor()
    await barillet.barillet_init()
    await asyncio.sleep(2)
    await pince.pince_init()
    await pince.pince_take()
    await pince.chariot_close()
    await barillet.barillet_pose_2()
    
    # Lidar
    robot._adversary_detection_enable = False

    # Placement
    await recalages.recalage()
    if robot.start_zone == 4 or robot.start_zone == 7:
        await propulsion.pointTo(poses.waypoint_rush_initial, 1.0)

    await robot.setScore(0)
    await robot.gpioSet('keyboard_led', True)
    await lidar.start()

    end_action = strategy.create_action('return_home')
    end_action.sequence_prepare = ''
    end_action.sequence = 'end_match'
    end_action.enabled = True
    end_action.priority = 0
    end_action.begin_pose = poses.zone_fin

    return True


@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """

    pose_depart = (propulsion.pose.position.x, propulsion.pose.position.y, 180)
    
    traj_depart = [
        pose_depart,
        poses.waypoint_rush_initial,
        poses.prise_marron
    ]

    traj_retour = [
        poses.prise_marron,
        poses.waypoint_rush_initial,
        pose_depart
    ]

    traj_retour_alt = [
        poses.prise_marron_alt,
        pose_depart,
        poses.prise_jaune_alt
    ]

    global assiette_1
    global rose_1
    global jaune_1
    global assiette_2
    global assiette_3
    global rose_2
    global jaune_2
    global check_areas_b
    global five_secs_limit
    global in_zone

    five_secs_limit = False
    in_zone = False

    await propulsion.setAccelerationLimits(1,1,20,20)
    strategy.addTimerCallback(1, the_end)

    robot._adversary_detection_enable = True
    #tasklidar = asyncio.create_task(check_areas())

    # Collecte gateaux
    if robot.start_zone == 4 or robot.start_zone == 7:
        await pince.pince_open()
        await propulsion.trajectorySpline(traj_depart, 1.2)
    
        await gateau.prend_gateau1()

        await propulsion.pointTo(poses.pose_gateau_1, 5.0)
        await propulsion.trajectorySpline(traj_retour, 1.2)
        await propulsion.pointTo(poses.prise_rose, 5.0)
        await pince.pince_open()
        await asyncio.sleep(0.2)
        await propulsion.moveToRetry(poses.prise_rose, 1.0)
        
        await gateau.prend_gateau5()

        await pince.pince_open()
        await asyncio.sleep(0.2)
        await propulsion.moveToRetry(poses.prise_jaune, 1.0)

        await gateau.prend_gateau3()
    elif robot.start_zone == 3 or robot.start_zone == 8:
        await pince.pince_open()
        await propulsion.moveToRetry(poses.prise_marron_alt, 1.2)
        await asyncio.sleep(0.2)

        await gateau.prend_gateau1()

        await pince.pince_open()
        await propulsion.pointTo(poses.prise_inter_alt, 5.0)
        await propulsion.moveToRetry(poses.prise_inter_alt, 1.0)
        await propulsion.pointTo(poses.prise_jaune_alt, 5.0)
        await propulsion.moveToRetry(poses.prise_jaune_alt, 1.0)

        await gateau.prend_gateau3()

        await pince.pince_open()
        await propulsion.pointTo(poses.prise_rose_alt, 5.0)
        await propulsion.moveToRetry(poses.prise_rose_alt, 1.2)

        await gateau.prend_gateau5()

        await propulsion.translation(-0.3, 1.2)
    else:
        return

    # Construction gateaux
    #await propulsion.pointTo(poses.pose_aruco, 5.0)
    #await propulsion.moveToRetry(poses.pose_aruco, 0.5)
    await propulsion.pointTo(poses.pose_gateau_1, 5.0)
    await propulsion.moveToRetry(poses.pose_gateau_1, 1.0)

    if robot.side == pos.Side.Blue:
        await propulsion.faceDirection(-90, 5.0)
    elif robot.side == pos.Side.Green:
        await propulsion.faceDirection(90, 5.0)

    await gateau.build_cake_1()
    test = await utils.get_cake_layers()
    await pince.recentre_cerise()
    await pince.chariot_close()
    await gateau.pose_cerise(2)
    await pince.pince_open()

    if (await utils.get_cake_layers() == test + 1):
        if test == 3:
            await robot.setScore(robot.score + 10)
        else:
            await robot.setScore(robot.score + test + 3)
    else:
        await robot.setScore(robot.score + test)
    
    await propulsion.translation(-0.15, 1.2)

    await gateau.build_cake_1()
    test = await utils.get_cake_layers()
    await pince.recentre_cerise()
    await pince.chariot_close()
    await gateau.pose_cerise(4)
    await pince.pince_open()

    if (await utils.get_cake_layers() == test + 1):
        if test == 3:
            await robot.setScore(robot.score + 10)
        else:
            await robot.setScore(robot.score + test + 3)
    else:
        await robot.setScore(robot.score + test)

    await propulsion.translation(-0.15, 1.2)

    await gateau.build_last_cake()
    test = await utils.get_cake_layers()
    await pince.recentre_cerise()
    await pince.chariot_close()
    await gateau.pose_cerise(6)
    await pince.pince_open()

    if (await utils.get_cake_layers() == test + 1):
        if test == 3:
            await robot.setScore(robot.score + 10)
        else:
            await robot.setScore(robot.score + test + 3)
    else:
        await robot.setScore(robot.score + test)

    await propulsion.translation(-0.20, 1.2)

    await pince.pince_take()
    await barillet.reset_valves()

    await propulsion.pointTo(poses.pose_inter_fin, 5.0)
    await propulsion.moveToRetry(poses.pose_inter_fin, 1.2)

    # retour en zone
    await propulsion.pointTo(poses.zone_fin, 5)
    await propulsion.moveToRetry(poses.zone_fin, 1.2)
    end_action.enabled = False
    await robot.gpioSet('keyboard_led', False)
    await lidar.stop()
    await propulsion.faceDirection(0, 0.5)


async def need_end_match():
    global five_secs_limit
    print('5 sec limit reached')
    five_secs_limit = True


async def the_end():
    await barillet.reset_valves()
    await pneumatic.lcd_on()
    await robot.setScore(robot.score + 5)
    await robot.gpioSet('keyboard_led', False)
    await lidar.stop()


async def end_match():
    print('end match callback')
    strategy.current_action.enabled = False
