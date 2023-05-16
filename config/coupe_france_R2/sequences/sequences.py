# import base modules
import asyncio
import numpy as np

# import modules from sequence directory
from . import pince
from . import positions as pos
from . import recalages
from . import robot_config as rc
from . import barillet

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

check_areas = True
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
    global check_areas
    while check_areas:
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
        await asyncio.sleep(0.2)


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
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    
    # Lidar
    robot._adversary_detection_enable = False
    await lidar.start()

    # Placement
    await recalages.recalage()

    # Score +5 pour presence panier
    await robot.setScore(5)
    await robot.gpioSet('keyboard_led', True)

    return True


@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """
    traj_depart = [
        poses.plat_start_pose,
        poses.plat_inter_pose,
        poses.prise_marron
    ]

    global assiette_1
    global rose_1
    global jaune_1
    global assiette_2
    global assiette_3
    global rose_2
    global jaune_2
    global check_areas
    global five_secs_limit
    global in_zone

    await propulsion.setAccelerationLimits(1,1,20,20)
    strategy.addTimerCallback(1, end_match)
    strategy.addTimerCallback(5, need_end_match)

    end_action = strategy.create_action('return_home')
    end_action.sequence_prepare = ''
    end_action.sequence = 'end_match'
    end_action.enabled = True
    end_action.priority = 0
    end_action.begin_pose = poses.zone_fin

    # await propulsion.pointTo(poses.prise_marron, 1.5)
    robot._adversary_detection_enable = True
    tasklidar = asyncio.create_task(check_areas())


    if robot.start_zone == 1 or robot.start_zone == 10: 
        try:
            await propulsion.trajectorySpline(traj_depart, speed=0.5)
        except:
            await propulsion.clearError()
            await propulsion.translation(-0.15, 0.5)
            await propulsion.pointTo(poses.prise_marron, 1.0)
            await propulsion.moveToRetry(poses.prise_marron, 0.5)
    elif robot.start_zone == 2 or robot.start_zone == 9:
        print("alt start zone")
        await propulsion.moveToRetry(poses.prise_marron_alt, 1.0)
        assiette_1 = False
    else:
        await propulsion.pointTo(poses.prise_marron, 1.0)
        await propulsion.moveToRetry(poses.prise_marron, 0.5)
    await taskarms

    # Depose marron
    await propulsion.pointTo(poses.pose_construction, 1.5)
    await propulsion.moveToRetry(poses.pose_construction, 1.0)
    await propulsion.pointTo(poses.depose_marron, 1.5)
    await propulsion.moveToRetry(poses.depose_marron, 0.5)

    # Pose construction
    await propulsion.moveToRetry(poses.pose_construction, 1.0)
    await propulsion.faceDirection(180, 1.5)

    check_areas = False

    # retour en zone
    await propulsion.pointTo(poses.zone_fin, 1.5)
    await propulsion.moveToRetry(poses.zone_fin, 1.0)
    end_action.enabled = False
    in_zone = True
    await propulsion.faceDirection(0, 1.5)


async def need_end_match():
    global five_secs_limit
    print('5 sec limit reached')
    five_secs_limit = True


async def the_end():
    global in_zone
    in_zone = True


async def end_match():
    global in_zone
    print('end match callback')
    if robot.side == pos.Side.Green:
        if lidar.objectInRectangle([2.60, 0.40], [2.999, 0.0]):
            if in_zone is True:
                robot.setScore(robot.score + 15)
    else:
        if lidar.objectInRectangle([2.60, -0.40], [2.999, 0.0]):
            if in_zone is True:
                robot.setScore(robot.score + 15)

    await robot.gpioSet('keyboard_led', False)
    lidar.stop()
