import numpy as np
from . import robot_config as rc

def symetrie(pose):
    if isinstance(pose, np.ndarray):
        if pose.shape[0] == 2:
            return np.array([pose[0], -pose[1]])
    return (pose[0], -pose[1], -pose[2])
    

class BluePoses:    
    useless_pose = (0.955, -1.5 + rc.robot_width * 0.5 + 5e-3, 0)

    

class GreenPoses(object):
    useless_pose = symetrie(BluePoses.useless_pose)

