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
    
