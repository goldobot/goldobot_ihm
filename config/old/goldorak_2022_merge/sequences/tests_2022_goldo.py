from asyncio import sleep
from . import robot_config as rc

from asyncio import sleep
import asyncio

import numpy as np
import math

# FIXME : DEBUG : HACK ++
def symetrie(pose):
    pose = np.array(pose, dtype=np.float64)
    if isinstance(pose, np.ndarray):
        if pose.shape[0] == 2:
            return np.array([pose[0], -pose[1]])
    return (pose[0], -pose[1], -pose[2])

def on_segment(p1, p2, d):
    p1 = np.array(p1, dtype=np.float64)
    p2 = np.array(p2, dtype=np.float64)
    diff = p2 - p1
    midpoint = (p1 + p2) * 0.5
    diff = diff/np.linalg.norm(diff)
    nr = np.array([diff[1], -diff[0]])
    return midpoint + nr * d

class Side:
    Unknown = 0
    Blue = 1
    Yellow = 2

class YellowPoses:
    start_pose = (1.0 - rc.robot_width * 0.5, -1.5 + rc.robot_back_length, 90)
    figurine_pivot = (1.5, -1.0)
    figurine_preprise = on_segment((2.0,-0.99), (1.49, -1.5), rc.robot_rotation_distance_figurine)
    figurine_prise = on_segment((2.0,-0.99), (1.49, -1.5), rc.robot_back_length)
    display = (rc.robot_rotation_distance_figurine, -1.25)
    display_pose = (rc.robot_back_length, -1.25)
    g1 = (rc.robot_rotation_distance_figurine, -0.4)
    
    g2 = (0.7, -1.05)
    g3 = (0.3,-1.0)
    
    g4 = (1.375, -0.7)
    g5 = (1.3, -0.925)
    g6 = (1.50, -1.0)
    g7 = (0.7, -0.9)
    g8 = (0.7, -1.1)
    
    g9 = (0.7, -1.1)
    
    # prise figurine
    t1 = [
        start_pose[0:2],
        (start_pose[0],-1.1),
        (1.3,-1.1),
        (1.75,-0.8),
        (1.75,-0.35),
        (1.55,-0.2),
        (1.375,-0.2),
        ]
    # prise figurine vers depose
    t2 = [
        t1[-1],
        g4,
        (1.20,-0.9),
        (0.9, -1.0),
        (0.7, -1.1),
        (0.7, -1.2)
        ]
    # depose vers 1er groupe
    t3 = [
        g2,
        (0.3,-1.0),
        (0.3,-0.4),
        (0.675,-0.3),
        ]
    #vers 2eme groupe
    t4 = [
        (0.3,-0.4),
        g5,
        (1.50, -1.0),
        on_segment((2.0,-0.99), (1.49, -1.5), rc.robot_front_length + 0.05)
        ]
        
    #start to display
    
class BluePoses:
    # start_pose = (0.8, -1.4 + robot_width * 0.5, 0)
    start_pose = symetrie(YellowPoses.start_pose)
    figurine_pivot = symetrie(YellowPoses.figurine_pivot)
    figurine_preprise = symetrie(YellowPoses.figurine_preprise)
    figurine_prise = symetrie(YellowPoses.figurine_prise)
    display = symetrie(YellowPoses.display)
    display_pose = symetrie(YellowPoses.display_pose)
    
    g1 = symetrie(YellowPoses.g1)
    g2 = symetrie(YellowPoses.g2)
    g3 = symetrie(YellowPoses.g3)
    g4 = symetrie(YellowPoses.g4)
    g5 = symetrie(YellowPoses.g5)
    g6 = symetrie(YellowPoses.g6)
    g7 = symetrie(YellowPoses.g7)
    g8 = symetrie(YellowPoses.g8)
    
    t1 = [symetrie(p) for p in YellowPoses.t1]
    t2 = [symetrie(p) for p in YellowPoses.t2]
    t3 = [symetrie(p) for p in YellowPoses.t3]
    t4 = [symetrie(p) for p in YellowPoses.t4]
# FIXME : DEBUG : HACK --
    
            

@robot.sequence
async def goldo_prematch():
    global poses
    
    if robot.side == Side.Blue:
        poses = BluePoses
    elif robot.side == Side.Yellow:
        poses = YellowPoses
    else:
        raise RuntimeError('Side not set')
        
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)    
    await propulsion.setMotorsEnable(True)    
    await propulsion.setEnable(True)
    
    await propulsion.setPose(poses.start_pose[0:2], poses.start_pose[2])
    #await propulsion.translation(0.05, 0.2)
    
    return True

@robot.sequence
async def goldo_test_async():
    task = asyncio.create_task(goldo_test_async_pompe())
    await goldo_test_traj_forward()
    await asyncio.sleep(2)
    await goldo_test_traj_back()
    await asyncio.sleep(2)
    await task

@robot.sequence
async def goldo_test_async_pompe():
    await asyncio.sleep(2)
    await goldo_enable_pompe_g()
    await asyncio.sleep(1)
    await goldo_disable_pompe_g()
    await asyncio.sleep(1)
    await goldo_enable_pompe_g()
    await asyncio.sleep(1)
    await goldo_disable_pompe_g()
    await asyncio.sleep(1)
    await goldo_enable_pompe_g()
    await asyncio.sleep(1)
    await goldo_disable_pompe_g()
    await asyncio.sleep(1)
    await goldo_enable_pompe_g()
    await asyncio.sleep(1)
    await goldo_disable_pompe_g()
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_traj_forward():
    await propulsion.moveTo((0.8725, 0.6), 0.1)

@robot.sequence
async def goldo_test_traj_back():
    await propulsion.moveTo((0.8725, 1.3), 0.1)

@robot.sequence
async def goldo_test_enable_left():
    await servos.setEnable('lift_left', True)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_enable_right():
    await servos.setEnable('lift_right', True)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_homing_left():
    await servos.setEnable('lift_left', True)
    await asyncio.sleep(1)
    await servos.liftDoHoming(0)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_homing_right():
    await servos.setEnable('lift_right', True)
    await asyncio.sleep(1)
    await servos.liftDoHoming(1)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_left_250():
    await servos.move('lift_left', 250)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_left_500():
    await servos.move('lift_left', 500)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_left_750():
    await servos.move('lift_left', 750)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_left_1000():
    await servos.move('lift_left', 1000)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_left_1250():
    await servos.move('lift_left', 1250)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_left_1500():
    await servos.move('lift_left', 1500)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_left_1750():
    await servos.move('lift_left', 1750)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_right_250():
    await servos.move('lift_right', 250)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_right_500():
    await servos.move('lift_right', 500)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_right_750():
    await servos.move('lift_right', 750)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_right_1000():
    await servos.move('lift_right', 1000)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_right_1250():
    await servos.move('lift_right', 1250)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_right_1500():
    await servos.move('lift_right', 1500)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_move_right_1750():
    await servos.move('lift_right', 1750)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_disable_left():
    await servos.setEnable('lift_left', False)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_test_disable_right():
    await servos.setEnable('lift_right', False)
    await asyncio.sleep(1)

@robot.sequence
async def goldo_enable_pompe_g():
    await robot.gpioSet('pompe_g', True)
    
@robot.sequence
async def goldo_enable_pompe_d():
    await robot.gpioSet('pompe_d', True)
    
@robot.sequence
async def goldo_disable_pompe_g():
    await robot.gpioSet('pompe_g', False)
    
@robot.sequence
async def goldo_disable_pompe_d():
    await robot.gpioSet('pompe_d', False)
    
# BACKUP OCT 2022
    
@robot.sequence
async def lift_left_disable():
    await servos.liftSetEnable(0,False)

@robot.sequence
async def lift_left_test_homing():
    await servos.liftDoHoming(0)

@robot.sequence
async def lift_test_combined_500_500():
    await servos.liftsRaw(500, 80, 500, 80)
    await asyncio.sleep(1)

@robot.sequence
async def lift_left_test_0():
    await servos.liftsRaw(0, 80, 0, 0)
    await asyncio.sleep(1)

@robot.sequence
async def lift_left_test_20():
    await servos.liftsRaw(20, 80, 0, 0)
    await asyncio.sleep(1)

@robot.sequence
async def lift_left_test_500():
    await servos.liftsRaw(500, 80, 0, 0)
    await asyncio.sleep(1)

@robot.sequence
async def lift_left_test_1000():
    await servos.liftsRaw(1000, 80, 0, 0)
    await asyncio.sleep(1)

@robot.sequence
async def lift_left_test_1500():
    await servos.liftsRaw(1500, 80, 0, 0)
    await asyncio.sleep(1)

@robot.sequence
async def lift_left_test_1800():
    await servos.liftsRaw(1800, 80, 0, 0)
    await asyncio.sleep(1)

@robot.sequence
async def lift_right_disable():
    await servos.liftSetEnable(1,False)

@robot.sequence
async def lift_right_test_homing():
    await servos.liftDoHoming(1)

@robot.sequence
async def lift_right_test_0():
    await servos.liftsRaw(0, 0, 0, 80)
    await asyncio.sleep(1)

@robot.sequence
async def lift_right_test_20():
    await servos.liftsRaw(0, 0, 20, 80)
    await asyncio.sleep(1)

@robot.sequence
async def lift_right_test_500():
    await servos.liftsRaw(0, 0, 500, 80)
    await asyncio.sleep(1)

@robot.sequence
async def lift_right_test_1000():
    await servos.liftsRaw(0, 0, 1000, 80)
    await asyncio.sleep(1)

@robot.sequence
async def lift_right_test_1500():
    await servos.liftsRaw(0, 0, 1500, 80)
    await asyncio.sleep(1)

@robot.sequence
async def lift_right_test_1800():
    await servos.liftsRaw(0, 0, 1800, 80)
    await asyncio.sleep(1)


