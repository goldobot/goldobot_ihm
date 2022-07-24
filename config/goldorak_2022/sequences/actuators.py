import asyncio

import inspect

def debug_goldo(caller):
    print ()
    print ("************************************************")
    print (" GOLDO DEBUG :  {:32s}".format(inspect.currentframe().f_back.f_code.co_name))
    print ("************************************************")
    print ()

#epaule_g
#coude_g

epaule_g_square = 1510
epaule_g_straight = 2032
epaule_d_square = 2633
epaule_d_straight = 2034

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

arms_storage_front = {
    'coude_g': 511,
    'coude_d': 511,
    'epaule_g': 3164,
    'epaule_d': 913
}

arms_lifts_init_3 = {
    'lift_left': 1900,
    'lift_right': 400
}

#arms_pos_prise_3hex = {
#    'epaule_d': 1907,
#    'epaule_g': 2222,
#    'coude_g': 490,
#    'coude_d': 530
#}

arms_pos_prise_3hex = {
    'epaule_d': 1907,
    'epaule_g': 2222,
    'coude_g': 460,
    'coude_d': 560
}

arms_pos_preprise_3hex = {
    'epaule_d': 1907,
    'epaule_g': 2222,
    'coude_g': 480,
    'coude_d': 540
}

arms_pos_prise_abri = {
    'epaule_g': 2032,
    'epaule_d': 2034,
    'coude_g': 511,
    'coude_d': 511
}

#arms_pos_serrage_3hex = {
#    'epaule_d': 1754,
#    'epaule_g': 2385,
#}

arms_pos_serrage_3hex = {
    'epaule_d': 1734,
    'epaule_g': 2405,
}

arms_pos_ecartes = {
    'epaule_d': 2924,
    'epaule_g': 1100,
    'coude_g': 816,
    'coude_d': 218
}

arms_pos_ouverts = {
    'epaule_d': 2924,
    'epaule_g': 1100,
    'coude_g': 600,
    'coude_d': 400
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

#lifts_pos_top = {
#    'lift_left': 1800,
#    'lift_right': 1800,
#}

lifts_pos_top = {
    'lift_left': 1872,
    'lift_right': 1872,
}

lifts_pos_under_top = {
    'lift_left': 1500,
    'lift_right': 1500,
}

lifts_pos_prise_abri = {
    'lift_left': 700,
    'lift_right': 700,
}

lifts_storage_front_ld_ru = {
    'lift_left': 400,
    'lift_right': 1900
}

lifts_storage_front_lu_rd = {
    'lift_left': 1900,
    'lift_right': 400
}

arms_pos_left_push = {
    'lift_left': 1700,
    'coude_g': 380
}

arms_pos_right_push = {
    'lift_right': 1700,
    'coude_d': 645
}

arms_servos = ['epaule_g', 'epaule_d', 'coude_g', 'coude_d']

@robot.sequence
async def arms_disable():
    debug_goldo(__name__)

    await servos.setEnable(['epaule_g', 'coude_g', 'epaule_d', 'coude_d', 'lift_left', 'lift_right'], False)
    
@robot.sequence
async def arms_initialize():
    debug_goldo(__name__)

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
    
    # FIXME : TODO : remove
    #await servos.moveMultiple(arms_lifts_init_3, speed=0.8)
    await servos.liftsRaw(1872, 60, 0, 0)
    await asyncio.sleep(1)
    await servos.liftsRaw(0, 00, 400, 60)
    await asyncio.sleep(1)
    
    #positionement bras ferme
    await servos.moveMultiple(arms_pos_init_3, speed=0.7)
    
@robot.sequence
async def arms_prep_prise_3hex():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    # FIXME : TODO : remove
    #await servos.moveMultiple(arms_pos_prise_3hex, speed=1)
    #await servos.moveMultiple(lifts_pos_prise_3hex, speed=1)
    await servos.moveMultiple(arms_pos_preprise_3hex, speed=1)
    # FIXME : TODO : fix
    #await servos.liftsRaw(150, 60, 150, 60)
    await servos.liftsRaw(250, 60, 0, 0)
    await servos.liftsRaw(0, 0, 250, 60)

@robot.sequence
async def arms_serrage_3hex():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 0.8)
    # FIXME : TODO : remove
    #await servos.moveMultiple(lifts_pos_leve_3hex, speed=1)
    await servos.liftsRaw(0, 60, 0, 60)
    await servos.moveMultiple(arms_pos_serrage_3hex, speed=1)

@robot.sequence
async def lifts_prise_3hex():
    debug_goldo(__name__)

    sensors_retries = 0
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    # FIXME : TODO : remove
    #await servos.moveMultiple(lifts_pos_prise_gnd, speed=1)
    # FIXME : TODO : fix
    #await servos.liftsRaw(10,60,10,60)
    await servos.liftsRaw(10,60,0,0)
    await servos.liftsRaw(0,0,10,60)
    await servos.moveMultiple(arms_pos_prise_3hex, speed=1)
    while (sensors['sick_bras_g'] == True or sensors['sick_bras_d'] == True) and (sensors_retries < 100):
        await asyncio.sleep(0.005)
        sensors_retries = sensors_retries + 1
    await servos.moveMultiple(arms_coude_plat, speed=1)

@robot.sequence
async def arms_push_abri():
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.moveMultiple(lifts_pos_prise_gnd, speed=0.6)
    await servos.moveMultiple(arms_pos_serrage_3hex, speed=1)
    
@robot.sequence
async def lifts_ejecteur():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    # FIXME : TODO : remove
    #await servos.moveMultiple(lifts_pos_ejecteur, speed=1)
    # FIXME : TODO : fix
    #await servos.liftsRaw(300, 60, 300, 60)
    await servos.liftsRaw(300, 60, 0, 0)
    await servos.liftsRaw(0, 0, 300, 60)
    await asyncio.sleep(0.1)

@robot.sequence
async def lifts_top():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d'], False)
    await servos.setMaxTorque(arms_servos, 1)
    # FIXME : TODO : remove
    #await servos.moveMultiple(lifts_pos_top, speed=1)
    await servos.liftsRaw(1872, 60, 1872, 60)
    await asyncio.sleep(0.1)

@robot.sequence
async def lifts_almost_top():
    await servos.setEnable(['coude_g', 'coude_d'], False)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.liftsRaw(1620, 60, 1620, 60)
    await asyncio.sleep(0.1)

@robot.sequence
async def bras_ecartes():
    debug_goldo(__name__)

    # FIXME : TODO : remove
    #await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    #await servos.setMaxTorque(arms_servos, 1)
    #await servos.moveMultiple(lifts_pos_top, speed=1)
    #await servos.moveMultiple(arms_pos_ecartes, speed=1)
    #await asyncio.sleep(0.3)
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    # FIXME : TODO : remove
    #await servos.moveMultiple(lifts_pos_under_top, speed=0.5)
    await servos.liftsRaw(1500, 50, 1500, 50)
    await servos.moveMultiple(arms_pos_ecartes, speed=1)
    await asyncio.sleep(0.3)

@robot.sequence
async def bras_ouverts():
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    # FIXME : TODO : remove
    #await servos.moveMultiple(lifts_pos_top, speed=0.5)
    await servos.liftsRaw(1872, 50, 1872, 50)
    await servos.moveMultiple(arms_pos_ouverts, speed=1)
    await asyncio.sleep(0.3)

@robot.sequence
async def bras_storage_front_lu_rd():
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    # FIXME : TODO : remove
    #await servos.moveMultiple(lifts_storage_front_lu_rd, speed=1)
    await servos.liftsRaw(1872, 90, 400, 90)
    await servos.moveMultiple(arms_storage_front, speed=1)
    await asyncio.sleep(0.3)

@robot.sequence
async def bras_storage_front_ld_ru():
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    # FIXME : TODO : remove
    #await servos.moveMultiple(lifts_storage_front_ld_ru, speed=1)
    await servos.liftsRaw(400, 90, 1872, 90)
    await servos.moveMultiple(arms_storage_front, speed=1)
    await asyncio.sleep(0.3)

@robot.sequence
async def prise_abri_chantier():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await start_pumps()
    # FIXME : TODO : remove
    #await servos.moveMultiple(lifts_pos_prise_abri, speed=1)
    #await asyncio.sleep(0.5)
    await servos.liftsRaw(660, 60, 660, 60)
    await asyncio.sleep(1)

@robot.sequence
async def preprise_abri_chantier():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.moveMultiple(arms_pos_prise_abri, speed=1)
    await servos.liftsRaw(800, 60, 800, 60)
    await asyncio.sleep(1)
    
@robot.sequence
async def push_square_left_arm():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'epaule_g'], True)
    await servos.moveMultiple(arms_pos_left_push, speed=1)
    await servos.moveMultiple({'epaule_g': epaule_g_square}, speed=1)
    await servos.moveMultiple({'epaule_g': epaule_g_straight}, speed=1)

@robot.sequence
async def push_square_right_arm():
    debug_goldo(__name__)

    await servos.setEnable(['coude_d', 'epaule_d'], True)
    await servos.moveMultiple(arms_pos_right_push, speed=1)
    await servos.moveMultiple({'epaule_d': epaule_d_square}, speed=1)
    await servos.moveMultiple({'epaule_d': epaule_d_straight}, speed=1)


@robot.sequence
async def start_pumps():
    debug_goldo(__name__)

    await robot.gpioSet('pompe_g', True)
    await robot.gpioSet('pompe_d', True)

@robot.sequence
async def stop_pumps():
    debug_goldo(__name__)

    await robot.gpioSet('pompe_g', False)
    await robot.gpioSet('pompe_d', False)

@robot.sequence
async def lift_left_test_homing():
    await servos.liftDoHoming(0)

@robot.sequence
async def lift_test_combined_500_500():
    await servos.liftsRaw(500, 80, 500, 80)
    await asyncio.sleep(1)

@robot.sequence
async def lift_left_test_0():
    await servos.liftsRaw(0, 80, 0, 0)
    await asyncio.sleep(1)

@robot.sequence
async def lift_left_test_500():
    await servos.liftsRaw(500, 80, 0, 0)
    await asyncio.sleep(1)

@robot.sequence
async def lift_left_test_1000():
    await servos.liftsRaw(1000, 80, 0, 0)
    await asyncio.sleep(1)

@robot.sequence
async def lift_right_test_homing():
    await servos.liftDoHoming(1)

@robot.sequence
async def lift_right_test_0():
    await servos.liftsRaw(0, 0, 0, 80)
    await asyncio.sleep(1)

@robot.sequence
async def lift_right_test_500():
    await servos.liftsRaw(0, 0, 500, 80)
    await asyncio.sleep(1)

@robot.sequence
async def lift_right_test_1000():
    await servos.liftsRaw(0, 0, 1000, 80)
    await asyncio.sleep(1)

