def symetrie(pose):
    if isinstance(pose, np.ndarray):
        if pose.shape[0] == 2:
            return np.array([pose[0], -pose[1]])
    return (pose[0], -pose[1], -pose[2])
    

class PurplePoses:    
    start_pose = (0.955, -1.5 + robot_width * 0.5 + 5e-3, 0)

    

class YellowPoses(object):
    start_pose = symetrie(BluePoses.start_pose)

