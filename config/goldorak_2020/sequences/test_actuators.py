import asyncio
import logging

@robot.sequence
async def test_servos_commands():
    await servos.disableAll()
    await servos.setEnable('pince_droite', True)
    await servos.setEnable(['pince_droite', 'pince_gauche'], True)
    await asyncio.sleep(2)
    await servos.setEnable('bras_lat_gauche', True)
    bras_lat_gauche_sorti = 14500
    await servos.move('bras_lat_gauche', bras_lat_gauche_sorti)

        
@robot.sequence
async def test_lifts():
    await servos.setEnable(['lift_left', 'lift_right'], True)
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
