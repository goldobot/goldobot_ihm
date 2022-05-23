#Ajout gobelet vert grand port et detection robot secondaire
from asyncio import sleep
import asyncio
from socketserver import BaseRequestHandler
from tracemalloc import start

import numpy as np
import math

#import modules from sequence directory
#purple replaces 2021's Blue
from .poses import YellowPoses, PurplePoses

from . import robot_config as rc
from . import test_actuators
from . import test_sequences

from . import actuators
from . import pince_ravisseuse
from . import ejecteur
from . import tests_2022
from . import tests_2022_goldo

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
    
#strategie homologation
#depart robot parallele au bord de latable
#avancée vers les fanions

class Pose:
    pass
    
class RefPoses:
    __ref_side__ = Side.Yellow
    start_pose: Pose = (0.955, -1.5 + rc.robot_width * 0.5 + 5e-3, 0)

class Map:
    zone_depart_x_min = 0.4
    zone_depart_x_max = 1.0
    
    
    
    
    
class YellowPoses:
    start_pose = (0.675, -1.20, 90)
    
    figurine_pivot = (1.5, -1.0)
    figurine_preprise = on_segment((2.0,-0.99), (1.49, -1.5), rc.robot_rotation_distance_figurine)
    figurine_prise = on_segment((2.0,-0.99), (1.49, -1.5), rc.robot_back_length)
    display = (rc.robot_rotation_distance_figurine, -1.25)
    display_pose = (rc.robot_back_length, -1.25)
    
    a_prise_zone1 = (0.67, -0.9, 90)
    a_retour_zone_depart = (0.7, -1.2, -90)
    
    g1 = (rc.robot_rotation_distance_figurine, -0.4)
    
    g2 = (0.7, -1.05)
    g3 = (0.3,-1.0)
    
    g4 = (1.375, -0.7)
    g5 = (1.3, -0.925)
    g6 = (1.50, -1.0)
    g7 = (0.7, -0.9)
    g8 = (0.7, -1.1)
    
    g9 = (0.7, -1.1)
    
    # prise figurine
    t1 = [
        start_pose[0:2],
        (start_pose[0],-1.1),
        (1.3,-1.1),
        (1.75,-0.8),
        (1.75,-0.35),
        (1.55,-0.2),
        (1.375,-0.2),
        ]
    # prise figurine vers depose
    t2 = [
        t1[-1],
        g4,
        (1.20,-0.9),
        (0.9, -1.0),
        (0.7, -1.1),
        (0.7, -1.2)
        ]
    # depose vers 1er groupe
    t3 = [
        g2,
        (0.3,-1.0),
        (0.3,-0.4),
        (0.675,-0.3),
        ]
    #vers 2eme groupe
    t4 = [
        (0.3,-0.4),
        g5,
        (1.50, -1.0),
        on_segment((2.0,-0.99), (1.49, -1.5), rc.robot_front_length + 0.05)
        ]
    #spline rush initial (gotta go fast !)
    traj_rush = [
        (start_pose[0] - rc.robot_width * 0.5, -1.05 + rc.robot_back_length),
        (0.675 - rc.robot_width * 0.5, -0.9 + rc.robot_back_length),
        (0.675 - rc.robot_width * 0.5, -0.74 + rc.robot_back_length)
    ]
    #start to display
    
class PurplePoses:
    # start_pose = (0.8, -1.4 + robot_width * 0.5, 0)
    start_pose = symetrie(YellowPoses.start_pose)
    figurine_pivot = symetrie(YellowPoses.figurine_pivot)
    figurine_preprise = symetrie(YellowPoses.figurine_preprise)
    figurine_prise = symetrie(YellowPoses.figurine_prise)
    display = symetrie(YellowPoses.display)
    display_pose = symetrie(YellowPoses.display_pose)
    
    #actions
    a_prise_zone1 = symetrie(YellowPoses.a_prise_zone1)
    a_retour_zone_depart = symetrie(YellowPoses.a_retour_zone_depart)
    
    g1 = symetrie(YellowPoses.g1)
    g2 = symetrie(YellowPoses.g2)
    g3 = symetrie(YellowPoses.g3)
    g4 = symetrie(YellowPoses.g4)
    g5 = symetrie(YellowPoses.g5)
    g6 = symetrie(YellowPoses.g6)
    g7 = symetrie(YellowPoses.g7)
    g8 = symetrie(YellowPoses.g8)
    
    t1 = [symetrie(p) for p in YellowPoses.t1]
    t2 = [symetrie(p) for p in YellowPoses.t2]
    t3 = [symetrie(p) for p in YellowPoses.t3]
    t4 = [symetrie(p) for p in YellowPoses.t4]
    traj_rush = [symetrie(p) for p in YellowPoses.traj_rush]
    
            
async def pointAndGoRetry(p, speed, yaw_rate):
    await propulsion.pointTo(p, yaw_rate)
    await propulsion.moveToRetry(p, speed)
    
 

@robot.sequence
async def prematch():
    global poses
    
    if robot.side == Side.Purple:
        poses = PurplePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses
    else:
        raise RuntimeError('Side not set')
        
    print('prematch1')
    await lidar.start()
    await robot.setScore(0)

    # Bras
    await actuators.arms_initialize()


    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)    
    await propulsion.setMotorsEnable(True)    
    await propulsion.setEnable(True)
    
    #await propulsion.setPose(poses.start_pose[0:2], poses.start_pose[2])
    #a = await propulsion.reposition(0.1, 0.1)
    await propulsion.setPose(poses.start_pose[0:2], poses.start_pose[2])
    
    #await propulsion.translation(0.05, 0.2)
    
    load_strategy()
    print('loaded')

    return True
    #robot._adversary_detection_enable = False

async def match_prise_figurine():
    await propulsion.trajectorySpline(poses.t1, speed=1.0)
    await propulsion.pointAndGo(poses.figurine_prise, 1.0, yaw_rate, back = True)
    await propulsion.moveTo(poses.figurine_preprise, 1.0)
    
async def depose_figurine():
    await propulsion.trajectorySpline(poses.t2, speed=1.0)
    await propulsion.faceDirection(0, yaw_rate)
    await propulsion.moveTo(poses.display_pose, 1.0)
    await asyncio.sleep(1)
    await propulsion.moveTo(poses.display, 1.0)
    await robot.setScore(20)

# @robot_sequence()
# async def inital_rush():
#     print('rush_initial')
#     await propulsion.trajectorySpline(poses.traj_rush, speed=0.2)
    
    
@robot.sequence
async def prise_zone1():
    # fill with things with arms
    print('SEQUENCE: action 1')
    await asyncio.sleep(1)
    print('SEQUENCE: action 1 finished ')
    strategy.current_action.enabled = False  

@robot.sequence
async def retour_zone_depart():
    print('SEQUENCE: action 2')
    await asyncio.sleep(1)
    print('SEQUENCE: action 2 finished ')
    strategy.current_action.enabled = False     
    
    
def load_strategy():
    a = strategy.create_action('prise_zone1')
    a.sequence = 'prise_zone1'
    a.enabled = True
    a.priority = 1
    a.begin_pose = poses.a_prise_zone1
    
    a = strategy.create_action('retour_zone_depart')
    a.sequence = 'retour_zone_depart'
    a.priority = 0
    a.enabled = True
    a.begin_pose = poses.a_retour_zone_depart

    
    
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
    
    #await propulsion.setPose(poses.start_pose[0:2], poses.start_pose[2])
    
    #strategy.addTimerCallback(3, end_match)
    #strategy.addTimerCallback(1, check_secondary_robot)
    
    #await propulsion.trajectorySpline(poses.t1, speed=1.0)    
    
    return
    #await lidar.stop()
    #robot._adversary_detection_enable = False
    
    yaw_rate = 5.0
    
    #prepare to get group 1 (south)
    await propulsion.trajectorySpline(poses.t1, speed=1.0)    
    await propulsion.pointTo(poses.g4, yaw_rate)
    await pales.move(both='ouvert')
    await asyncio.sleep(1)
    
    # bring group 1 into starting area
    await propulsion.trajectorySpline(poses.t2, speed=0.5)  
    await robot.setScore(20)

    # get out of starting area     
    await propulsion.pointAndGo(poses.g2, 1.0, yaw_rate, back = True)
    await pales.move(both='ferme')
    await asyncio.sleep(1)
    
    # prepare to push group 2
    await propulsion.pointTo(poses.g3, yaw_rate)
    await propulsion.trajectorySpline(poses.t3, speed=1.0)
    await propulsion.pointTo(poses.g2, yaw_rate)
    await pales.move(both='ouvert') 
    await asyncio.sleep(1)
    await propulsion.moveTo(poses.g2, speed=1.0)    
    return
    

    
    #strategy.actions['action1'].enabled = True

async def end_match():
    print('end match callback')
    await robot.setScore(42)

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


