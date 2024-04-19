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

class BluePoses:
    # Poses recalages jaune:
    zone1_start_pose = (1.75, -1.25, 180)
    zone3_start_pose = (0.25, -1.25, 0)
    zone5_start_pose = (1.0, 1.25, 180)
    # Poses recalages bleu:
    zone2_start_pose = (1.0, -1.25, 90)
    zone4_start_pose = (0.25, 1.25, 180)
    zone6_start_pose = (1.75, 1.25, 180)