

@robot.sequence
async def test_recalage():
    #test recalage coin bleu
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(2,2,2,2)
    await propulsion.setPose([0.40, 1.0], -90)
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.measureNormal(-90, -1.5 + rc.robot_back_length)
    await propulsion.translation(0.20, 0.2)
    await propulsion.faceDirection(0, 0.6)
    await propulsion.reposition(-1.0, 0.2)
    await propulsion.measureNormal(0, 0 + rc.robot_back_length)
    await propulsion.translation(0.15, 0.2)
    await propulsion.moveTo(BluePoses.start_pose, 0.2)
    await propulsion.faceDirection(-90, 0.8)
    


@robot.sequence
async def test_emergency_stop():
    await propulsion.setAccelerationLimits(0.5,0.5,0.5,0.5)
    await propulsion.setPose([0,0], 0)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    await propulsion.reposition(0.2,0.1)

    task = asyncio.create_task(propulsion.translation(0.5, 0.1))
    await sleep(1)
    await propulsion.setTargetSpeed(0.3)
    await sleep(1)
    print('estop')
    await propulsion.emergencyStop()
    await task