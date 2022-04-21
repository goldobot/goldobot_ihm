#Ajout gobelet vert grand port et detection robot secondaire
from asyncio import sleep
import asyncio

import numpy as np
import math

#import modules from sequence directory
#purple replaces 2021's Blue
from .poses import YellowPoses, PurplePoses
from .herse import herse
from .pales import pales
from . import robot_config as rc
from . import test_actuators
from . import test_sequences

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

class Side:
    Unknown = 0
    Blue = 1
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

class YellowPoses:
    start_pose = (0.70, -1.5 + rc.robot_back_length, 90)
    t1 = [
        start_pose[0:2],
        (0.70,-0.9),
        (1.25,-0.9),
        (1.5, -1.0),
        on_segment((2.0,-0.99), (1.49, -1.5), rc.robot_front_length + 0.01)
        ]
    t2 = [
        t1[-1],
        (1.5, -1.0),
        (1.25,-0.9),
        (0.55,-1.1),
        (0.35,-1.25),
        (0.15,-1.25)
        ]
    t3 = [
        (0.15,-0.62),
        (0.9,-0.62),
        (1.1,-0.9),
        (1.5, -1.0),
        t1[-1]
        ]
    t4 = [
        t3[-1],
        on_segment((2.0,-0.99), (1.49, -1.5), rc.robot_front_length + 0.05),
        (1.75, -0.3),
        (1.35, -0.3),
        (1.35, -0.7),
        ]
    
class BluePoses:
    # start_pose = (0.8, -1.4 + robot_width * 0.5, 0)
    start_pose = symetrie(YellowPoses.start_pose)
    t1 = [symetrie(p) for p in YellowPoses.t1]
    t2 = [symetrie(p) for p in YellowPoses.t2]
    t3 = [symetrie(p) for p in YellowPoses.t3]
    t4 = [symetrie(p) for p in YellowPoses.t4]
    
            
async def pointAndGoRetry(p, speed, yaw_rate):
    await propulsion.pointTo(p, yaw_rate)
    await propulsion.moveToRetry(p, speed)
    
    
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
    global poses
    
    if robot.side == Side.Blue:
        poses = BluePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses
    else:
        raise RuntimeError('Side not set')
        
    await lidar.start()
    await robot.setScore(0)

    #servos
    await servos.setEnable('pale_g', True)
    await servos.setEnable('pale_d', True)
    await pales.move(both='ferme')

    #await servos.setEnable('fanion', True)
    #await servos.move('fanion', fanion_ferme)

    #await servos.setEnable('bras_lat_gauche', True)
    #await servos.move('bras_lat_gauche', bras_lat_gauche_rentre)

    #await servos.setEnable('bras_lat_droite', True)
    #await servos.move('bras_lat_droite', bras_lat_droite_rentre)

    await herse.initialize()

    await odrive.clearErrors()
    await propulsion.clearError()
    
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    
    await propulsion.setPose(poses.start_pose[0:2], poses.start_pose[2])
    print('start pose')
    #a = await propulsion.reposition(-0.1, 0.1)
    #if a.data1 == 0:
    #    raise RuntimeError("reposition didn't hit")

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

    await propulsion.trajectorySpline(poses.t1, speed=1.0)
    await propulsion.trajectorySpline(poses.t2, speed=1.0)
    await propulsion.pointAndGo(poses.t3[0], 1.0, 1.0)
    await propulsion.pointTo(poses.t3[1], 1.0)
    await propulsion.trajectorySpline(poses.t3, speed=1.0)
    await propulsion.trajectorySpline(poses.t4, speed=1.0)
    
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
