import asyncio
from . import positions as pos
from . import robot_config as rc

@robot.sequence
async def recalage_plat():
    if robot.side == pos.Side.Blue:
        poses = pos.BluePoses
    elif robot.side == pos.Side.Green:
        poses = pos.GreenPoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)
    
    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.plat_start_pose[0],
                              poses.plat_start_pose[1]], 0)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([rc.robot_back_length , propulsion.pose.position.y], 0)
    await asyncio.sleep(1.0)

    print("Orientation axe Y")    
    await propulsion.moveTo(poses.plat_start_pose, 0.2)
    await propulsion.pointTo([poses.plat_start_pose[0], 0], 1)
    await asyncio.sleep(1.0)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    if robot.side == pos.Side.Green:
        await propulsion.setPose([propulsion.pose.position.x , 1.0 - rc.robot_back_length], -90)
    elif robot.side == pos.Side.Blue:
        await propulsion.setPose([propulsion.pose.position.x , -1.0 + rc.robot_back_length], 90)
    await asyncio.sleep(1.0)

    print("go depart")
    await propulsion.moveTo(poses.plat_start_pose, 0.2)
    if robot.side == pos.Side.Green:
        await propulsion.faceDirection(90, 1)
    await asyncio.sleep(1.0)


@robot.sequence
async def recalage_assiette():
    if robot.side == pos.Side.Blue:
        poses = pos.BluePoses
    elif robot.side == pos.Side.Green:
        poses = pos.GreenPoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)
    
    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.assiette_start_pose[0],
                              poses.assiette_start_pose[1]], 0)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([3.0 - rc.robot_back_length , propulsion.pose.position.y], 0)
    await asyncio.sleep(1.0)

    print("Orientation axe Y")    
    await propulsion.moveTo(poses.assiette_start_pose, 0.2)
    await propulsion.pointTo([poses.assiette_start_pose[0], 0], 0.2)
    await asyncio.sleep(1.0)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    if robot.side == pos.Side.Green:
        await propulsion.setPose([propulsion.pose.position.x , -1.5 + rc.robot_back_length], 90)
    elif robot.side == pos.Side.Blue:
        await propulsion.setPose([propulsion.pose.position.x , 1.5 - rc.robot_back_length], -90)
    await asyncio.sleep(1.0)

    print("go depart")
    await propulsion.moveTo(poses.plat_start_pose, 0.2)
    await asyncio.sleep(1.0)