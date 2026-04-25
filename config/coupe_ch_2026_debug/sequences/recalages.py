import asyncio
from . import positions as pos
from . import robot_config as rc

@robot.sequence
async def recalage():
    if robot.start_zone == 1:
        await recalage_zone_1()
    elif robot.start_zone == 2:
        await recalage_zone_2()
    else:
        print("Recalage : Wrong start zone")

# BLUE
async def recalage_zone_1():
    poses = pos.BluePoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.Start_pose[0],
                              poses.Start_pose[1]], 0)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([propulsion.pose.position.x , 1.5 - rc.robot_back_length], -90)
    await asyncio.sleep(0.5)

    print("Orientation axe X")
    await propulsion.moveTo([propulsion.pose.position.x , poses.Start_pose[1]], 0.2)
    await asyncio.sleep(0.5)
    await propulsion.faceDirection(0, 1)
    await asyncio.sleep(0.5)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([rc.robot_back_length , propulsion.pose.position.y], 0)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.Start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.faceDirection(0, 1)
    await asyncio.sleep(0.5)


# YELLOW
async def recalage_zone_2():
    poses = pos.YellowPoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)

    # Robot is to put approximately at its start pose
    await propulsion.setPose([poses.Start_pose[0],
                              poses.Start_pose[1]], 0)

    print("Recalage axe Y")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([propulsion.pose.position.x , -1.5 + rc.robot_back_length], 90)
    await asyncio.sleep(0.5)

    print("Orientation axe X")    
    await propulsion.moveTo([propulsion.pose.position.x , poses.Start_pose[1]], 0.2)
    await asyncio.sleep(0.5)
    await propulsion.faceDirection(0, 1)
    await asyncio.sleep(0.5)

    print("Recalage axe X")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([rc.robot_back_length , propulsion.pose.position.y], 0)
    await asyncio.sleep(0.5)

    print("go depart")
    await propulsion.moveTo(poses.Start_pose, 0.2)
    await asyncio.sleep(0.5)
    await propulsion.faceDirection(0, 1)
    await asyncio.sleep(0.5)


