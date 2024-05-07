import numpy as np
from . import robot_config as rc


def symetrie(pose):
    if isinstance(pose, np.ndarray):
        if pose.shape[0] == 2:
            return np.array([pose[0], -pose[1]])
    return (pose[0], -pose[1], -pose[2])

class Side:
    Unknown = 0
    Yellow = 1
    Blue = 2

class YellowPoses:
    # Poses recalages jaune:
    zone1_start_pose = (1.75, -1.25, 180)
    zone3_start_pose = (0.25, -1.25, 0)
    zone5_start_pose = (1.0, 1.25, 180)
    # Poses recalages bleu:
    zone2_start_pose = (1.0, -1.25, 90)
    zone4_start_pose = (0.25, 1.25, 180)
    zone6_start_pose = (1.75, 1.25, 180)

    retour_plantes_1 = (1.6, 0.5, 180)
    retour_plantes_2 = (0.4, 0.5, 180)
    retour_plantes_3 = (0.35, 1.2, 180)
    retour_plantes = [retour_plantes_1[0:2], retour_plantes_2[0:2], retour_plantes_3[0:2]]

    prise_plantes_1 = (1.150, 0.25, -60)
    depose_plantes_1 = (1.6, 1.1, -60)

    prise_plantes_2 = (0.85, 0.2, 130)

    backup_1 = (0.95, 0.83, 180)

    prise_plantes_3 = (0.36, 0.34, -90)
    depose_plantes_3 = (0.95, -1.15, -90)

    depart_panneaux = (1.835, 0.40, -90)

    start_pose = (1.835, 1.35, -90)
    end_pose = (0.4, 1.1, 90)
    zone_fin = (0.5, 1.0, 90)

    zone_1 = [1.060, -1.4]
    zone_2 = [0.5, -0.25]
    zone_3 = [0.5, 0, 0]

    panneau_1 = (1.835, 1.40, -90)
    panneau_2 = (1.835, 1.175, -90)
    panneau_3 = (1.835, 0.95, -90)
    panneau_4 = (1.835, 0.40, -90)
    panneau_5 = (1.835, 0.175, -90)
    panneau_6 = (1.835, -0.5, -90)


class BluePoses:
    # Poses recalages jaune:
    zone1_start_pose = (1.75, -1.25, 180)
    zone3_start_pose = (0.25, -1.25, 0)
    zone5_start_pose = (1.0, 1.25, 180)
    # Poses recalages bleu:
    zone2_start_pose = (1.0, -1.25, 90)
    zone4_start_pose = (0.25, 1.25, 180)
    zone6_start_pose = (1.75, 1.25, 180)

    retour_plantes_1 = symetrie(YellowPoses.retour_plantes_1)
    retour_plantes_2 = symetrie(YellowPoses.retour_plantes_2)
    retour_plantes_3 = symetrie(YellowPoses.retour_plantes_3)
    retour_plantes = [retour_plantes_1[0:2], retour_plantes_2[0:2], retour_plantes_3[0:2]]

    prise_plantes_1 = symetrie(YellowPoses.prise_plantes_1)
    depose_plantes_1 = symetrie(YellowPoses.depose_plantes_1)

    prise_plantes_2 = symetrie(YellowPoses.prise_plantes_2)

    backup_1 = symetrie(YellowPoses.backup_1)

    prise_plantes_3 = symetrie(YellowPoses.prise_plantes_3)
    depose_plantes_3 = symetrie(YellowPoses.depose_plantes_3)
    depart_panneaux = symetrie(YellowPoses.depart_panneaux)

    start_pose = symetrie(YellowPoses.start_pose)
    end_pose = symetrie(YellowPoses.end_pose)
    zone_fin = symetrie(YellowPoses.zone_fin)

    zone_1 = [1.060, 1.4]
    zone_2 = [0.5, 0.25]
    zone_3 = [0.5, 0, 0]

    panneau_1 = symetrie(YellowPoses.panneau_1)
    panneau_2 = symetrie(YellowPoses.panneau_2)
    panneau_3 = symetrie(YellowPoses.panneau_3)
    panneau_4 = symetrie(YellowPoses.panneau_4)
    panneau_5 = symetrie(YellowPoses.panneau_5)
    panneau_6 = symetrie(YellowPoses.panneau_6)