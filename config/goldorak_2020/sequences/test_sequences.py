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
    #await herse.pinces_attrape(gauche=True)