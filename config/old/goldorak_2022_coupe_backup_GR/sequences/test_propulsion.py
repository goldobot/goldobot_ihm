import asyncio

@robot.sequence
async def test_propulsion_reposition_and_shock():
    await propulsion.setAccelerationLimits(2.0, 2.0, 0.5, 0.5)
    await propulsion.setPose([0,0], 0)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    await propulsion.reposition(-0.2,0.1)
    await propulsion.translation(0.4, 0.5)
    await asyncio.sleep(1)
    await propulsion.translation(-0.6, 0.7)
    
    await propulsion.setMotorsEnable(False)
    await propulsion.setEnable(False)
    
@robot.sequence
async def test_propulsion_mine():
    await propulsion.setAccelerationLimits(2.0, 2.0, 0.5, 0.5)
    await propulsion.setPose([0,0], 0)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    try:
        await propulsion.translation(-0.6, 0.7)
    finally:    
        await propulsion.setMotorsEnable(False)
        await propulsion.setEnable(False)
        
@robot.sequence
async def test_propulsion_rotation():
    await propulsion.setAccelerationLimits(2.0, 2.0, 2.0, 2.0)
    await propulsion.setPose([0,0], 0)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    try:
        await propulsion.rotation(90, 0.7)
    finally:    
        await propulsion.setMotorsEnable(False)
        await propulsion.setEnable(False)