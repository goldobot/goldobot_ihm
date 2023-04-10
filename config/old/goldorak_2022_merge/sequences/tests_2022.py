from asyncio import sleep

@robot.sequence
async def test_pompes():
    while True:
        print(robot.sensors)
        await sleep(0.2)
    await robot.gpioSet('pompe_g', True)
    await sleep(2)
    await robot.gpioSet('pompe_g', False)
    await sleep(1)
    
    print(robot.sensors['sick_bras_g'])
    await robot.gpioSet('pompe_d', True)
    await sleep(2)
    print(robot.sensors['sick_bras_g'])
    await robot.gpioSet('pompe_d', False)

@robot.sequence
async def test_lifts():
    #await servos.setEnable('lift_left', False)
    await servos.liftDoHoming(0)
    await sleep(2)
    await servos.setEnable('lift_left', True)
    await servos.move('lift_left', 1800,speed=1)
    #await servos.move('lift_left', 500)
    await servos.move('lift_left', 1,speed=0.1)
    await servos.move('lift_left', 500,speed=1)
    #await servos.move('lift_left', 1200)