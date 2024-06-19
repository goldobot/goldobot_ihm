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

    zone_fin = zone2_start_pose

    # Changement de zone
    traj_change_zone_coin = (1.68, 0.32, -90)
    traj_change_zone_milieu = (1.0, 0.0, -90)
    traj_change_zone_bout = zone2_start_pose

    pose_depart_panneaux = (1.81, 1.25, 90)
    pose_inter_panneaux = (1.81, 0.48, -90)
    pose_fin_panneaux = (1.81, -0.35, -90)
    pose_fin = zone2_start_pose
    pose_retour_panneaux = (1.4, -0.33, 90)
    pose_retour_panneaux2 = (1.7, 0.43, 90)
    pose_retour_panneaux3 = (1.7, 1.2, 90)
    pose_no_panneaux = (1.07, 1.19, 90)

    debut_prise_1 = (1.69, 0.5, 180)
    fin_prise_1 = (1.35, 0.5, 180)
    inter_prise_1 = (1.51, 0.5, 180)
    inter2_prise_1 = (1.427, 0.5, 180)

    debut_prise_2 = (0.91, 0.5, 0)
    fin_prise_2 = (0.67, 0.5, 0)
    inter_prise_2 = (0.814, 0.5, 0)

    pose_inter_depose1 = (0.615, 1.145, -90)
    pose_inter_depose1_avance = (0.615, 0.96, -90)
    depose1 = (0.2, 0.70, 0)

    prise_pots_2 = (2-0.615, 1.148, -90)
    depose_zone_protegee = (0.36, 0.75, 0)
                            
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



class BluePoses:
    # Poses recalages jaune:
    zone1_start_pose = (1.81, -1.25, 180)
    zone3_start_pose = (0.25, -1.25, 0)
    zone5_start_pose = (1.0, 1.25, 180)
    # Poses recalages bleu:
    zone2_start_pose = (1.0, -1.25, 90)
    zone4_start_pose = (0.25, 1.25, 180)
    zone6_start_pose = (1.81, 1.25, 180)

    zone_fin = zone5_start_pose

    # Changement de zone
    traj_change_zone_coin = symetrie(YellowPoses.traj_change_zone_coin)
    traj_change_zone_milieu = symetrie(YellowPoses.traj_change_zone_milieu)
    traj_change_zone_bout = zone5_start_pose


    pose_depart_panneaux = symetrie(YellowPoses.pose_depart_panneaux)
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

    pose_inter_depose1 = symetrie(YellowPoses.pose_inter_depose1)
    pose_inter_depose1_avance = symetrie(YellowPoses.pose_inter_depose1_avance)
    depose1 = symetrie(YellowPoses.depose1)

    prise_pots_2 = symetrie(YellowPoses.prise_pots_2)
    depose_zone_protegee = symetrie(YellowPoses.depose_zone_protegee)
    
    predepose2 = symetrie(YellowPoses.predepose2)
    predepose2_deg = symetrie(YellowPoses.predepose2_deg)
    depose2 = symetrie(YellowPoses.depose2)
    orientation_depose2 = symetrie(YellowPoses.orientation_depose2)

    pose_inter_fin = symetrie(YellowPoses.pose_inter_fin)
    pose_alternative_fin = zone2_start_pose

    zone_inter_fin = symetrie(YellowPoses.zone_inter_fin)
    depose_fin = symetrie(YellowPoses.depose_fin)
