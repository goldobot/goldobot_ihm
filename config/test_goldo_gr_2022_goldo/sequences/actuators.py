import asyncio

import inspect

def debug_goldo(caller):
    print ()
    print ("************************************************")
    print (" GOLDO DEBUG :  {:32s}".format(inspect.currentframe().f_back.f_code.co_name))
    print ("************************************************")
    print ()


class GoldoLift:
    Unknown = 0
    Left = 1
    Right = 2

async def goldo_lift_move(side,pos):
    if (side==GoldoLift.Left):
        await servos.liftsRaw(pos, 80, 0, 0)
    if (side==GoldoLift.Right):
        await servos.liftsRaw(0, 0, pos, 80)

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

#arms_pos_prise_3hex = {
#    'epaule_d': 1907,
#    'epaule_g': 2222,
#    'coude_g': 460,
#    'coude_d': 560
#}

arms_pos_preprise_3hex = {
    'epaule_d': 1907,
    'epaule_g': 2222,
    'coude_g': 480,
    'coude_d': 540
}

arms_pos_prise_3hex = {
    'epaule_d': 1907,
    'epaule_g': 2222,
    'coude_g': 460,
    'coude_d': 560
}

arms_pos_serrage_3hex = {
    'epaule_d': 1734,
    'epaule_g': 2405,
}

arms_pos_depose_galerie = {
    'epaule_g': 2032,
    'epaule_d': 2034,
    'coude_g': 700,
    'coude_d': 300
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

async def prepare_depose_galerie():
    debug_goldo(__name__)

    await servos.moveMultiple(arms_pos_depose_galerie, speed=1)
    await servos.liftsRaw(450, 60, 0, 0)
    await asyncio.sleep(0.3)
    await servos.liftsRaw(0, 0, 450, 60)
    await asyncio.sleep(0.3)
    await asyncio.sleep(0.5)

@robot.sequence
async def arms_disable():
    debug_goldo(__name__)

    await servos.liftSetEnable(0,False)
    await servos.liftSetEnable(1,False)
    await servos.setEnable(['epaule_g', 'coude_g', 'epaule_d', 'coude_d', 'lift_left', 'lift_right'], False)
    await asyncio.sleep(0.5)
    
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
    
    await asyncio.sleep(3)
    
    await servos.liftsRaw(1700, 60, 0, 0)
    await asyncio.sleep(1)
    await servos.liftsRaw(0, 0, 400, 60)
    await asyncio.sleep(1)
    
    #positionement bras ferme
    await servos.moveMultiple(arms_pos_init_3, speed=0.7)
    
async def arms_prep_prise_3hex():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.moveMultiple(arms_pos_preprise_3hex, speed=1)
    await servos.liftsRaw(250, 60, 0, 0)
    await asyncio.sleep(0.3)
    await servos.liftsRaw(0, 0, 250, 60)
    await asyncio.sleep(0.3)

async def arms_serrage_3hex():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 0.8)
    await servos.liftsRaw(0, 60, 0, 0)
    await asyncio.sleep(0.3)
    await servos.liftsRaw(0, 0, 0, 60)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(arms_pos_serrage_3hex, speed=1)

async def lifts_prise_3hex():
    debug_goldo(__name__)

    sensors_retries = 0
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.liftsRaw(0,60,0,0)
    await asyncio.sleep(0.3)
    await servos.liftsRaw(0,0,0,60)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(arms_pos_prise_3hex, speed=1)
    await asyncio.sleep(0.5)
    while (sensors['sick_bras_g'] == True or sensors['sick_bras_d'] == True) and (sensors_retries < 100):
        await asyncio.sleep(0.005)
        sensors_retries = sensors_retries + 1
    await servos.moveMultiple(arms_coude_plat, speed=1)

async def arms_push_abri():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.moveMultiple(lifts_pos_prise_gnd, speed=0.6)
    await servos.moveMultiple(arms_pos_serrage_3hex, speed=1)
    
async def lifts_ejecteur():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.liftsRaw(400, 80, 0, 0)
    await asyncio.sleep(0.3)
    await servos.liftsRaw(0, 0, 400, 80)
    await asyncio.sleep(0.3)

@robot.sequence
async def lifts_top():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d'], False)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.liftsRaw(1900, 60, 1900, 60)
    await asyncio.sleep(1.0)

@robot.sequence
async def lifts_almost_top():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d'], False)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.liftsRaw(1620, 60, 1620, 60)
    await asyncio.sleep(0.3)

async def bras_ecartes():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    #await servos.liftsRaw(1680, 50, 1580, 50)
    await servos.liftsRaw(1800, 50, 1800, 50)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(arms_pos_ecartes, speed=1)
    await asyncio.sleep(0.3)

async def bras_ouverts():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.liftsRaw(1872, 50, 1872, 50)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(arms_pos_ouverts, speed=1)
    await asyncio.sleep(0.3)

async def bras_storage_front_lu_rd():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.liftsRaw(1872, 90, 400, 90)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(arms_storage_front, speed=1)
    await asyncio.sleep(0.3)

async def bras_storage_front_ld_ru():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.liftsRaw(400, 90, 1872, 90)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(arms_storage_front, speed=1)
    await asyncio.sleep(0.3)

async def prise_abri_chantier():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await start_pumps()
    await servos.liftsRaw(660, 60, 660, 60)
    await asyncio.sleep(1)

async def preprise_abri_chantier():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.moveMultiple(arms_pos_prise_abri, speed=1)
    await servos.liftsRaw(800, 60, 800, 60)
    await asyncio.sleep(1)
    
async def push_square_left_arm():
    debug_goldo(__name__)

    await servos.setEnable(['coude_g', 'epaule_g'], True)
    await servos.moveMultiple(arms_pos_left_push, speed=1)
    await servos.moveMultiple({'epaule_g': epaule_g_square}, speed=1)
    await servos.moveMultiple({'epaule_g': epaule_g_straight}, speed=1)

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
async def lift_left_disable():
    debug_goldo(__name__)

    await servos.liftSetEnable(0,False)

@robot.sequence
async def lift_left_test_homing():
    debug_goldo(__name__)

    await servos.liftDoHoming(0)

@robot.sequence
async def lift_left_test_0():
    debug_goldo(__name__)

    await servos.liftsRaw(0, 80, 0, 0)
    await asyncio.sleep(1)

@robot.sequence
async def lift_left_test_250():
    debug_goldo(__name__)

    await servos.liftsRaw(250, 80, 0, 0)
    await asyncio.sleep(1)

@robot.sequence
async def lift_left_test_500():
    debug_goldo(__name__)

    await servos.liftsRaw(500, 80, 0, 0)
    await asyncio.sleep(1)

@robot.sequence
async def lift_right_disable():
    debug_goldo(__name__)

    await servos.liftSetEnable(1,False)

@robot.sequence
async def lift_right_test_homing():
    debug_goldo(__name__)

    await servos.liftDoHoming(1)

@robot.sequence
async def lift_right_test_0():
    debug_goldo(__name__)

    await servos.liftsRaw(0, 0, 0, 80)
    await asyncio.sleep(1)

@robot.sequence
async def lift_right_test_250():
    debug_goldo(__name__)

    await servos.liftsRaw(0, 0, 250, 80)
    await asyncio.sleep(1)

@robot.sequence
async def lift_right_test_500():
    debug_goldo(__name__)

    await servos.liftsRaw(0, 0, 500, 80)
    await asyncio.sleep(1)

coude_d_retrait  = 200
coude_d_haut     = 480
coude_d_millieu  = 500
coude_d_bas      = 530

coude_g_retrait  = 820
coude_g_haut     = 540
coude_g_millieu  = 520
coude_g_bas      = 490

epaule_g_init    = 2200
epaule_d_init    = 1900

epaule_d_prise_j = 3200
epaule_g_prise_j = 900
epaule_d_prise_r = 2400
epaule_g_prise_r = 1700
#epaule_g_prise_m = 1700
epaule_g_prise_m = 1800
epaule_d_prise_m = 2300

epaule_d_depose  = 1500
#epaule_d_depose  = 1450
#epaule_g_depose  = 2700
epaule_g_depose  = 2650

arms_cake_init = {
    'coude_g': coude_g_retrait,
    'coude_d': coude_d_retrait,
    'epaule_g': epaule_g_init,
    'epaule_d': epaule_d_init
}

@robot.sequence
async def test_goldo_init_cake():
    debug_goldo(__name__)

    # initialisation ascenseurs    
    await servos.liftDoHoming(0)
    await servos.liftDoHoming(1)
    
    await asyncio.sleep(3)
    
    await servos.setEnable(['coude_g', 'coude_d', 'epaule_d', 'epaule_g'], True)
    await servos.setMaxTorque(arms_servos, 1)
    await servos.moveMultiple(arms_cake_init, speed=1)
    await asyncio.sleep(0.5)
    await servos.liftsRaw(500, 60, 0, 0)
    await asyncio.sleep(0.3)
    await servos.liftsRaw(0, 0, 500, 60)
    await asyncio.sleep(0.3)

    await servos.setEnable(['chariot_g', 'chariot_d', 'mors_d', 'mors_g', 'lift_pince'], True)


async def test_goldo_manip_tranche_gateau(tempo_s, lift, lift_pos_init, lift_pos_prise, lift_pos_transport, lift_pos_depose, epaule, epaule_init, epaule_prise, epaule_depose, coude, coude_bas, coude_haut, pompe):
    await goldo_lift_move(lift, lift_pos_transport)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({epaule: epaule_prise}, speed=1)
    await asyncio.sleep(tempo_s)
    await goldo_lift_move(lift, lift_pos_prise)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({coude: coude_bas}, speed=1)
    await asyncio.sleep(tempo_s)
    await robot.gpioSet(pompe, True)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({coude: coude_haut}, speed=1)
    await asyncio.sleep(tempo_s)
    await goldo_lift_move(lift, lift_pos_transport)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({epaule: epaule_depose}, speed=1)
    await asyncio.sleep(tempo_s)
    await goldo_lift_move(lift, lift_pos_depose)
    await asyncio.sleep(0.6)
    await robot.gpioSet(pompe, False)
    await asyncio.sleep(tempo_s)
    await goldo_lift_move(lift, lift_pos_init)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({epaule: epaule_init}, speed=1)
    await asyncio.sleep(tempo_s)

@robot.sequence
async def test_goldo_cake1():
    debug_goldo(__name__)

    tempo_s = 0.2

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Left, 500, 500, 500, 20, 'epaule_g', epaule_g_init, epaule_g_prise_m, epaule_g_depose, 'coude_g', coude_g_bas, coude_g_haut, 'pompe_g')

    tempo_s = 0.2

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Right, 500, 500, 800, 250, 'epaule_d', epaule_d_init, epaule_d_prise_j, epaule_d_depose, 'coude_d', coude_d_bas, coude_d_haut, 'pompe_d')

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Right, 500, 500, 500, 500, 'epaule_d', epaule_d_init, epaule_d_prise_r, epaule_d_depose, 'coude_d', coude_d_bas, coude_d_haut, 'pompe_d')

@robot.sequence
async def test_goldo_cake1_b():
    debug_goldo(__name__)

    tempo_s = 0.2

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Right, 500, 500, 500, 20, 'epaule_d', epaule_d_init, epaule_d_prise_m, epaule_d_depose, 'coude_d', coude_d_bas, coude_d_haut, 'pompe_d')

    tempo_s = 0.2

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Left, 500, 500, 800, 250, 'epaule_g', epaule_g_init, epaule_g_prise_j, epaule_g_depose, 'coude_g', coude_g_bas, coude_g_haut, 'pompe_g')

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Left, 500, 500, 500, 500, 'epaule_g', epaule_g_init, epaule_g_prise_r, epaule_g_depose, 'coude_g', coude_g_bas, coude_g_haut, 'pompe_g')

@robot.sequence
async def test_goldo_cake2():
    debug_goldo(__name__)

    tempo_s = 0.2

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Left, 500, 250, 500, 20, 'epaule_g', epaule_g_init, epaule_g_prise_m, epaule_g_depose, 'coude_g', coude_g_bas, coude_g_haut, 'pompe_g')

    tempo_s = 0.2

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Right, 250, 250, 800, 250, 'epaule_d', epaule_d_init, epaule_d_prise_j, epaule_d_depose, 'coude_d', coude_d_bas, coude_d_haut, 'pompe_d')

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Right, 500, 250, 500, 500, 'epaule_d', epaule_d_init, epaule_d_prise_r, epaule_d_depose, 'coude_d', coude_d_bas, coude_d_haut, 'pompe_d')

@robot.sequence
async def test_goldo_cake2_b():
    debug_goldo(__name__)

    tempo_s = 0.2

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Right, 500, 250, 500, 20, 'epaule_d', epaule_d_init, epaule_d_prise_m, epaule_d_depose, 'coude_d', coude_d_bas, coude_d_haut, 'pompe_d')

    tempo_s = 0.2

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Left, 250, 250, 800, 250, 'epaule_g', epaule_g_init, epaule_g_prise_j, epaule_g_depose, 'coude_g', coude_g_bas, coude_g_haut, 'pompe_g')

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Left, 500, 250, 500, 500, 'epaule_g', epaule_g_init, epaule_g_prise_r, epaule_g_depose, 'coude_g', coude_g_bas, coude_g_haut, 'pompe_g')

@robot.sequence
async def test_goldo_cake3():
    debug_goldo(__name__)

    tempo_s = 0.2

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Left, 500, 20, 500, 20, 'epaule_g', epaule_g_init, epaule_g_prise_m, epaule_g_depose, 'coude_g', coude_g_bas, coude_g_haut, 'pompe_g')

    tempo_s = 0.2

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Right, 250, 20, 800, 250, 'epaule_d', epaule_d_init, epaule_d_prise_j, epaule_d_depose, 'coude_d', coude_d_bas, coude_d_haut, 'pompe_d')

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Right, 500, 20, 500, 500, 'epaule_d', epaule_d_init, epaule_d_prise_r, epaule_d_depose, 'coude_d', coude_d_bas, coude_d_haut, 'pompe_d')

@robot.sequence
async def test_goldo_cake3_b():
    debug_goldo(__name__)

    tempo_s = 0.2

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Right, 500, 20, 500, 20, 'epaule_d', epaule_d_init, epaule_d_prise_m, epaule_d_depose, 'coude_d', coude_d_bas, coude_d_haut, 'pompe_d')

    tempo_s = 0.2

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Left, 250, 20, 800, 250, 'epaule_g', epaule_g_init, epaule_g_prise_j, epaule_g_depose, 'coude_g', coude_g_bas, coude_g_haut, 'pompe_g')

    await test_goldo_manip_tranche_gateau(tempo_s, GoldoLift.Left, 500, 20, 500, 500, 'epaule_g', epaule_g_init, epaule_g_prise_r, epaule_g_depose, 'coude_g', coude_g_bas, coude_g_haut, 'pompe_g')


async def test_goldo_cake_old():
    debug_goldo(__name__)

    tempo_s = 0.5

    await servos.liftsRaw(500, 80, 0, 0)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'epaule_g': epaule_g_prise_m}, speed=1)
    await asyncio.sleep(tempo_s)
    await servos.liftsRaw(500, 80, 0, 0)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'coude_g': coude_g_bas}, speed=1)
    await asyncio.sleep(tempo_s)
    await robot.gpioSet('pompe_g', True)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'coude_g': coude_g_haut}, speed=1)
    await asyncio.sleep(tempo_s)
    await servos.liftsRaw(500, 80, 0, 0)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'epaule_g': epaule_g_depose}, speed=1)
    await asyncio.sleep(tempo_s)
    await servos.liftsRaw(0, 80, 0, 0)
    await asyncio.sleep(tempo_s)
    await robot.gpioSet('pompe_g', False)
    await asyncio.sleep(tempo_s)
    await servos.liftsRaw(500, 80, 0, 0)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'epaule_g': epaule_g_init}, speed=1)
    await asyncio.sleep(tempo_s)

    await servos.liftsRaw(0, 0, 800, 80)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'epaule_d': epaule_d_prise_j}, speed=1)
    await asyncio.sleep(tempo_s)
    await servos.liftsRaw(0, 0, 500, 80)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'coude_d': coude_d_bas}, speed=1)
    await asyncio.sleep(tempo_s)
    await robot.gpioSet('pompe_d', True)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'coude_d': coude_d_haut}, speed=1)
    await asyncio.sleep(tempo_s)
    await servos.liftsRaw(0, 0, 800, 80)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'epaule_d': epaule_d_depose}, speed=1)
    await asyncio.sleep(tempo_s)
    await servos.liftsRaw(0, 0, 250, 80)
    await asyncio.sleep(tempo_s)
    await robot.gpioSet('pompe_d', False)
    await asyncio.sleep(tempo_s)
    await servos.liftsRaw(0, 0, 500, 80)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'epaule_d': epaule_d_init}, speed=1)
    await asyncio.sleep(tempo_s)

    await servos.liftsRaw(0, 0, 500, 80)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'epaule_d': epaule_d_prise_r}, speed=1)
    await asyncio.sleep(tempo_s)
    await servos.liftsRaw(0, 0, 500, 80)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'coude_d': coude_d_bas}, speed=1)
    await asyncio.sleep(tempo_s)
    await robot.gpioSet('pompe_d', True)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'coude_d': coude_d_haut}, speed=1)
    await asyncio.sleep(tempo_s)
    await servos.liftsRaw(0, 0, 500, 80)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'epaule_d': epaule_d_depose}, speed=1)
    await asyncio.sleep(tempo_s)
    await servos.liftsRaw(0, 0, 500, 80)
    await asyncio.sleep(tempo_s)
    await robot.gpioSet('pompe_d', False)
    await asyncio.sleep(tempo_s)
    await servos.liftsRaw(0, 0, 500, 80)
    await asyncio.sleep(tempo_s)
    await servos.moveMultiple({'epaule_d': epaule_d_init}, speed=1)
    await asyncio.sleep(tempo_s)

