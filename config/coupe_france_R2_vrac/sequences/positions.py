import numpy as np
from . import robot_config as rc

def symetrie(pose):
    if isinstance(pose, np.ndarray):
        if pose.shape[0] == 2:
            return np.array([pose[0], -pose[1]])
    return (pose[0], -pose[1], -pose[2])


class Side:
    Unknown = 0
    Green = 1
    Blue = 2


class GreenPoses:
    # Poses recalages vert:
    zone1_start_pose = (0.2, 0.8, 0)
    zone3_start_pose = (1.875, 0.7, -90)
    zone5_start_pose = (2.8, 0.275, 180)
    zone7_start_pose = (2.8, -0.8, 180)
    zone9_start_pose = (1.125, -0.8, 90)

    # Poses recalages bleu:
    zone2_start_pose = (1.125, 0.8, -90)
    zone4_start_pose = (2.8, 0.8, 180)
    zone6_start_pose = (2.8, -0.275, 180)    
    zone8_start_pose = (1.875, -0.7, 90)
    zone10_start_pose = (0.2, -0.8, 0)

    # demarrage coin
    waypoint_rush_initial = (2.5, -0.3, 90)

    # retour en zone
    zone_fin = (2.83, 0.3, 0)
    pose_inter_fin = (2.3, 0.3, 0)

    # Poses depart coin
    prise_marron = (1.875, -0.275, 30)
    prise_jaune = (2.325, -0.775, 180)
    prise_rose = (2.525, -0.775, 180)

    prise_marron_alt = (1.875, 0.275, -90)
    prise_inter_alt = (1.875, 0.775, 180)
    prise_jaune_alt = (2.175, 0.775, 180)
    prise_rose_alt = (2.425, 0.775, 180)

    # Poses gateaux finis
    # pose_gateau_1 = (2.75, -0.750, 0) # pour mettre bien dans le coin
    pose_gateau_1 = (1.875, 0.80, 90) # pour mettre bien dans le coin
    pose_aruco = (2.35, -0.350, -45)

    pose_vol_evo = (2.560, 0.06, -45)


    # Gateaux marrons
    marron_assiette_1 = (1.125, -0.275, -90)
    marron_assiette_2 = (1.875, 0.275, 90)
    assiette_1 = (1.200, -0.70, -90)
    depose_j_1 = (1.0, -0.60, -90)
    depose_r_1 = (0.850, -0.60, -90)
    assiette_2 = (1.940, 0.6, 90)
    prise_j1 = (0.805, -0.700, -90)
    prise_r1 = (0.575, -0.700, -90)

    marron_assiette_3 = (1.875, -0.275, -90)
    assiette_3 = (1.760, 0.6, 90)
    
    rose_1 = (0.575, -0.775, 0)
    dep_rose_1 = (0.9, -0.775, 0)
    rose_2 = (2.425, 0.775, 0)
    dep_rose_2 = (2.1, 0.775, 0)
    jaune_1 = (0.775, -0.775, 0)
    jaune_2 = (2.225, 0.775, 0)

    jr_1 = (0.3, -0.775, 0)
    jr_2 = (0.3, -0.775, 0)

class BluePoses:
    # Poses recalages vert:
    zone1_start_pose = (0.2, 0.8, 0)
    zone3_start_pose = (1.875, 0.8, -90)
    zone5_start_pose = (2.8, 0.275, 180)
    zone7_start_pose = (2.8, -0.8, 180)
    zone9_start_pose = (1.125, -0.8, 90)
    
    # Poses recalages bleu:
    zone2_start_pose = (1.125, 0.8, -90)
    zone4_start_pose = (2.8, 0.8, 180)
    zone6_start_pose = (2.8, -0.275, 180)
    zone8_start_pose = (1.875, -0.8, 90)
    zone10_start_pose = (0.2, -0.8, 0)

    # demarrage coin
    waypoint_rush_initial = symetrie(GreenPoses.waypoint_rush_initial)
   
    # retour en zone
    zone_fin = symetrie(GreenPoses.zone_fin)
    pose_inter_fin = symetrie(GreenPoses.pose_inter_fin)

    prise_marron = symetrie(GreenPoses.prise_marron)
    prise_jaune = symetrie(GreenPoses.prise_jaune)
    prise_rose = symetrie(GreenPoses.prise_rose)

    prise_marron_alt = symetrie(GreenPoses.prise_marron_alt)
    prise_inter_alt = symetrie(GreenPoses.prise_inter_alt)
    prise_jaune_alt = symetrie(GreenPoses.prise_jaune_alt)
    prise_rose_alt = symetrie(GreenPoses.prise_rose_alt)

    # Poses gateaux finis
    pose_gateau_1 = symetrie(GreenPoses.pose_gateau_1)
    pose_aruco = symetrie(GreenPoses.pose_aruco)

    # Gateaux marrons
    marron_assiette_1 = symetrie(GreenPoses.marron_assiette_1)
    marron_assiette_2 = symetrie(GreenPoses.marron_assiette_2)
    assiette_1 = symetrie(GreenPoses.assiette_1)
    depose_j_1 = symetrie(GreenPoses.depose_j_1)
    depose_r_1 = symetrie(GreenPoses.depose_r_1)
    assiette_2 = symetrie(GreenPoses.assiette_2)
    prise_j1 = symetrie(GreenPoses.prise_j1)
    prise_r1 = symetrie(GreenPoses.prise_r1)
    
    marron_assiette_3 = symetrie(GreenPoses.marron_assiette_3)
    assiette_3 = symetrie(GreenPoses.assiette_3)

    rose_1 = symetrie(GreenPoses.rose_1)
    rose_2 = symetrie(GreenPoses.rose_2)
    jaune_1 = symetrie(GreenPoses.jaune_1)
    jaune_2 = symetrie(GreenPoses.jaune_2)

@robot.sequence
async def print_start_zone():
    print("Start zone : " + str(robot.start_zone))

@robot.sequence
async def led_off():
    await robot.gpioSet('keyboard_led', False)

@robot.sequence
async def led_on():
    await robot.gpioSet('keyboard_led', True)