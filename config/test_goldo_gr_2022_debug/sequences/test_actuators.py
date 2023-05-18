import asyncio
import logging

async def test_prise_g_itw():
    await servos.moveMultiple({'herse_v' : herse.v_degagement, 'pale_g' : 190, 'pale_d' : 823})
    await servos.moveMultiple({'herse_slider' : herse.h_prise_g})
    await servos.moveMultiple({'herse_v' : herse.v_prise})
    await sleep(5)
    await servos.moveMultiple({'herse_v' : herse.v_prise_approche})
    await herse.pinces_attrape(gauche = True, droite = True)
    await servos.moveMultiple({'herse_v':herse.v_degagement})
    await servos.moveMultiple({'herse_slider' : herse.h_centre_d})

async def test_prise_g_itw():
    await servos.moveMultiple({'herse_v' : herse.v_degagement, 'pale_g' : 190, 'pale_d' : 823})
    await servos.moveMultiple({'herse_slider' : herse.h_prise_d})
    await servos.moveMultiple({'herse_v' : herse.v_prise})
    await sleep(5)
    await servos.moveMultiple({'herse_v' : herse.v_prise_approche})
    await herse.pinces_attrape(gauche = True, droite = True)
    await servos.moveMultiple({'herse_v':herse.v_degagement})
    await servos.moveMultiple({'herse_slider' : herse.h_centre_g})

async def test_depose_itw():
    await herse.depose_d()
    await herse.depose_g()

async def test_servos_commands():
    await servos.disableAll()
    await servos.setEnable('pince_droite', True)
    await servos.setEnable(['pince_droite', 'pince_gauche'], True)
    await asyncio.sleep(2)
    await servos.setEnable('bras_lat_gauche', True)
    bras_lat_gauche_sorti = 14500
    await servos.move('bras_lat_gauche', bras_lat_gauche_sorti)
    await servos.setMaxTorque(['pince_droite', 'pince_gauche'], 0.5)
    
async def test_serre_pale():
    await servos.disableAll()
    await servos.setEnable('pale_g', True)
    await servos.setMaxTorque('pale_g', 0.08)
    await servos.move('pale_g', 156)

        
async def test_lifts():
    await servos.setEnable(['lift_left', 'lift_right'], True)
    await servos.liftDoHoming(0)
    await servos.liftDoHoming(1)
    await asyncio.sleep(2)
    
async def test_lift_move():
    id_ = 'lift_right'
    await servos.setEnable(id_, True)
    await servos.move(id_, 000)
    await asyncio.sleep(1)
    await servos.move(id_, 1000)