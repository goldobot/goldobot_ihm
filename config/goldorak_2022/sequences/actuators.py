import asyncio

#epaule_g
#coude_g

arms_pos_init_1 = {
    'coude_g': 816,
    'coude_d': 218
}

arms_pos_init_2 = {
    'epaule_g': 2032,
    'epaule_d': 2034
}

arms_pos_init_3 = {
    'epaule_g': 3316,
    'epaule_d': 766
}

arms_coude_plat  = {
    'coude_g': 511,
    'coude_d': 511
}

arms_lifts_init_3 = {
    'lift_left': 1800,
    'lift_right': 500
}

arms_pos_prise_3hex = {
    'epaule_d': 1907,
    'epaule_g': 2222,
    'coude_g': 490,
    'coude_d': 530
}

arms_pos_prise_abri = {
    'epaule_g': 2032,
    'epaule_d': 2034,
    'coude_g': 511,
    'coude_d': 511
}

arms_pos_serrage_3hex = {
    'epaule_d': 1754,
    'epaule_g': 2385,
}

arms_pos_ecartes = {
    'epaule_d': 2924,
    'epaule_g': 1100,
    'coude_g': 816,
    'coude_d': 218
}

lifts_pos_prise_3hex = {
    'lift_left': 300,
    'lift_right': 300,
}

lifts_pos_leve_3hex = {
    'lift_left': 20,
    'lift_right': 20,
}

lifts_pos_prise_gnd = {
    'lift_left': 0,
    'lift_right': 0,
}

lifts_pos_ejecteur = {
    'lift_left': 300,
    'lift_right': 300,
}

lifts_pos_top = {
    'lift_left': 1800,
    'lift_right': 1800,
}

lifts_pos_prise_abri = {
    'lift_left': 1200,
    'lift_right': 1200,
}

arms_servos = ['epaule_g', 'epaule_d', 'coude_g', 'coude_d']

@robot.sequence
async def arms_disable():
    await servos.setEnable(['epaule_g', 'coude_g', 'epaule_d', 'coude_d', 'lift_left', 'lift_right'], False)
    
@robot.sequence
async def arms_initialize():
    # en 1er monter les coudes
    await servos.setMaxTorque(['epaule_g', 'epaule_d'], 0.30)
    await servos.setMaxTorque(['coude_g', 'coude_d'], 0.20)
    
    await servos.setEnable(['epaule_g', 'epaule_d'], False)
    await servos.setEnable(['coude_g', 'coude_d'], True)
    
    await servos.moveMultiple(arms_pos_init_1, speed=0.7)
    await asyncio.sleep(0.2)
    
    # puis les epaules
    await servos.setEnable(['epaule_g', 'epaule_d'], True)
    await servos.moveMultiple(arms_pos_init_2, speed=0.7)
    
    await asyncio.sleep(0.2)
    
    await servos.setMaxTorque(arms_servos, 0.5)
    await servos.moveMultiple(arms_coude_plat, speed=0.7)
    
    await asyncio.sleep(0.2)
    
    # initialisation ascenceurs    
    await servos.liftDoHoming(0)
    await servos.liftDoHoming(1)
    
    await asyncio.sleep(1)
    
    await servos.moveMultiple(arms_lifts_init_3, speed=0.8)
    await asyncio.sleep(0.5)
    
    #positionement bras ferme
    
    await servos.moveMultiple(arms_pos_init_3, speed=0.7)
    
@robot.sequence
async def arms_prep_prise_3hex():
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.moveMultiple(arms_pos_prise_3hex, speed=1)
    await servos.moveMultiple(lifts_pos_prise_3hex, speed=1)

@robot.sequence
async def arms_serrage_3hex():
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 0.8)
    #await servos.moveMultiple(lifts_pos_leve_3hex, speed=1)
    await servos.moveMultiple(arms_pos_serrage_3hex, speed=1)

@robot.sequence
async def lifts_prise_3hex():
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.moveMultiple(lifts_pos_prise_gnd, speed=1)
    await servos.moveMultiple(arms_pos_prise_3hex, speed=1)
    while sensors['sick_bras_g'] == True and sensors['sick_bras_d'] == True:
        await asyncio.sleep(0.005)
    await servos.moveMultiple(arms_coude_plat, speed=1)
    
@robot.sequence
async def lifts_ejecteur():
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.moveMultiple(lifts_pos_ejecteur, speed=1)
    await asyncio.sleep(0.1)

@robot.sequence
async def lifts_top():
    await servos.setEnable(['coude_g', 'coude_d'], False)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.moveMultiple(arms_pos_ecartes, speed=1)
    await asyncio.sleep(0.1)

@robot.sequence
async def bras_ecartes():
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.moveMultiple(lifts_pos_top, speed=1)
    await servos.moveMultiple(arms_pos_ecartes, speed=1)
    await asyncio.sleep(0.3)

@robot.sequence
async def prise_abri_chantier():
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.moveMultiple(arms_pos_prise_abri, speed=1)
    await start_pumps()
    await servos.moveMultiple(lifts_pos_prise_abri, speed=1)
    await asyncio.sleep(0.3)

@robot.sequence
async def start_pumps():
    await robot.gpioSet('pompe_g', True)
    await robot.gpioSet('pompe_d', True)


@robot.sequence
async def stop_pumps():
    await robot.gpioSet('pompe_g', False)
    await robot.gpioSet('pompe_d', False)