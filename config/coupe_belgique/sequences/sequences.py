# import base modules
import asyncio
import numpy as np

# import modules from sequence directory
from . import positions as pos
from . import recalages
from . import canon_cerises
from . import distrib_cerises
from . import actuators
from . import robot_config as rc

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

check_areas = True
assiette_1 = True
assiette_2 = True

#Task pour verifier si un robot prend les gateaux marrons
async def check_areas():
    global assiette_1
    global assiette_2
    global check_areas
    while check_areas:
        if lidar.objectInDisk(poses.marron_assiette_1, 0.20):
            assiette_1 = False
        if lidar.objectInDisk(poses.marron_assiette_2, 0.20):
            assiette_2 = False
        await asyncio.sleep(0.1)


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

    # Actionneurs
    await distrib_cerises.distrib_enable()
    await distrib_cerises.distrib_neutral()
    #await canon_cerises.canon_initialize()
    await actuators.arms_initialize()

    # Placement
    await recalages.recalage_plat()

    # Score +5 pour presence panier
    await robot.setScore(5)

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
    global assiette_2
    global check_areas

    await propulsion.setAccelerationLimits(1,1,20,20)

    taskarms = asyncio.create_task(actuators.arms_open())
    await canon_cerises.canon_shoot()

    # Prise marron
    if robot.side == pos.Side.Green:
        await propulsion.faceDirection(-90, 1.5)

    # await propulsion.pointTo(poses.prise_marron, 1.5)
    # robot._adversary_detection_enable = True
    tasklidar = asyncio.create_task(check_areas())
    # await propulsion.moveTo(poses.prise_marron, 1.0)
    await propulsion.trajectorySpline(traj_depart, speed=1.0)
    await taskarms
    
    # Prise avec les bras
    await actuators.arms_take()

    # Depose marron
    await propulsion.pointTo(poses.pose_construction, 1.5)
    await propulsion.moveTo(poses.pose_construction, 1.0)
    await propulsion.pointTo(poses.depose_marron, 1.5)
    await propulsion.moveTo(poses.depose_marron, 0.5)

    # Depose avec les bras
    await actuators.arms_open()
    await asyncio.sleep(0.2)

    # Pose construction
    await propulsion.moveTo(poses.pose_construction, 1.0)
    await propulsion.faceDirection(180, 1.5)


    # Construction gateau 1
    if robot.side == pos.Side.Green:
        await actuators.construction_gateau_haut_vert()
    else:
        await actuators.construction_gateau_haut_bleu()
    await actuators.goldo_lifts_move(60, 80)
    await propulsion.moveTo(poses.pose_gateau_1, 1.0)
    await actuators.arms_take()
    await distrib_cerises.distrib_lache()
    await asyncio.sleep(0.2)
    await actuators.arms_open()
    await robot.setScore(robot.score + 10)

    # Construction gateau 2
    await propulsion.moveTo(poses.pose_construction, 1.0)
    await propulsion.faceDirection(180, 1.5)
    if robot.side == pos.Side.Green:
        await actuators.construction_gateau_milieu_vert()
    else:
        await actuators.construction_gateau_milieu_bleu()
    await actuators.goldo_lifts_move(60, 80)
    await propulsion.moveTo(poses.pose_gateau_2, 1.0)
    await actuators.arms_take()
    await distrib_cerises.distrib_lache()
    await asyncio.sleep(0.2)
    await actuators.arms_open()
    await robot.setScore(robot.score + 10)

    # Construction gateau 3
    await propulsion.moveTo(poses.pose_construction, 1.0)
    await propulsion.faceDirection(180, 1.5)
    if robot.side == pos.Side.Green:
        await actuators.construction_gateau_bas_vert()
    else:
        await actuators.construction_gateau_bas_bleu()
    await actuators.goldo_lifts_move(60, 80)
    await propulsion.moveTo(poses.pose_gateau_3, 1.0)
    await actuators.arms_take()
    await distrib_cerises.distrib_lache()
    await asyncio.sleep(0.2)
    await actuators.arms_open()
    await robot.setScore(robot.score + 10)

    # Recul
    await propulsion.translation(-0.15, 1.0)
    
    # Prise marron
    if assiette_1:
        await propulsion.pointTo(poses.marron_assiette_1, 1.5)
        await propulsion.moveTo(poses.marron_assiette_1, 1.0)
        await actuators.arms_take()
        await propulsion.pointTo(poses.assiette_1, 1.5)
        await propulsion.moveTo(poses.assiette_1, 1.0)
        await distrib_cerises.distrib_lache()
        await actuators.arms_open()
        await robot.setScore(robot.score + 7)
        await asyncio.sleep(0.2)
        await propulsion.translation(-0.15, 1.0)

    if assiette_2:
        await propulsion.pointTo(poses.marron_assiette_2, 1.5)
        await propulsion.moveTo(poses.marron_assiette_2, 1.0)
        await actuators.arms_take()
        await propulsion.pointTo(poses.assiette_2, 1.5)
        await propulsion.moveTo(poses.assiette_2, 1.0)
        await distrib_cerises.distrib_lache()
        await actuators.arms_open()
        await robot.setScore(robot.score + 7)
        await asyncio.sleep(0.2)
        await propulsion.translation(-0.15, 1.0)
    


    check_areas = False

    # retour en zone
    await propulsion.pointTo(poses.zone_fin, 1.5)
    await propulsion.moveTo(poses.zone_fin, 1.0)
    await robot.setScore(robot.score + 10)


async def end_match():
    print('end match callback')
    lidar.stop()