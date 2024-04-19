import asyncio
from . import positions as pos
from . import robot_config as rc


@robot.sequence
async def recalage():
    if robot.start_zone == 1:
        await recalage_zone_1()
    elif robot.start_zone == 2:
        await recalage_zone_2()
    elif robot.start_zone == 3:
        await recalage_zone_3()
    elif robot.start_zone == 4:
        await recalage_zone_4()
    elif robot.start_zone == 5:
        await recalage_zone_5()
    elif robot.start_zone == 6:
        await recalage_zone_6()
    else:
        print("Recalage : Wrong start zone")


async def recalage_zone_1():
    poses = pos.YellowPoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.zone1_start_pose[0],
                              poses.zone1_start_pose[1]], 180)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.setPose([2.0 - rc.robot_back_length, propulsion.pose.position.y], 180)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")
    await propulsion.moveTo(poses.zone1_start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.pointTo([poses.zone1_start_pose[0], 90], 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.setPose([propulsion.pose.position.x , 1.5 - rc.robot_back_length], 90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone1_start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.faceDirection(90, 1)
    await asyncio.sleep(0.5)

async def recalage_zone_2():
    poses = pos.BluePoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.zone2_start_pose[0],
                              poses.zone2_start_pose[1]], 180)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.setPose([2.0 - rc.robot_back_length, propulsion.pose.position.y], 180)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")
    await propulsion.moveTo(poses.zone2_start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.pointTo([poses.zone2_start_pose[0], 90], 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.setPose([propulsion.pose.position.x , 1.5 - rc.robot_back_length], 90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone2_start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.faceDirection(90, 1)
    await asyncio.sleep(0.5)

async def recalage_zone_3():
    poses = pos.YellowPoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.zone3_start_pose[0],
                              poses.zone3_start_pose[1]], 0)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.setPose([rc.robot_back_length, propulsion.pose.position.y], 0)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")
    await propulsion.moveTo(poses.zone3_start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.pointTo([poses.zone3_start_pose[0], 90], 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.setPose([propulsion.pose.position.x , 1.5 - rc.robot_back_length], 90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone3_start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.faceDirection(90, 1)
    await asyncio.sleep(0.5)

async def recalage_zone_4():
    poses = pos.BluePoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.zone4_start_pose[0],
                              poses.zone4_start_pose[1]], 0)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.setPose([rc.robot_back_length, propulsion.pose.position.y], 0)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")
    await propulsion.moveTo(poses.zone4_start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.pointTo([poses.zone4_start_pose[0], -90], 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.setPose([propulsion.pose.position.x , 1.5 - rc.robot_back_length], -90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone1_start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.faceDirection(-90, 1)
    await asyncio.sleep(0.5)

async def recalage_zone_5():
    poses = pos.YellowPoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.zone5_start_pose[0],
                              poses.zone5_start_pose[1]], 180)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.setPose([2.0 - rc.robot_back_length, propulsion.pose.position.y], 180)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")
    await propulsion.moveTo(poses.zone5_start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.pointTo([poses.zone5_start_pose[0], -90], 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.setPose([propulsion.pose.position.x , 1.5 - rc.robot_back_length], -90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone5_start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.faceDirection(-90, 1)
    await asyncio.sleep(0.5)

async def recalage_zone_6():
    poses = pos.BluePoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.zone6_start_pose[0],
                              poses.zone6_start_pose[1]], 180)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.setPose([2.0 - rc.robot_back_length, propulsion.pose.position.y], 180)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")
    await propulsion.moveTo(poses.zone6_start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.pointTo([poses.zone6_start_pose[0], -90], 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.setPose([propulsion.pose.position.x , 1.5 - rc.robot_back_length], -90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone6_start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.faceDirection(-90, 1)
    await asyncio.sleep(0.5)