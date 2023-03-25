#Ajout gobelet vert grand port et detection robot secondaire
from asyncio import sleep
import asyncio
from socketserver import BaseRequestHandler
from tracemalloc import start

import numpy as np
import math
import random

#import modules from sequence directory
#purple replaces 2021's Blue
from .poses import YellowPoses, PurplePoses
from . import pince_ravisseuse

from . import robot_config as rc


import inspect

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)
class Side:
    Unknown = 0
    Purple = 1
    Yellow = 2


def symetrie(pose):
    pose = np.array(pose, dtype=np.float64)
    if isinstance(pose, np.ndarray):
        if pose.shape[0] == 2:
            return np.array([pose[0], -pose[1]])
    return (pose[0], -pose[1], -pose[2])

def on_segment(p1, p2, d):
    p1 = np.array(p1, dtype=np.float64)
    p2 = np.array(p2, dtype=np.float64)
    diff = p2 - p1
    midpoint = (p1 + p2) * 0.5
    diff = diff/np.linalg.norm(diff)
    nr = np.array([diff[1], -diff[0]])
    return midpoint + nr * d
    
class Pose:
    pass
    
class RefPoses:
    __ref_side__ = Side.Yellow
    start_pose: Pose = (0.955, -1.5 + rc.robot_width * 0.5 + 5e-3, 0)

class Map:
    zone_depart_x_min = 0.4
    zone_depart_x_max = 1.0    
    
class YellowPoses:
    start_pose = (0.675, -1.235, 90)
    hippodrome_1 =(0.5, 1, 90)
    hippodrome_2 =(0.5, -1, 0)
    hippodrome_3 =(1.5, 1, 180)
    hippodrome_4 =(1.5, -1, -90)

class PurplePoses:
    start_pose = symetrie(YellowPoses.start_pose)
    hippodrome_1 =(0.5, 1, 90)
    hippodrome_2 =(0.5, -1, 0)
    hippodrome_3 =(1.5, 1, 180)
    hippodrome_4 =(1.5, -1, -90)
            
async def pointAndGoRetry(p, speed, yaw_rate):
    await propulsion.pointTo(p, yaw_rate)
    await propulsion.moveToRetry(p, speed)

@robot.sequence
async def recalage():
    if robot.side == Side.Purple:
        poses = PurplePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses

    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(0.3,0.3,3,3)
    if robot.side == Side.Purple:
        await propulsion.setPose([0.40, 1.0], 0)
    elif robot.side == Side.Yellow:
        await propulsion.setPose([0.40, -1.0], 0)

    print("recalage X")
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.setPose([0+rc.robot_back_length, propulsion.pose.position.y], 0)
    await propulsion.translation(poses.start_pose[0] - rc.robot_back_length, 0.2)

    print("recalage Y")
    if robot.side == Side.Purple:
        print("orientation violette")
        await propulsion.faceDirection(-90, 0.6)
        print("recalage violet")
        await propulsion.reposition(-1.0, 0.2)
        await propulsion.setPose([propulsion.pose.position.x, 1.5 - rc.robot_back_length, ], -90)
    elif robot.side == Side.Yellow:
        print("orientation jaune")
        await propulsion.faceDirection(90, 0.6)
        print("recalage jaune")
        await propulsion.reposition(-1.0, 0.2)
        await propulsion.setPose([propulsion.pose.position.x, -1.5 + rc.robot_back_length, ], 90)
    print("decollage bordure")    
    await propulsion.translation(0.05, 0.2)
    print("go depart")
    await propulsion.moveTo(poses.start_pose, 0.2)
    if robot.side == Side.Purple:
        await propulsion.faceDirection(-90, 0.6)
    elif robot.side == Side.Yellow:
        await propulsion.faceDirection(90, 0.6)
    
 

@robot.sequence
async def prematch():
    global poses

    if robot.side == Side.Purple:
        poses = PurplePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses
    else:
        raise RuntimeError('Side not set')

    await lidar.start()

    # Propulsion
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,5,5)    
    await propulsion.setMotorsEnable(True)    
    await propulsion.setEnable(True)
    await recalage()
    await pince_ravisseuse.initialize_pince()
    await pince_ravisseuse.lift_pince_top()
    load_strategy()
    return True
    
def load_strategy():

    if robot.side == Side.Purple:
        poses = PurplePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses
    else:
        raise RuntimeError('Side not set')

    priorities = random.sample(range(0, 50), 4)

    print("Hippodrome 1 : priority = {} | position = {}".format(priorities[0], poses.hippodrome_1) )
    print("Hippodrome 2 : priority = {} | position = {}".format(priorities[1], poses.hippodrome_2) )
    print("Hippodrome 3 : priority = {} | position = {}".format(priorities[2], poses.hippodrome_3) )
    print("Hippodrome 4 : priority = {} | position = {}".format(priorities[3], poses.hippodrome_4) )

    a = strategy.create_action('hippodrome_1')
    a.sequence = 'hippodrome_1'
    a.enabled = True
    a.opponent_radius = 0.40
    a.speed = 1.2
    a.priority = priorities[0]
    a.begin_pose = poses.hippodrome_1
    
    a = strategy.create_action('hippodrome_2')
    a.sequence = 'hippodrome_2'
    a.priority = priorities[1]
    a.enabled = True
    a.opponent_radius = 0.50
    a.speed = 1.5
    a.begin_pose = poses.hippodrome_2

    a = strategy.create_action('hippodrome_3')
    a.sequence = 'hippodrome_3'
    a.priority = priorities[2]
    a.enabled = True
    a.opponent_radius = 0.30
    a.speed = 0.6
    a.begin_pose = poses.hippodrome_3

    a = strategy.create_action('hippodrome_4')
    a.sequence = 'hippodrome_4'
    a.priority = priorities[3]
    a.enabled = True
    a.begin_pose = poses.hippodrome_4


@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """

    if robot.side == Side.Purple:
        poses = PurplePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses
    else:
        raise RuntimeError('Side not set')
        
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await lidar.start()

    robot._adversary_detection_enable = True

@robot.sequence
async def hippodrome_1():
    await pince_ravisseuse.lift_pince_bottom()
    await pince_ravisseuse.lift_pince_top()
    print("Hippodrome 1 sequence")
    strategy.current_action.enabled = False

@robot.sequence
async def hippodrome_2():
    await pince_ravisseuse.lift_pince_bottom()
    await pince_ravisseuse.lift_pince_top()
    await pince_ravisseuse.lift_pince_bottom()
    await pince_ravisseuse.lift_pince_top()
    print("Hippodrome 2 sequence")
    strategy.current_action.enabled = False

@robot.sequence
async def hippodrome_3():
    await pince_ravisseuse.lift_pince_bottom()
    await pince_ravisseuse.lift_pince_top()
    await pince_ravisseuse.lift_pince_bottom()
    await pince_ravisseuse.lift_pince_top()
    await pince_ravisseuse.lift_pince_bottom()
    await pince_ravisseuse.lift_pince_top()
    print("Hippodrome 3 sequence")
    strategy.current_action.enabled = False

@robot.sequence
async def hippodrome_4():
    await pince_ravisseuse.lift_pince_bottom()
    await pince_ravisseuse.lift_pince_top()
    await pince_ravisseuse.lift_pince_bottom()
    await pince_ravisseuse.lift_pince_top()
    await pince_ravisseuse.lift_pince_bottom()
    await pince_ravisseuse.lift_pince_top()
    await pince_ravisseuse.lift_pince_bottom()
    await pince_ravisseuse.lift_pince_top()
    print("Hippodrome 4 sequence")
    strategy.current_action.enabled = False

async def end_match():
    print('end match callback')
    await robot.setScore(42)
    await lidar.start()
