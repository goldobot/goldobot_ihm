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
    
    await servos.moveMultiple(arms_pos_init_1, speed=0.3)
    await asyncio.sleep(2)
    
    # puis les epaules
    await servos.setEnable(['epaule_g', 'epaule_d'], True)
    await servos.moveMultiple(arms_pos_init_2, speed=0.3)
    
    await asyncio.sleep(1)
    
    await servos.setMaxTorque(arms_servos, 0.5)
    await servos.moveMultiple(arms_coude_plat, speed=0.5)
    
    await asyncio.sleep(1)
    
    # initialisation ascenceurs    
    await servos.liftDoHoming(0)
    await servos.liftDoHoming(1)
    
    await asyncio.sleep(1)
    
    await servos.moveMultiple(arms_lifts_init_3, speed=0.3)
    await asyncio.sleep(1)
    
    #positionement bras ferme
    
    await servos.moveMultiple(arms_pos_init_3, speed=0.3)
    
    

    
    
    


    

    
    
    
    
