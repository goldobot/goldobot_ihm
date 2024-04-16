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
#from . import test_actuators
#from . import test_sequences

from . import actuators
from . import pince_ravisseuse
from . import ejecteur

import inspect


test_match_goldo0 = ( 0.250,  0.750)
#test_match_goldo1 = ( 1.100, -0.100)
#test_match_goldo2 = ( 1.500, -0.100)

test_match_goldo1 = ( 0.570,  0.550)
test_match_goldo2 = ( 1.500,  0.450)

test_match_goldo3 = ( 1.500,  0.250)
test_match_goldo4 = ( 1.125,  0.274)
test_match_goldo5 = ( 0.675,  0.290)
test_match_goldo6 = ( 0.775,  0.545)
test_match_goldo7 = ( 0.250,  0.545)
test_match_goldo8 = ( 0.375,  0.545)
test_match_goldo9 = ( 0.550,  0.545)
test_match_goldo_fin = ( 1.650,  0.545)


traj_test_match_goldo = [
    test_match_goldo0,
    test_match_goldo1,
    test_match_goldo2,
    test_match_goldo3,
]


def debug_goldo(caller):
    print ()
    print ("************************************************")
    print (" GOLDO DEBUG :  {:32s}".format(inspect.currentframe().f_back.f_code.co_name))
    print ("************************************************")
    print ()

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
#avancee vers les fanions

class Pose:
    pass
    
class RefPoses:
    __ref_side__ = Side.Yellow
    start_pose: Pose = (0.955, -1.5 + rc.robot_width * 0.5 + 5e-3, 0)

class Map:
    zone_depart_x_min = 0.4
    zone_depart_x_max = 1.0


class YellowPoses:
    #start_pose = (0.675, -1.235, 90)
    start_pose = (0.675, -1.25, 90)
    
    figurine_pivot = (1.5, -1.0)
    figurine_preprise = on_segment((2.0,-0.99), (1.49, -1.5), rc.robot_rotation_distance_figurine)
    figurine_prise = on_segment((2.0,-0.99), (1.49, -1.5), rc.robot_back_length)
    display = (rc.robot_rotation_distance_figurine, -1.25)
    display_pose = (rc.robot_back_length, -1.25)
    
    a_prise_zone1 = (0.67, -0.9, 90)
    a_retour_zone_depart = (0.7, -1.2, -90)
    a_retour_presque_zone_depart = (0.8, -1.3, -90)
    a_prepare_depose_galerie = (0.4, -0.695, 180)
    a_depose_galerie = (0.210, -0.695, 180)

    # FIXME : DEBUG
    #pose_rush_3hex = (0.675, -0.750, 90)
    pose_rush_3hex = (0.675, -0.820, 90)
    pose_prise_3hex = (0.675, -0.890, 90)
    pose_pompe_3hex = (0.675, -0.950, 90)

    pose_ejecteur = (1.5, -1.0, -45)
    pose_prise_abri = (1.615, -1.115, -45)
    pose_depose_statuette = (0.4, -1.275, 0)

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
    #TEST GOLDO
    test_goldo0 = start_pose[0:2]
    test_goldo1 = (0.25, start_pose[1])
    test_goldo2 = (0.25,-0.75)
    test_goldo3 = (1.50,-0.75)
    test_goldo4 = (1.50, start_pose[1])
    traj_test_goldo = [
        test_goldo0,
        test_goldo1,
        test_goldo2,
        test_goldo3,
        test_goldo4,
        test_goldo0,
    ]
    
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
    a_prepare_depose_galerie = symetrie(YellowPoses.a_prepare_depose_galerie)
    a_depose_galerie = symetrie(YellowPoses.a_depose_galerie)

    pose_rush_3hex = symetrie(YellowPoses.pose_rush_3hex)
    pose_prise_3hex = symetrie(YellowPoses.pose_prise_3hex)
    pose_pompe_3hex = symetrie(YellowPoses.pose_pompe_3hex)

    pose_ejecteur = symetrie(YellowPoses.pose_ejecteur)
    pose_prise_abri = symetrie(YellowPoses.pose_prise_abri)
    pose_depose_statuette = symetrie(YellowPoses.pose_depose_statuette)
    
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

    #TEST GOLDO
    test_goldo0 = symetrie(YellowPoses.test_goldo0)
    test_goldo1 = symetrie(YellowPoses.test_goldo1)
    test_goldo2 = symetrie(YellowPoses.test_goldo2)
    test_goldo3 = symetrie(YellowPoses.test_goldo3)
    test_goldo4 = symetrie(YellowPoses.test_goldo4)
    traj_test_goldo = [symetrie(p) for p in YellowPoses.traj_test_goldo]


def load_strategy():
    a = strategy.create_action('prise_zone1')
    a.sequence = 'prise_zone1'
    a.enabled = False
    a.priority = 1
    a.begin_pose = poses.a_prise_zone1
    
    a = strategy.create_action('retour_zone_depart')
    a.sequence = 'retour_zone_depart'
    a.priority = 0
    a.enabled = True
    a.begin_pose = poses.a_retour_zone_depart

async def prise_zone1():
    debug_goldo(__name__)

    # fill with things with arms
    print('SEQUENCE: action 1')
    
    print('SEQUENCE: action 1 finished ')
    # FIXME : DEBUG
    #strategy.current_action.enabled = False

async def retour_zone_depart():
    debug_goldo(__name__)

    print('SEQUENCE: action 2')
    await asyncio.sleep(1)
    print('SEQUENCE: action 2 finished ')
    # FIXME : DEBUG
    #strategy.current_action.enabled = False
    
async def recalage():
    debug_goldo(__name__)

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
    # FIXME : TODO : remove
    #await propulsion.measureNormal(0, 0 + rc.robot_back_length)
    await propulsion.setPose([0+rc.robot_back_length, propulsion.pose.position.y], 0)
    print("decollage bordure")
    await propulsion.translation(poses.start_pose[0] - rc.robot_back_length, 0.2)
    if robot.side == Side.Purple:
        print("orientation violette")
        await propulsion.faceDirection(-90, 0.6)
        print("recalage violet")
        await propulsion.reposition(-1.0, 0.2)
        # FIXME : TODO : remove
        #await propulsion.measureNormal(-90, -1.5 + rc.robot_back_length)
        await propulsion.setPose([propulsion.pose.position.x, 1.5 - rc.robot_back_length, ], -90)
    elif robot.side == Side.Yellow:
        print("orientation jaune")
        await propulsion.faceDirection(90, 0.6)
        print("recalage jaune")
        await propulsion.reposition(-1.0, 0.2)
        # FIXME : TODO : remove
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

#@robot.sequence
async def old_prematch():
    global poses

    debug_goldo(__name__)

    if robot.side == Side.Purple:
        poses = PurplePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses
    else:
        raise RuntimeError('Side not set')
        
    print('prematch1')
    await lidar.stop()

    # Pince
    #taskpince = asyncio.create_task(pince_ravisseuse.initialize_pince())
    
    # Bras
    #await actuators.arms_initialize()
    #await taskpince

    # Ejecteur
    #await ejecteur.ejecteur_initialize()

    # Replique
    #await pince_ravisseuse.take_replica_left()

    #await asyncio.sleep(2)

    # Propulsion
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await recalage()
    
    #await lidar.start()
    #await robot.setScore(4)
    #await robot.setScore(24)

    #load_strategy()
    #print('loaded')

    return True
    #robot._adversary_detection_enable = False


async def arms_prise_3hex():
    if robot.side == Side.Purple:
        poses = PurplePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses
    await servos.setMaxTorque(actuators.arms_servos, 1)
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

async def goto_abri_chantier():
    debug_goldo(__name__)

    if robot.side == Side.Purple:
        poses = PurplePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses
    else:
        raise RuntimeError('Side not set')
        
    await propulsion.pointTo(poses.pose_ejecteur, 20.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(poses.pose_ejecteur, 1.0)
    await asyncio.sleep(0.5)
    if robot.side == Side.Purple:
        await propulsion.faceDirection(45,20.0)
    elif robot.side == Side.Yellow:
        await propulsion.faceDirection(-45,20.0)
    await asyncio.sleep(0.5)
    await actuators.arms_serrage_3hex()
    await asyncio.sleep(0.5)

# S'orienter vers l'abri de chantier
# Lever les éléments dans les bras, et éjecter l'élément du milieu
# Poser les éléments dans les bras, lever les bras, récupérer ceux de l'abri
# Ecarter les bras, pousser les éléments sous l'abri
async def abri_chantier():
    debug_goldo(__name__)

    if robot.side == Side.Purple:
        poses = PurplePoses
        await propulsion.faceDirection(45,20.0)
    elif robot.side == Side.Yellow:
        poses = YellowPoses
        await propulsion.faceDirection(-45,20.0)
    print("lifts")
    await actuators.lifts_ejecteur()
    await asyncio.sleep(0.3)
    await ejecteur.ejecteur_trigger()
    await robot.setScore(robot.score + 5)
    await asyncio.sleep(0.3)
    print("pumps")
    await robot.gpioSet('pompe_g', False)
    await robot.gpioSet('pompe_d', False)
    await asyncio.sleep(0.3)
    await actuators.lifts_top()
    await asyncio.sleep(0.3)
    await actuators.preprise_abri_chantier()
    await asyncio.sleep(0.3)
    await propulsion.moveTo(poses.pose_prise_abri, 0.6)
    await actuators.prise_abri_chantier()
    await robot.setScore(robot.score + 2)
    await asyncio.sleep(0.3)
    await actuators.lifts_top()
    await asyncio.sleep(0.3)
    #print("*********************************")
    #print("*********************************")
    #print("* DEBUG * DEBUG * DEBUG * DEBUG *")
    #print("*********************************")
    #print("*********************************")
    #await asyncio.sleep(60)
    await actuators.bras_ecartes()
    await asyncio.sleep(0.3)
    await propulsion.reposition(0.30, 0.2)
    await robot.setScore(robot.score + 10)
    await propulsion.moveTo(poses.pose_ejecteur, 0.2)
    await asyncio.sleep(0.3)
    await actuators.lifts_almost_top()
    await asyncio.sleep(0.3)

# S'orienter dos à la statuette et reculer en mode recalage pour la récupérer
# Si le capteur Hall ne détecte pas la prise de la statuette, petit wobble
async def prise_statuette():
    debug_goldo(__name__)

    if robot.side == Side.Purple:
        await propulsion.faceDirection(-135, 20.0)
    else:
        await propulsion.faceDirection(135, 20.0)

    await propulsion.reposition(-0.30, 0.2)
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
    await propulsion.translation(0.10, 0.2)
    await asyncio.sleep(0.3)
    await robot.setScore(robot.score + 5)
    await pince_ravisseuse.lift_put_replica()
    if robot.side == Side.Purple:
        await propulsion.faceDirection(-45, 2.0)
    else:
        await propulsion.faceDirection(-135, 2.0)
    await pince_ravisseuse.pince_put_replica()
    await pince_ravisseuse.lift_pince_top()
    await pince_ravisseuse.close_pince()
    await robot.setScore(robot.score + 10)
    await asyncio.sleep(1.0)

async def goto_vitrine():
    debug_goldo(__name__)

    await propulsion.pointTo(poses.pose_depose_statuette, 20.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(poses.pose_depose_statuette, 1.0)
    await asyncio.sleep(0.5)

# S'orienter dos à la vitrine et reculer en mode recalage pour poser la statuette
# Si le capteur à effet Hall ne detecte pas que la statuette est décrochée, petit wobble
async def depose_statuette():
    debug_goldo(__name__)

    await propulsion.faceDirection(0, 2.0)
    await propulsion.reposition(-1.0, 0.2)
    if sensors['hall_statuette'] == True:
        await propulsion.faceDirection(-2,1.0)
        await propulsion.faceDirection(2,1.0)
        await propulsion.faceDirection(-2,1.0)
        await propulsion.faceDirection(2,1.0)
    await propulsion.translation(0.10, 0.4)
    await robot.setScore(robot.score + 20)
    await asyncio.sleep(0.5)

async def carres_fouille_purple():
    debug_goldo(__name__)

    tryohm_val = None
    between_squares = 0.185
    offset = 0
    poses = PurplePoses
    await propulsion.faceDirection(-90,20.0)
    tryohm_val = await pince_ravisseuse.measure_tryohm_left()
    # Premier carré bonne couleur, on pousse les 2 premiers
    if tryohm_val == 'purple':
        task_pince = pince_ravisseuse.push_square_left()
        task_arm = actuators.push_square_left_arm()
        await task_pince
        await task_arm
        await robot.setScore(robot.score + 15)
    # Premier carré pas bonne couleur, on pousse le 2 et 3
    elif tryohm_val == 'red':
        offset = between_squares
        await propulsion.translation(offset, 0.6)
        task_pince = pince_ravisseuse.push_square_left()
        task_arm = asyncio.create_task(actuators.push_square_left_arm())
        await task_pince
        await task_arm
        await robot.setScore(robot.score + 15)
    # On arrive pas à lire, failsafe
    else:
        print("Failed to read square")
        await(actuators.push_square_left_arm)
        await robot.setScore(robot.score + 10)

    # On avance au 4ème carré
    await propulsion.translation(3 * between_squares - offset, 0.6)
    # Mesure 4ème carré
    tryohm_val = await pince_ravisseuse.measure_tryohm_left()
    # Si bonne couleur, on le tape et on tape le 7eme
    if tryohm_val == 'purple':
        await pince_ravisseuse.push_square_left()
        await robot.setScore(robot.score + 5)
        await propulsion.translation(2 * between_squares)
        await actuators.push_square_left_arm()
        await robot.setScore(robot.score + 5)
    # Si mauvaise couleur, on avance et on tape les 2 du milieu
    elif tryohm_val == 'yellow':
        await propulsion.translation(between_squares)
        task_pince = pince_ravisseuse.push_square_left()
        task_arm = asyncio.create_task(actuators.push_square_left_arm())
        await task_pince
        await task_arm
        await robot.setScore(robot.score + 10)
    # Si on arrive pas à lire, on tape les 4 du milieu
    else:
        task_pince = pince_ravisseuse.push_square_left()
        task_arm = asyncio.create_task(actuators.push_square_left_arm())
        await task_pince
        await task_arm
        await propulsion.translation(2 * between_squares)
        task_pince = pince_ravisseuse.push_square_left()
        task_arm = asyncio.create_task(actuators.push_square_left_arm())
        await task_pince
        await task_arm
        await robot.setScore(robot.score + 10)

async def carres_fouille_yellow():
    debug_goldo(__name__)

    tryohm_val = None
    between_squares = 0.185
    offset = 0
    poses = YellowPoses
    await propulsion.faceDirection(90,20.0)
    tryohm_val = await pince_ravisseuse.measure_tryohm_right()
    # Premier carré bonne couleur, on pousse les 2 premiers
    if tryohm_val == 'yellow':
        task_pince = pince_ravisseuse.push_square_right()
        task_arm = actuators.push_square_right_arm()
        await task_pince
        await task_arm
        await robot.setScore(robot.score + 15)
    # Premier carré pas bonne couleur, on pousse le 2 et 3
    elif tryohm_val == 'red':
        offset = between_squares
        await propulsion.translation(offset, 0.6)
        task_pince = pince_ravisseuse.push_square_right()
        task_arm = asyncio.create_task(actuators.push_square_right_arm())
        await task_pince
        await task_arm
        await robot.setScore(robot.score + 15)
    # On arrive pas à lire, failsafe
    else:
        print("Failed to read square")
        await(actuators.push_square_right_arm)
        await robot.setScore(robot.score + 10)

    # On avance au 4ème carré
    await propulsion.translation(3 * between_squares - offset, 0.6)
    # Mesure 4ème carré
    tryohm_val = await pince_ravisseuse.measure_tryohm_right()
    # Si bonne couleur, on le tape et on tape le 7eme
    if tryohm_val == 'yellow':
        await pince_ravisseuse.push_square_right()
        await robot.setScore(robot.score + 5)
        await propulsion.translation(2 * between_squares)
        await actuators.push_square_right_arm()
        await robot.setScore(robot.score + 5)
    # Si mauvaise couleur, on avance et on tape les 2 du milieu
    elif tryohm_val == 'purple':
        await propulsion.translation(between_squares)
        task_pince = pince_ravisseuse.push_square_right()
        task_arm = asyncio.create_task(actuators.push_square_right_arm())
        await task_pince
        await task_arm
        await robot.setScore(robot.score + 10)
    # Si on arrive pas à lire, on tape les 4 du milieu
    else:
        task_pince = pince_ravisseuse.push_square_right()
        task_arm = asyncio.create_task(actuators.push_square_right_arm())
        await task_pince
        await task_arm
        await propulsion.translation(2 * between_squares)
        task_pince = pince_ravisseuse.push_square_right()
        task_arm = asyncio.create_task(actuators.push_square_right_arm())
        await task_pince
        await task_arm
        await robot.setScore(robot.score + 10)

async def carres_fouille():
    debug_goldo(__name__)

    if robot.side == Side.Purple:
        poses = PurplePoses
        await carres_fouille_purple()
    elif robot.side == Side.Yellow:
        poses = YellowPoses
        await carres_fouille_yellow()  


#@robot.sequence
async def old_start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """
    debug_goldo(__name__)

    if robot.side == Side.Purple:
        poses = PurplePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses
    else:
        raise RuntimeError('Side not set')
        
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    print ("DEBUG : RUSH INITIAL")

    await propulsion.setAccelerationLimits(1,1,20,20)

    arms_task = asyncio.create_task(arms_prise_3hex())
    await propulsion.moveTo(poses.pose_rush_3hex, 1.0)
    await arms_task

    print ("DEBUG : WAIT PR MOVE 1")
    await asyncio.sleep(2.0)

    print ("DEBUG : ABRI CHANTIER")

    await goto_abri_chantier()

    await propulsion.setAccelerationLimits(1,1,2,2)

    await abri_chantier()

    await actuators.prepare_depose_galerie()

    await prise_statuette()

    await propulsion.setAccelerationLimits(1,1,20,20)

    print ("DEBUG : DEPOSE GALERIE")

    #await actuators.prepare_depose_galerie()

    await propulsion.pointTo(poses.a_prepare_depose_galerie, 20.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(poses.a_prepare_depose_galerie, 1.0)
    await asyncio.sleep(0.5)
    await propulsion.pointTo(poses.a_depose_galerie, 20.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(poses.a_depose_galerie, 1.0)
    await asyncio.sleep(0.5)

    await actuators.stop_pumps()
    await asyncio.sleep(0.5)

    await propulsion.moveTo(poses.a_prepare_depose_galerie, 1.0)
    await asyncio.sleep(0.5)

    print ("DEBUG : DEPOSE STATUETTE")

    await goto_vitrine()

    await depose_statuette()

    await propulsion.pointTo(poses.a_retour_presque_zone_depart, 20.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(poses.a_retour_presque_zone_depart, 1.0)
    await asyncio.sleep(0.5)
    await propulsion.faceDirection(-90, 0.8)
    await asyncio.sleep(0.5)

    await asyncio.sleep(60.0)


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

@robot.sequence
async def test_goldo_hippodrome():
    debug_goldo(__name__)

    if robot.side == Side.Purple:
        poses = PurplePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses
    else:
        raise RuntimeError('Side not set')
        
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    #await propulsion.pointTo(poses.test_goldo1, 10.0)
    #await asyncio.sleep(0.5)

    #await propulsion.trajectorySpline(poses.traj_test_goldo, speed=1.0)

    await propulsion.pointTo(poses.test_goldo1, 10.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(poses.test_goldo1, 1.0)
    await asyncio.sleep(0.5)

    await propulsion.pointTo(poses.test_goldo2, 10.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(poses.test_goldo2, 1.0)
    await asyncio.sleep(0.5)

    await propulsion.pointTo(poses.test_goldo3, 10.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(poses.test_goldo3, 1.0)
    await asyncio.sleep(0.5)

    await propulsion.pointTo(poses.test_goldo4, 10.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(poses.test_goldo4, 1.0)
    await asyncio.sleep(0.5)

    await propulsion.pointTo(poses.test_goldo0, 10.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(poses.test_goldo0, 1.0)
    await asyncio.sleep(0.5)

@robot.sequence
async def test_goldo_prematch():
    debug_goldo(__name__)

    global poses

    debug_goldo(__name__)

    if robot.side == Side.Purple:
        poses = PurplePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses
    else:
        raise RuntimeError('Side not set')
        
    await lidar.stop()

    # Pince
    #taskpince = asyncio.create_task(pince_ravisseuse.initialize_pince())
    
    # Bras
    #await actuators.arms_initialize()
    #await taskpince

    #await asyncio.sleep(2)

    # Propulsion
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    
    #await lidar.start()

    if robot.side == Side.Purple:
        await propulsion.setPose([0.25,  0.75], -45)
    elif robot.side == Side.Yellow:
        await propulsion.setPose([0.25, -0.75],  45)

    await actuators.test_goldo_init_cake()

    return True

@robot.sequence
async def test_goldo_traj():
    debug_goldo(__name__)

    if robot.side != Side.Purple:
        test_match_goldo0 = (test_match_goldo0[0],  -test_match_goldo0[1])
        test_match_goldo1 = (test_match_goldo1[0],  -test_match_goldo1[1])
        test_match_goldo2 = (test_match_goldo2[0],  -test_match_goldo2[1])
        test_match_goldo3 = (test_match_goldo3[0],  -test_match_goldo3[1])
        test_match_goldo4 = (test_match_goldo4[0],  -test_match_goldo4[1])
        test_match_goldo5 = (test_match_goldo5[0],  -test_match_goldo5[1])
        test_match_goldo6 = (test_match_goldo6[0],  -test_match_goldo6[1])
        test_match_goldo7 = (test_match_goldo7[0],  -test_match_goldo7[1])
        test_match_goldo8 = (test_match_goldo8[0],  -test_match_goldo8[1])
        test_match_goldo9 = (test_match_goldo9[0],  -test_match_goldo9[1])
        test_match_goldo_fin = (test_match_goldo_fin[0],  -test_match_goldo_fin[1])

    await propulsion.setAccelerationLimits(1,1,20,20)

    await propulsion.pointTo(test_match_goldo1, 20.0)
    await asyncio.sleep(0.5)

    await propulsion.trajectorySpline(traj_test_match_goldo, speed=1.0)

@robot.sequence
async def test_goldo_match():
    debug_goldo(__name__)

    test_match_goldo0 = ( 0.250,  0.750)
    #test_match_goldo1 = ( 1.100, -0.100)
    #test_match_goldo2 = ( 1.500, -0.100)

    test_match_goldo1 = ( 0.570,  0.550)
    test_match_goldo2 = ( 1.500,  0.450)

    test_match_goldo3 = ( 1.500,  0.250)
    test_match_goldo4 = ( 1.125,  0.274)
    test_match_goldo5 = ( 0.675,  0.290)
    test_match_goldo6 = ( 0.775,  0.545)
    test_match_goldo7 = ( 0.250,  0.545)
    test_match_goldo8 = ( 0.375,  0.545)
    test_match_goldo9 = ( 0.550,  0.545)
    test_match_goldo_fin = ( 1.650,  0.545)

    traj_test_match_goldo = [
        test_match_goldo0,
        test_match_goldo1,
        test_match_goldo2,
        test_match_goldo3,
    ]

    if robot.side != Side.Purple:
        test_match_goldo0 = (test_match_goldo0[0],  -test_match_goldo0[1])
        test_match_goldo1 = (test_match_goldo1[0],  -test_match_goldo1[1])
        test_match_goldo2 = (test_match_goldo2[0],  -test_match_goldo2[1])
        test_match_goldo3 = (test_match_goldo3[0],  -test_match_goldo3[1])
        test_match_goldo4 = (test_match_goldo4[0],  -test_match_goldo4[1])
        test_match_goldo5 = (test_match_goldo5[0],  -test_match_goldo5[1])
        test_match_goldo6 = (test_match_goldo6[0],  -test_match_goldo6[1])
        test_match_goldo7 = (test_match_goldo7[0],  -test_match_goldo7[1])
        test_match_goldo8 = (test_match_goldo8[0],  -test_match_goldo8[1])
        test_match_goldo9 = (test_match_goldo9[0],  -test_match_goldo9[1])
        test_match_goldo_fin = (test_match_goldo_fin[0],  -test_match_goldo_fin[1])
        traj_test_match_goldo = [
            test_match_goldo0,
            test_match_goldo1,
            test_match_goldo2,
            test_match_goldo3,
        ]

    await propulsion.setAccelerationLimits(1,1,20,20)

    await propulsion.pointTo(test_match_goldo1, 20.0)
    await asyncio.sleep(0.5)

    await propulsion.trajectorySpline(traj_test_match_goldo, speed=1.0)

    #await propulsion.pointTo(test_match_goldo1, 20.0)
    #await asyncio.sleep(0.5)
    #await propulsion.moveTo(test_match_goldo1, 1.0)
    #await asyncio.sleep(0.5)

    #await propulsion.pointTo(test_match_goldo2, 20.0)
    #await asyncio.sleep(0.5)
    #await propulsion.moveTo(test_match_goldo2, 1.0)
    #await asyncio.sleep(0.5)

    #await propulsion.pointTo(test_match_goldo3, 20.0)
    #await asyncio.sleep(0.5)
    #await propulsion.moveTo(test_match_goldo3, 1.0)
    #await asyncio.sleep(0.5)

    await propulsion.pointTo(test_match_goldo4, 20.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(test_match_goldo4, 1.0)
    await asyncio.sleep(0.5)

    await propulsion.pointTo(test_match_goldo5, 20.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(test_match_goldo5, 1.0)
    await asyncio.sleep(0.5)

    await propulsion.moveTo(test_match_goldo4, 1.0)
    await asyncio.sleep(0.5)

    await propulsion.pointTo(test_match_goldo6, 20.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(test_match_goldo6, 1.0)
    await asyncio.sleep(0.5)

    await propulsion.pointTo(test_match_goldo7, 20.0)
    await asyncio.sleep(0.5)

    if robot.side == Side.Purple:
        await actuators.test_goldo_cake1()
    else:
        await actuators.test_goldo_cake1_b()
    await asyncio.sleep(1.0)

    await propulsion.moveTo(test_match_goldo7, 1.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(test_match_goldo6, 1.0)
    await asyncio.sleep(0.5)

    if robot.side == Side.Purple:
        await actuators.test_goldo_cake2()
    else:
        await actuators.test_goldo_cake2_b()
    await asyncio.sleep(1.0)

    await propulsion.moveTo(test_match_goldo8, 1.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(test_match_goldo6, 1.0)
    await asyncio.sleep(0.5)

    if robot.side == Side.Purple:
        await actuators.test_goldo_cake3()
    else:
        await actuators.test_goldo_cake3_b()
    await asyncio.sleep(1.0)

    await propulsion.moveTo(test_match_goldo9, 1.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(test_match_goldo6, 1.0)
    await asyncio.sleep(0.5)

    await propulsion.moveTo(test_match_goldo_fin, 1.0)
    await asyncio.sleep(0.5)

@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """
    debug_goldo(__name__)

    await test_goldo_match()

@robot.sequence
async def prematch():

    debug_goldo(__name__)

    await test_goldo_prematch()

    return True

test_hyppo1 = ( 0.400, 0.800)
test_hyppo2 = ( 0.400,-0.800)
test_hyppo3 = ( 2.600,-0.800)
test_hyppo4 = ( 2.600, 0.800)

@robot.sequence
async def hyppo_prematch():

    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,20,20)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await asyncio.sleep(0.5)

    await propulsion.setPose([0.200,  0.000], 0)
    await asyncio.sleep(0.5)

@robot.sequence
async def hyppodrome():

    for i in range(0,3):
        await propulsion.pointTo(test_hyppo1, 20.0)
        await asyncio.sleep(0.5)
        await propulsion.moveTo(test_hyppo1, 1.0)
        await asyncio.sleep(0.5)

        await propulsion.pointTo(test_hyppo2, 20.0)
        await asyncio.sleep(0.5)
        await propulsion.moveTo(test_hyppo2, 1.0)
        await asyncio.sleep(0.5)

        await propulsion.pointTo(test_hyppo3, 20.0)
        await asyncio.sleep(0.5)
        await propulsion.moveTo(test_hyppo3, 1.0)
        await asyncio.sleep(0.5)

        await propulsion.pointTo(test_hyppo4, 20.0)
        await asyncio.sleep(0.5)
        await propulsion.moveTo(test_hyppo4, 1.0)
        await asyncio.sleep(0.5)
    
    await propulsion.pointTo(test_hyppo1, 20.0)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(test_hyppo1, 1.0)
    await asyncio.sleep(0.5)


