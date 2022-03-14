from .herse import herse
import asyncio



async def check_sensors():
    while True:
        if sensors['gache_d'] == False:
            await asyncio.shield(herse.pinces_attrape(droite = True))
            return
        await asyncio.sleep(.05)
            
@robot.sequence
async def test_herse_pinces_attrape():
    await servos.setEnable('pince_droite', True)
    await servos.setEnable('pince_gauche', True)
    
    await herse.pinces(droite='ouvert')
    await asyncio.sleep(1)
        
    task = asyncio.create_task(check_sensors())
    await task
    print('finished')
    return
    await herse.initialize()
     
    await herse.pinces(both='ouvert')
    await asyncio.sleep(5)
    
@robot.sequence
async def test_reposition():
    await propulsion.setAccelerationLimits(0.5,0.5,0.5,0.5)
    await propulsion.setPose([0,0], 0)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    await propulsion.reposition(0.2,0.5)
    await propulsion.transformPose((0,0), 90)
    
@robot.sequence
async def test_reposition_after_trajectory():
    await propulsion.setAccelerationLimits(0.5,0.5,0.5,0.5)
    await propulsion.setPose([0,0], 0)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    await propulsion.trajectorySpline([(0,0), (0.5,0), (0.5,0.5)], speed=0.5,  reposition_speed=0.2,reposition_distance=0.5)