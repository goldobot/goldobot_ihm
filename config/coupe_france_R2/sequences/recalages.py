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
    elif robot.start_zone == 7:
        await recalage_zone_7()
    elif robot.start_zone == 8:
        await recalage_zone_8()
    elif robot.start_zone == 9:
        await recalage_zone_9()
    elif robot.start_zone == 10:
        await recalage_zone_10()
    else:
        print("Recalage : Wrong start zone")

async def recalage_zone_1():
    poses = pos.GreenPoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.zone1_start_pose[0],
                              poses.zone1_start_pose[1]], 0)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([rc.robot_back_length , propulsion.pose.position.y], 0)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")    
    await propulsion.moveTo(poses.zone1_start_pose, 0.2)
    await propulsion.pointTo([poses.zone1_start_pose[0], 0], 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([propulsion.pose.position.x , 1.0 - rc.robot_back_length], -90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone1_start_pose, 0.2)
    await propulsion.faceDirection(-90, 1)
    await asyncio.sleep(0.5)


async def recalage_zone_2():
    poses = pos.BluePoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put facing away from central camera stand
    await propulsion.setPose([poses.zone2_start_pose[0], 0], 0)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([rc.robot_back_length , propulsion.pose.position.y], 0)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")    
    await propulsion.moveTo([poses.zone2_start_pose[0], propulsion.pose.position.y], 0.2)
    await propulsion.faceDirection(-90, 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-2.0, 0.2)
    await propulsion.setPose([propulsion.pose.position.x , 1.0 - rc.robot_back_length], -90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone2_start_pose, 0.2)
    await propulsion.faceDirection(-90, 1)
    await asyncio.sleep(0.5)


async def recalage_zone_3():
    poses = pos.GreenPoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put in zone 5, facing central camera stand
    await propulsion.setPose([poses.zone3_start_pose[0], 0], 180)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([3.000 - rc.robot_back_length , propulsion.pose.position.y], 180)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")    
    await propulsion.moveTo([poses.zone3_start_pose[0], propulsion.pose.position.y], 0.2)
    await propulsion.faceDirection(-90, 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-2.0, 0.2)
    await propulsion.setPose([propulsion.pose.position.x , 1.0 - rc.robot_back_length], -90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone3_start_pose, 0.2)
    await propulsion.faceDirection(-90, 1)
    await asyncio.sleep(0.5)


async def recalage_zone_4():
    poses = pos.BluePoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.zone4_start_pose[0],
                              poses.zone4_start_pose[1]], 180)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([3.00 - rc.robot_back_length , propulsion.pose.position.y], 180)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")    
    await propulsion.moveTo(poses.zone4_start_pose, 0.2)
    await propulsion.faceDirection(-90, 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([propulsion.pose.position.x , 1.0 - rc.robot_back_length], -90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone4_start_pose, 0.2)
    await propulsion.faceDirection(180, 1)
    await asyncio.sleep(0.5)


async def recalage_zone_5():
    poses = pos.GreenPoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put in zone 3, facing away from border
    await propulsion.setPose([poses.zone5_start_pose[0] - 1.00, poses.zone5_start_pose[1]], -90)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([propulsion.pose.position.x , 1.00 - rc.robot_back_length], -90)
    await asyncio.sleep(0.5)

    print("Orientation axe X")    
    await propulsion.moveTo([propulsion.pose.position.x, poses.zone5_start_pose[1]], 0.2)
    await propulsion.faceDirection(180, 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-2.0, 0.2)
    await propulsion.setPose([3.000 - rc.robot_back_length , propulsion.pose.position.y], 180)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone5_start_pose, 0.2)
    await propulsion.faceDirection(180, 1)
    await asyncio.sleep(0.5)


async def recalage_zone_6():
    poses = pos.BluePoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put in zone 3, facing away from border
    await propulsion.setPose([poses.zone6_start_pose[0] - 1.00, poses.zone6_start_pose[1]], 90)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([propulsion.pose.position.x , 1.00 - rc.robot_back_length], 90)
    await asyncio.sleep(0.5)

    print("Orientation axe X")    
    await propulsion.moveTo([propulsion.pose.position.x, poses.zone6_start_pose[1]], 0.2)
    await propulsion.faceDirection(180, 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-2.0, 0.2)
    await propulsion.setPose([3.000 - rc.robot_back_length , propulsion.pose.position.y], 180)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone6_start_pose, 0.2)
    await propulsion.faceDirection(180, 1)
    await asyncio.sleep(0.5)


async def recalage_zone_7():
    poses = pos.GreenPoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.zone7_start_pose[0],
                              poses.zone7_start_pose[1]], 180)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([3.00 - rc.robot_back_length , propulsion.pose.position.y], 180)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")    
    await propulsion.moveTo(poses.zone7_start_pose, 0.2)
    await propulsion.pointTo([poses.zone7_start_pose[0], 0], 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([propulsion.pose.position.x , -1.0 + rc.robot_back_length], 90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone7_start_pose, 0.2)
    await propulsion.faceDirection(180, 1)
    await asyncio.sleep(0.5)


async def recalage_zone_8():
    poses = pos.BluePoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put in zone 6, facing central camera stand
    await propulsion.setPose([poses.zone8_start_pose[0], 0], 180)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([3.000 - rc.robot_back_length , propulsion.pose.position.y], 180)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")    
    await propulsion.moveTo([poses.zone8_start_pose[0], propulsion.pose.position.y], 0.2)
    await propulsion.faceDirection(90, 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-2.0, 0.2)
    await propulsion.setPose([propulsion.pose.position.x , -1.0 + rc.robot_back_length], 90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone8_start_pose, 0.2)
    await propulsion.faceDirection(90, 1)
    await asyncio.sleep(0.5)


async def recalage_zone_9():
    poses = pos.GreenPoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put facing away from central camera stand
    await propulsion.setPose([poses.zone9_start_pose[0], 0], 0)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([rc.robot_back_length , propulsion.pose.position.y], 0)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")    
    await propulsion.moveTo([poses.zone9_start_pose[0], propulsion.pose.position.y], 0.2)
    await propulsion.faceDirection(90, 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-2.0, 0.2)
    await propulsion.setPose([propulsion.pose.position.x , -1.0 + rc.robot_back_length], 90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone9_start_pose, 0.2)
    await propulsion.faceDirection(90, 1)
    await asyncio.sleep(0.5)


async def recalage_zone_10():
    poses = pos.BluePoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.zone10_start_pose[0],
                              poses.zone10_start_pose[1]], 0)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([rc.robot_back_length , propulsion.pose.position.y], 0)
    await asyncio.sleep(0.5)

    print("Orientation axe Y")    
    await propulsion.moveTo(poses.zone10_start_pose, 0.2)
    await propulsion.pointTo([poses.zone10_start_pose[0], 0], 1)
    await asyncio.sleep(0.5)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([propulsion.pose.position.x , -1.0 + rc.robot_back_length], 90)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.zone10_start_pose, 0.2)
    await propulsion.faceDirection(90, 1)
    await asyncio.sleep(0.5)
