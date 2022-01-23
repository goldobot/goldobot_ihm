import asyncio

@robot.sequence
async def test_lifts():
    await servos.liftDoHoming(0)
    await servos.liftDoHoming(1)
    await asyncio.sleep(2)
    
@robot.sequence
async def test_lift_move():
    id_ = 'lift_right'
    await servos.setEnable(id_, True)
    await servos.move(id_, 000)
    await asyncio.sleep(1)
    await servos.move(id_, 1000)
