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
    zone1_start_pose = (1.81, -1.25, 180)
    zone3_start_pose = (0.25, -1.25, 0)
    zone5_start_pose = (1.0, 1.25, 180)
    # Poses recalages bleu:
    zone2_start_pose = (1.0, -1.25, 90)
    zone4_start_pose = (0.25, 1.25, 180)
    zone6_start_pose = (1.81, 1.25, 180)

    pose_inter_panneaux = (1.81, 0.48, -90)
    pose_fin_panneaux = (1.81, -0.35, -90)
    pose_fin = zone2_start_pose
    pose_retour_panneaux = (1.4, -0.33, 90)
    pose_retour_panneaux2 = (1.7, 0.43, 90)
    pose_retour_panneaux3 = (1.7, 1.2, 90)
    pose_no_panneaux = (1.07, 1.19, 90)

    # FIXME : DEBUG
    #debut_prise_1 = (1.7, 0.5, 180)
    debut_prise_1 = (1.7, 0.505, 180)
    fin_prise_1 = (1.33, 0.5, 180)
    inter_prise_1 = (1.53, 0.5, 180)
    inter2_prise_1 = (1.43, 0.5, 180)

    debut_prise_2 = (0.86, 0.5, 0)
    fin_prise_2 = (0.75, 0.5, 0)
    inter_prise_2 = (0.65, 0.5, 0)
    inter2_prise_2 = (0.65, 0.5, 0)

    # FIXME : DEBUG : GOLDO
    #pose_inter_depose1 = (0.59, 1.14, 180)
    pose_inter_depose1 = (0.62, 1.14, -90)
    pose_inter_depose1_avance = (0.62, 0.96, -90)

    depose1 = (0.2, 0.70, 0)

    # FIXME : DEBUG : GOLDO
    #predepose2 = (0.3, 1.29, 0)
    #predepose2_deg = (0.800, 1.29, 0)
    predepose2 = (0.3, 1.28, 0)
    predepose2_deg = (0.800, 1.28, 0)
    # FIXME : DEBUG : GOLDO
    #depose2 = (0.6, 1.2, 0)
    depose2 = (0.61, 1.2, 0)
    orientation_depose2 = (0.6, 1.0, 0)

    pose_inter_fin = (1.6, 0.4, -90)
    pose_alternative_fin = (0.6, 1.1, 0)
    zone_inter_fin = (0.5, 1.0, 90)
    depose_fin = (0.25, 1.10, 90)

    pose_spline_traversee_1 = (0.7, 0.7, 90)
    pose_spline_traversee_2 = (0.5, 0.15, 90)
    pose_spline_traversee_3 = (0.7, -0.35, 90)
    pose_spline_traversee_4 = (1.0, -1.2, 90)



class BluePoses:
    # Poses recalages jaune:
    zone1_start_pose = (1.81, -1.25, 180)
    zone3_start_pose = (0.25, -1.25, 0)
    zone5_start_pose = (1.0, 1.25, 180)
    # Poses recalages bleu:
    zone2_start_pose = (1.0, -1.25, 90)
    zone4_start_pose = (0.25, 1.25, 180)
    zone6_start_pose = (1.81, 1.25, 180)

    pose_inter_panneaux = (1.81, -0.5, -90)
    pose_fin_panneaux = (1.81, 0.35, -90)
    pose_fin = zone5_start_pose
    pose_retour_panneaux = symetrie(YellowPoses.pose_retour_panneaux)
    pose_retour_panneaux2 = symetrie(YellowPoses.pose_retour_panneaux2)
    pose_retour_panneaux3 = symetrie(YellowPoses.pose_retour_panneaux3)
    pose_no_panneaux = symetrie(YellowPoses.pose_no_panneaux)

    debut_prise_1 = symetrie(YellowPoses.debut_prise_1)
    fin_prise_1 = symetrie(YellowPoses.fin_prise_1)
    inter_prise_1 = symetrie(YellowPoses.inter_prise_1)
    inter2_prise_1 = symetrie(YellowPoses.inter2_prise_1)

    debut_prise_2 = symetrie(YellowPoses.debut_prise_2)
    fin_prise_2 = symetrie(YellowPoses.fin_prise_2)
    inter_prise_2 = symetrie(YellowPoses.inter_prise_2)
    inter2_prise_2 = symetrie(YellowPoses.inter2_prise_2)

    pose_inter_depose1 = symetrie(YellowPoses.pose_inter_depose1)
    depose1 = symetrie(YellowPoses.depose1)

    predepose2 = symetrie(YellowPoses.predepose2)
    predepose2_deg = symetrie(YellowPoses.predepose2_deg)
    depose2 = symetrie(YellowPoses.depose2)
    orientation_depose2 = symetrie(YellowPoses.orientation_depose2)

    pose_inter_fin = symetrie(YellowPoses.pose_inter_fin)
    pose_alternative_fin = zone2_start_pose

    zone_inter_fin = symetrie(YellowPoses.zone_inter_fin)
    depose_fin = symetrie(YellowPoses.depose_fin)

    pose_spline_traversee_1 = symetrie(YellowPoses.pose_spline_traversee_1)
    pose_spline_traversee_2 = symetrie(YellowPoses.pose_spline_traversee_2)
    pose_spline_traversee_3 = symetrie(YellowPoses.pose_spline_traversee_3)
    pose_spline_traversee_4 = symetrie(YellowPoses.pose_spline_traversee_4)
