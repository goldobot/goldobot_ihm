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

    await pneumatic.lcd_off()
    await barillet.barillet_init()
    await asyncio.sleep(2)
    await pince.pince_init()
    await pince.pince_take()
    await pince.chariot_close()
    
    # Lidar
    robot._adversary_detection_enable = False
    await lidar.start()

    # Placement
    await recalages.recalage()

    # Score +5 pour presence panier
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
    global check_areas_b
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

    await propulsion.pointTo(poses.marron_assiette_3, 1.5)
    await pince.pince_open()
    await asyncio.sleep(0.5)
    await propulsion.moveToRetry(poses.marron_assiette_3, 0.5)
    await pince.pince_take()
    await asyncio.sleep(0.5)
    await propulsion.pointTo(poses.assiette_3, 1.5)
    await propulsion.moveToRetry(poses.assiette_3, 0.5)
    await pince.pince_open()
    await asyncio.sleep(0.5)
    await propulsion.translation(-0.2, 0.5)
    await robot.setScore(robot.score + 6)
    await pince.pince_take()

    check_areas_b = False

    # retour en zone
    await propulsion.pointTo(poses.zone_fin, 1.5)
    await propulsion.moveToRetry(poses.zone_fin, 0.5)
    end_action.enabled = False
    in_zone = True
    await robot.gpioSet('keyboard_led', False)
    await lidar.stop()
    await propulsion.faceDirection(0, 0.5)


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
    await pneumatic.lcd_on()
    await robot.setScore(robot.score + 5)
    strategy.current_action.enabled = False
    await robot.gpioSet('keyboard_led', False)
    await lidar.stop()
