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
    plat_start_pose = (0.24, 0.8, 0)
    plat_inter_pose = (0.24, 0.7, 0)
    assiette_start_pose = (2.8, -0.7, 180)
    zone_fin = (2.6, 0.3, 0)

    # Poses depart plat
    prise_marron = (1.03, 0.285, 30)
    depose_marron = (0.640, 0.370, -135)
    pose_construction = (0.850-rc.robot_back_length,  0.523, 180)
    

    # Poses gateaux finis
    pose_gateau_1 = (0.2, 0.523, 180)
    pose_gateau_2 = (0.35, 0.523, 180)
    pose_gateau_3 = (0.5, 0.523, 180)

    # Gateaux marrons
    marron_assiette_1 = (1.125, -0.275, -90)
    marron_assiette_2 = (1.875, 0.275, 90)
    assiette_1 = (1.100, -0.7, -90)
    assiette_2 = (1.900, 0.7, 90)


class BluePoses:
    plat_start_pose = symetrie(GreenPoses.plat_start_pose)
    plat_inter_pose = symetrie(GreenPoses.plat_inter_pose)
    assiette_start_pose = symetrie(GreenPoses.assiette_start_pose)
    zone_fin = symetrie(GreenPoses.zone_fin)

    # Poses depart plat
    prise_marron = symetrie(GreenPoses.prise_marron)
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
    assiette_2 = symetrie(GreenPoses.assiette_2)
