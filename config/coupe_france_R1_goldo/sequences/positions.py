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


    plat_start_pose = (0.2, 0.8, 0)
    plat_inter_pose = (0.2, 0.7, 0)
    assiette_start_pose = (2.8, -0.7, 180)
    zone_presque_fin = (2.35, 0.3, 0)
    zone_fin = (2.50, 0.3, 0)
    zone_fin_au_fond = (2.85, 0.3, 0)

    # Poses depart plat
    #prise_marron = (1.03, 0.285, 30)
    prise_marron = (1.04, 0.283, 30)
    prise_marron_alt = (1.125, -0.290, 90)
    #depose_marron = (0.644, 0.370, -135)
    #depose_marron = (0.660, 0.385, -135)
    depose_marron = (0.648, 0.390, -135)
    pose_construction = (0.850-rc.robot_back_length, 0.527, 180)

    # Pose tir cerises:
    tir_cerises = (0.480, 0.80, 90)
    
    # Poses gateaux finis
    pose_gateau_1 = (0.20, 0.523, 180)
    pose_gateau_2 = (0.32, 0.523, 180)
    pose_gateau_3 = (0.44, 0.523, 180)

    # Gateaux monocouleur
    marron_assiette_1 = (1.125, -0.275, -90)
    assiette_1 = (1.125, -0.67, -90)
    prise_j1 = (0.805, -0.700, -90)
    depose_j_1 = (1.0, -0.60, -90)
    prise_r1 = (0.575, -0.700, -90)
    depose_r_1 = (0.850, -0.60, -90)

    marron_assiette_2 = (1.875, 0.275, 90)
    assiette_2 = (1.875, 0.67, 90)

    marron_assiette_3 = (1.875, -0.275, -90)
    assiette_3 = (1.760, 0.6, 90)
    #assiette_3 = (1.280, -0.6, 90)
    
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

    # Pose tir cerises:
    tir_cerises = (0.480, -0.8, -90)

    plat_start_pose = symetrie(GreenPoses.plat_start_pose)
    plat_inter_pose = symetrie(GreenPoses.plat_inter_pose)
    assiette_start_pose = symetrie(GreenPoses.assiette_start_pose)
    zone_presque_fin = symetrie(GreenPoses.zone_presque_fin)
    zone_fin = symetrie(GreenPoses.zone_fin)
    zone_fin_au_fond = symetrie(GreenPoses.zone_fin_au_fond)

    # Poses depart plat
    prise_marron = symetrie(GreenPoses.prise_marron)
    prise_marron_alt = symetrie(GreenPoses.prise_marron_alt)
    depose_marron = symetrie(GreenPoses.depose_marron)
    pose_construction = symetrie(GreenPoses.pose_construction)

    # Poses gateaux finis
    pose_gateau_1 = symetrie(GreenPoses.pose_gateau_1)
    pose_gateau_2 = symetrie(GreenPoses.pose_gateau_2)
    pose_gateau_3 = symetrie(GreenPoses.pose_gateau_3)

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
