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

secondary_robot_present = False

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
#avancÃ©e vers les fanions

class Pose:
    pass
    
class RefPoses:
    __ref_side__ = Side.Yellow
    start_pose: Pose = (0.955, -1.5 + rc.robot_width * 0.5 + 5e-3, 0)

class Map:
    zone_depart_x_min = 0.4
    zone_depart_x_max = 1.0
    
    
class YellowPoses:
    start_pose = (0.625, -1.235, 90)
    
    figurine_pivot = (1.5, -1.0)
    figurine_preprise = on_segment((2.0,-0.99), (1.49, -1.5), rc.robot_rotation_distance_figurine)
    figurine_prise = on_segment((2.0,-0.99), (1.49, -1.5), rc.robot_back_length)
    display = (rc.robot_rotation_distance_figurine, -1.25)
    display_pose = (rc.robot_back_length, -1.25)
    
    a_prise_zone1 = (0.67, -0.9, 90)
    a_retour_zone_depart = (0.9, -1.2, -90)
    a_retour_presque_zone_depart = (1.0, -1.3, -90)

    pose_rush_3hex = (0.675, -0.750, 90)
    pose_prise_3hex = (0.675, -0.890, 90)
    pose_pompe_3hex = (0.675, -0.950, 90)

    pose_ejecteur = (1.5, -1.0, -45)
    pose_prise_abri = (1.615, -1.115, -45)
    pose_depose_statuette = (0.4, -1.275, 0)

    pose_square_one = (1.8, -0.850, 90)

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
    a_retour_presque_zone_depart = symetrie(YellowPoses.a_retour_presque_zone_depart)

    pose_rush_3hex = symetrie(YellowPoses.pose_rush_3hex)
    pose_prise_3hex = symetrie(YellowPoses.pose_prise_3hex)
    pose_pompe_3hex = symetrie(YellowPoses.pose_pompe_3hex)

    pose_ejecteur = symetrie(YellowPoses.pose_ejecteur)
    pose_prise_abri = symetrie(YellowPoses.pose_prise_abri)
    pose_depose_statuette = symetrie(YellowPoses.pose_depose_statuette)
    
    pose_square_one = symetrie(YellowPoses.pose_square_one)
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
    #await propulsion.measureNormal(0, 0 + rc.robot_back_length)
    await propulsion.setPose([0+rc.robot_back_length, propulsion.pose.position.y], 0)
    print("decollage bordure")
    await propulsion.translation(poses.start_pose[0] - rc.robot_back_length, 0.2)
    if robot.side == Side.Purple:
        print("orientation violette")
        await propulsion.faceDirection(-90, 0.6)
        print("recalage violet")
        await propulsion.reposition(-1.0, 0.2)
        #await propulsion.measureNormal(-90, -1.5 + rc.robot_back_length)
        await propulsion.setPose([propulsion.pose.position.x, 1.5 - rc.robot_back_length, ], -90)
    elif robot.side == Side.Yellow:
        print("orientation jaune")
        await propulsion.faceDirection(90, 0.6)
        print("recalage jaune")
        await propulsion.reposition(-1.0, 0.2)
        #await propulsion.measureNormal(90, -1.5 + rc.robot_back_length)
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
async def test():
    print("test")

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
    await lidar.stop()

    await actuators.arms_initialize()
    # Pince
    if(sensors['sick_lat_g'] == True):
        await pince_ravisseuse.initialize_pince()
    # if(sensors['sick_lat_g'] == True):
    #     taskpince = asyncio.create_task(pince_ravisseuse.initialize_pince())
    # else:
    #     taskpince = asyncio.create_task(test())
    
    # # Bras
    # await actuators.arms_initialize()
    # await taskpince

    # Ejecteur
    #await ejecteur.ejecteur_initialize()

    # Replique
    await pince_ravisseuse.take_replica_left()

    await asyncio.sleep(1)
    
    # Si on est dans la zone de dÃ©part, on a 20 pts + les 4 de la vitrine
    await robot.setScore(24)


    # Propulsion
    await odrive.clearErrors()
    await propulsion.setEnable(True)
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)    
    await propulsion.setMotorsEnable(True)    
    await propulsion.setEnable(True)
    await recalage()

    await lidar.start()
    propulsion.adversary_detection_enable = False
    propulsion.adversary_detection_front_distance = 0.300

    load_strategy()
    print('loaded')

    return True

@robot.sequence
async def retour_zone_depart():
    coin1_zone_depart = [0, 0]
    coin2_zone_depart = [0, 0]
    if robot.side == Side.Purple:
        await propulsion.faceDirection(-135, 1.0)
        coin1_zone_depart = [1.2, 1.45]
        coin2_zone_depart = [0.25, 0.95]
    else:
        await propulsion.faceDirection(135, 1.0)
        coin1_zone_depart = [1.2, -1.45]
        coin2_zone_depart = [0.25, -0.95]
    if(lidar.objectInRectangle(coin1_zone_depart, coin2_zone_depart)):
        await robot.setScore(robot.score + 20)
    await asyncio.sleep(1)
    print('SEQUENCE: action 2 finished ')
    strategy.current_action.enabled = False 
    
def load_strategy():
    a = strategy.create_action('retour_zone_depart')
    a.sequence = 'retour_zone_depart'
    a.priority = 1
    a.enabled = False
    a.begin_pose = poses.a_retour_zone_depart

    a = strategy.create_action('prise_statuette')
    a.sequence = 'prise_statuette'
    a.priority = 3
    a.enabled = True
    a.begin_pose = poses.pose_ejecteur

    a = strategy.create_action('depose_statuette')
    a.sequence = 'depose_statuette'
    a.priority = 3
    a.enabled = False
    a.begin_pose = poses.pose_ejecteur

    a = strategy.create_action('first_square')
    a.sequence = 'first_square'
    a.priority = 4
    a.enabled = False
    a.begin_pose = poses.pose_square_one

@robot.sequence
async def prise_statuette():
    coin1_carres = [0, 0]
    coin2_carres = [0, 0]
    if robot.side == Side.Purple:
        await propulsion.faceDirection(-135, 1.0)
        coin1_carres = [1.6, 1.4]
        coin2_carres = [1.98, 0.1]
    else:
        await propulsion.faceDirection(135, 1.0)
        coin1_carres = [1.6, -1.4]
        coin2_carres = [1.98, -0.1]
    await propulsion.reposition(-1.0, 0.2)
    if sensors['hall_statuette'] == False:
        if robot.side == Side.Purple:
            await propulsion.faceDirection(-137, 1.0)
            await propulsion.faceDirection(-133, 1.0)
            await propulsion.faceDirection(-137, 1.0)
            await propulsion.faceDirection(-133, 1.0)
            await propulsion.faceDirection(-135, 1.0)
        else:
            await propulsion.faceDirection(137, 1.0)
            await propulsion.faceDirection(133, 1.0)
            await propulsion.faceDirection(137, 1.0)
            await propulsion.faceDirection(133, 1.0)
            await propulsion.faceDirection(135, 1.0)
    await propulsion.translation(0.10, 1.0)
    await robot.setScore(robot.score + 5)
    await pince_ravisseuse.lift_put_replica()
    if robot.side == Side.Purple:
        await propulsion.faceDirection(-45, 1.0)
    else:
        await propulsion.faceDirection(-135, 1.0)
    await pince_ravisseuse.pince_put_replica()
    await pince_ravisseuse.lift_pince_top()
    await pince_ravisseuse.close_pince()
    await robot.setScore(robot.score + 10)
    strategy.actions['prise_statuette'].enabled = False
    if not lidar.objectInRectangle(coin1_carres, coin2_carres):
        strategy.actions['first_square'].enabled = True
    strategy.actions['depose_statuette'].enabled = True
    
@robot.sequence
async def depose_statuette():
    coin1_carres = [0, 0]
    coin2_carres = [0, 0]
    if robot.side == Side.Purple:
        poses = PurplePoses
        coin1_carres = [1.6, 1.4]
        coin2_carres = [1.98, 0.1]
    elif robot.side == Side.Yellow:
        poses = YellowPoses
        coin1_carres = [1.6, -1.4]
        coin2_carres = [1.98, -0.1]
    #depose
    await propulsion.faceDirection(0, 1.0)
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.translation(0.20, 1.0)
    if sensors['hall_statuette'] == True:
        await propulsion.reposition(0.3, 0.2)
        await propulsion.faceDirection(2, 1.0)
        await propulsion.faceDirection(-2, 1.0)
        await propulsion.faceDirection(2, 1.0)
        await propulsion.faceDirection(-2, 1.0)
        await propulsion.faceDirection(0, 1.0)
    await propulsion.translation(0.20, 1.0)
    if sensors['hall_statuette'] == False:
        await robot.setScore(robot.score + 20)
    strategy.actions['depose_statuette'].enabled = False
    if strategy.actions['first_square'].priority != 42:
        if not lidar.objectInRectangle(coin1_carres, coin2_carres):
            strategy.actions['first_square'].enabled = True


@robot.sequence
async def first_square():
    tryohm_val = None
    if robot.side == Side.Purple:
        await propulsion.faceDirection(-90, 1.0)
    else:
        await propulsion.faceDirection(90, 1.0)
    # Mesure tryohm
    tryohm_val = await pince_ravisseuse.measure_tryohm_left()
    # Si le premier carrÃ© est de la bonne couleur on le shoot
    if robot.side == Side.Purple:
        if tryohm_val != None:
            if tryohm_val == 'purple':
                await pince_ravisseuse.push_square_left()
            else:
                await propulsion.translation(2 * 0.185, 0.6)
                await pince_ravisseuse.push_square_left()  
            await robot.setScore(robot.score + 5)          
    else :
        if tryohm_val != None:
            if tryohm_val == 'yellow':
                await pince_ravisseuse.push_square_right() 
            else:
                await propulsion.translation(2 * 0.185, 0.6)
                await pince_ravisseuse.push_square_right()
            await robot.setScore(robot.score + 5)
    first_square_done = True
    strategy.actions['first_square'].enabled = False
    strategy.actions['first_square'].priority = 42
    
async def arms_prise_3hex():
    if robot.side == Side.Purple:
        poses = PurplePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses
    await servos.setMaxTorque(actuators.arms_servos, 1)
    propulsion.adversary_detection_front_distance = 0.450
    await actuators.arms_prep_prise_3hex()
    while abs(propulsion.pose.position.y) > abs(poses.pose_pompe_3hex[1]):
        await asyncio.sleep(0.01)
    await robot.gpioSet('pompe_g', True)
    await robot.gpioSet('pompe_d', True)
    while abs(propulsion.pose.position.y) > abs(poses.pose_prise_3hex[1]):
        await asyncio.sleep(0.005)
    await actuators.lifts_prise_3hex()
    while abs(propulsion.pose.position.y) > abs(poses.pose_rush_3hex[1]):
        await asyncio.sleep(0.01)
    await actuators.arms_serrage_3hex()

@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """
    coin1_carres = [0, 0]
    coin2_carres = [0, 0]
    if robot.side == Side.Purple:
        poses = PurplePoses
        coin1_carres = [1.6, 1.4]
        coin2_carres = [1.98, 0.1]
    elif robot.side == Side.Yellow:
        poses = YellowPoses
        coin1_carres = [1.6, -1.4]
        coin2_carres = [1.98, -0.1]
    else:
        raise RuntimeError('Side not set')
        
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    await robot.setScore(4)

    # Go straight and activate avoidance
    await propulsion.moveTo(poses.pose_rush_3hex, 1.4)
    propulsion.adversary_detection_enable = True

    # Go devant l'abri de chantier
    await propulsion.pointTo(poses.pose_ejecteur, 2.0)
    await asyncio.sleep(5)
    await propulsion.moveTo(poses.pose_ejecteur, 1.4)
    
    # Prise de la statuette et dÃ©pose de la replique
    await prise_statuette()

    # Tryohm
    # Check with LIDAR if risky
    #if not lidar.objectInRectangle(coin1_carres, coin2_carres):
    #    await propulsion.pointTo(poses.pose_square_one, 1.0)
    #    await propulsion.moveTo(poses.pose_square_one, 1.0)
    #    await first_square()

    # Go a la vitrine
    await propulsion.pointTo(poses.pose_depose_statuette, 2.0)
    await propulsion.moveTo(poses.pose_depose_statuette, 1.4)
    
    # Depose statuette
    await depose_statuette()
    
    await propulsion.pointTo(poses.a_retour_presque_zone_depart, 2.0)
    await propulsion.moveTo(poses.a_retour_presque_zone_depart, 1.4)

    await robot.setScore(robot.score + 20)