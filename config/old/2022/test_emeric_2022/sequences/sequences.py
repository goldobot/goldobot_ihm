import asyncio

import numpy as np
import math

import inspect

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


class Pose:
    pass
    
class Map:
    zone_depart_x_min = 0.4
    zone_depart_x_max = 1.0

class YellowPoses:
    start_pose = (0.675, -1.235, 90)
    
    
class PurplePoses:
    start_pose = symetrie(YellowPoses.start_pose)


@robot.sequence
async def enable_servos():
    debug_goldo(__name__)

    await servos.setEnable(['servo0', 'servo1', 'servo11'], True)

@robot.sequence
async def disable_servos():
    debug_goldo(__name__)

    await servos.setEnable(['servo0', 'servo1', 'servo11'], False)

@robot.sequence
async def servo11_6000():
    debug_goldo(__name__)
    await servos.moveMultiple({'servo11': 6000}, 1)

@robot.sequence
async def servo11_8000():
    debug_goldo(__name__)
    await servos.moveMultiple({'servo11': 8000}, 1)

@robot.sequence
async def servo11_10000():
    debug_goldo(__name__)
    await servos.moveMultiple({'servo11': 10000}, 1)


@robot.sequence
async def prematch():
    global poses

    debug_goldo(__name__)

    # FIXME : DEBUG
    #if robot.side == Side.Purple:
    #    poses = PurplePoses
    #elif robot.side == Side.Yellow:
    #    poses = YellowPoses
    #else:
    #    raise RuntimeError('Side not set')
    poses = PurplePoses
        
    await enable_servos()

    await asyncio.sleep(2)

    return True

@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """
    debug_goldo(__name__)

    # FIXME : DEBUG
    #if robot.side == Side.Purple:
    #    poses = PurplePoses
    #elif robot.side == Side.Yellow:
    #    poses = YellowPoses
    #else:
    #    raise RuntimeError('Side not set')
    poses = PurplePoses
        
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    await asyncio.sleep(200)

async def end_match():
    print('end match callback')
    await robot.setScore(42)

