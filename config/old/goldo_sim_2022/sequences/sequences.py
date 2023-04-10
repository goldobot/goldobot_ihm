#Ajout gobelet vert grand port et detection robot secondaire
from asyncio import sleep
import asyncio

import numpy as np
import math

#import modules from sequence directory
from . import test_actuators
from . import test_sequences

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

class Side:
    Unknown = 0
    Purple = 1
    Yellow = 2

#values for 07 2021
robot_width = 0.255
robot_front_length =  0.1197
robot_back_length = 0.0837

def symetrie(pose):
    if isinstance(pose, np.ndarray):
        if pose.shape[0] == 2:
            return np.array([pose[0], -pose[1]])
    return (pose[0], -pose[1], -pose[2])

def on_segment(p1, p2, d):
    diff = p2 - p1
    midpoint = (p1 + p2) * 0.5
    diff = diff/np.linalg.norm(diff)
    nr = np.array([diff[1], -diff[0]])
    return midpoint + nr * d
    
def set_astar_static_obstacles():
    # borders
    strategy._astar.fillRect((0, -1.5), (0.1, 1.5), 0)
    strategy._astar.fillRect((1.9, -1.5), (2.0, 1.5), 0)
    strategy._astar.fillRect((0, -1.5), (2.0, -1.4), 0)
    strategy._astar.fillRect((0, 1.4), (2.0, 1.5), 0)
    # obstacles
    strategy._astar.fillRect((0, -0.1), (0.4, 0.1), 0)


class PurplePoses(object):
    start_pose_simul_goldo = (0.55, 1.4, -90)


class YellowPoses(object):
    start_pose_simul_goldo = symetrie(PurplePoses.start_pose_simul_goldo)


async def moveToRetry(p, speed):
    await propulsion.moveToRetry(p, speed)
            
async def pointAndGoRetry(p, speed, yaw_rate):
    await propulsion.pointTo(p, yaw_rate)
    await moveToRetry(p, speed)
    
@robot.sequence
async def test_recalage():
    #test recalage coin bleu
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(2,2,2,2)
    await propulsion.setPose([0.15, -1.35], 95)
    await propulsion.reposition(-0.1, 0.1)
    await propulsion.measureNormal(90, -1.5 + robot_back_length)
    await propulsion.translation(0.15, 0.5)
    await propulsion.faceDirection(0, 0.5)
    await propulsion.reposition(-0.2, 0.1)
    await propulsion.measureNormal(0, 0 + robot_back_length)
    await propulsion.translation(0.15, 0.5)

@robot.sequence
async def prematch():
    print (" DEBUG GOLDO : prematch()")

    await propulsion.setAccelerationLimits(4.0,4.0,20,20)

    global poses
    #await lidar.start()

    strategy._astar.resetCosts()
    set_astar_static_obstacles()
    #strategy._astar.fillDisk((1.0,0.0), 0.4, 5)
    #strategy._astar.fillDisk((1.0,0.0), 0.3, 0)
    #await strategy.display_astar()

    await robot.setScore(0)

    #servos
    # FIXME : TODO

    await odrive.clearErrors()
    await propulsion.clearError()


    if robot.side == Side.Purple:
        poses = PurplePoses
    if robot.side == Side.Yellow:
        poses = YellowPoses
    await propulsion.setPose(poses.start_pose_simul_goldo[0:2], poses.start_pose_simul_goldo[2])

    print (" DEBUG GOLDO : prematch() DONE")

    return True
    #robot._adversary_detection_enable = False

@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    strategy.addTimerCallback(3, end_match)
    strategy.addTimerCallback(1, check_secondary_robot)
    if robot.side == Side.Purple:
        print ("FIXME : TODO")
    if robot.side == Side.Yellow:
        print ("test_goldo()")
        await test_goldo()
    #strategy.actions['action1'].enabled = True

async def end_match():
    print('end match callback')
    await servos.move('fanion', fanion_ouvert)
    await sleep(2)
    await servos.move('fanion', fanion_ferme)
    await robot.setScore(robot.score + 10)

async def check_secondary_robot():
    print('Check if second robot is in zone')
    if girouette == 'unknown':
        print('Yes')
        await robot.setScore(robot.score + 10)
    elif lidar.objectFrontFar():
        print('Yes')
        await robot.setScore(robot.score + 10)
    else:
        print('No')    

@robot.sequence
async def test_emergency_stop():
    await propulsion.setAccelerationLimits(0.5,0.5,0.5,0.5)
    await propulsion.setPose([0,0], 0)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    await propulsion.reposition(0.2,0.1)

    task = asyncio.create_task(propulsion.translation(0.5, 0.1))
    await sleep(1)
    await propulsion.setTargetSpeed(0.3)
    await sleep(1)
    print('estop')
    await propulsion.emergencyStop()
    await task

async def test_goldo():
    #await propulsion.trajectory([(0.65,-1.0)], 0.5)

    #await propulsion.trajectory([(0.7,-0.55),(1.05,0.02),(1.4,0.3),(1.7,0.3)], 0.5)
    #await sleep(2)
    #await propulsion.pointTo((1.54, 0.15), 20)
    #await sleep(2)
    ##print (rplidar_detections)
    #strategy._astar.resetCosts()
    #for d in rplidar_detections:
    #    #print (d)
    #    if (d.detect_quality>0):
    #        strategy._astar.setDisk((d.x,d.y), 30)
    #await strategy.display_astar()
    #new_path = strategy._astar.computePath((1.7,0.3), (1.8, -1.3))
    #print (new_path)
    #await propulsion.trajectorySpline(new_path, 0.5)

    # PR 2022
    await propulsion.trajectory([(0.55,-1.0),(0.2,-0.7),(0.2,-0.45),(0.45,-0.15)], 0.5)
    await sleep(1)
    await propulsion.pointTo((0.10, -0.15), 20)
    await sleep(1)
    await propulsion.trajectory([(0.15,-0.15)], 0.5)
    await sleep(10)
    await propulsion.pointTo((0.25, -0.45), 20)
    await sleep(1)
    await propulsion.trajectory([(0.25, -0.45)], 0.5)
    await sleep(1)
    await propulsion.pointTo((0.10, -0.45), 20)
    await sleep(1)
    await propulsion.trajectory([(0.2,-0.45)], 0.5)
    await sleep(10)
    await propulsion.pointTo((1.0, 0.0), 20)
    await sleep(1)
    #await propulsion.trajectory([(1.0, 0.0)], 0.5)
    strategy._astar.resetCosts()
    set_astar_static_obstacles()
    for d in rplidar_detections:
        #print (d)
        if (d.detect_quality>0):
            #strategy._astar.fillDisk((d.x,d.y), 0.3, 5)
            strategy._astar.fillDisk((d.x,d.y), 0.3, 0)
    await strategy.display_astar()
    new_path = strategy._astar.computePath((0.2,-0.45), (1.0, 0.0))
    new_path = [(0.2,-0.45)] + new_path
    print (new_path)
    await propulsion.trajectorySpline(new_path, 0.5)
    await sleep(1)
