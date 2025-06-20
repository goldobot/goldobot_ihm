import asyncio

from . import actuators_pneuma

pose_asc_down = 4095
pose_asc_soulage = 3800
#pose_asc_soulage = 3700
pose_asc_transport = 3504
pose_asc_standby = 2800
pose_asc_stage2_high = 450
pose_asc_stage2_depose = 1600
pose_asc_stage2_low = 622
pose_asc_up = 0
pose_asc_up_high = 0

pose_soulageur_down = 206
pose_soulageur_mid = 380
pose_soulageur_up = 530
pose_soulageur_transport = 560

pose_bras_up = 660
pose_bras_transport = 402
pose_bras_prise = 382
pose_bras_prise_hard = 360
pose_bras_standby = 445

global_long_speed = 0.60
global_turn_speed = 3.2
global_turn_speed_slow = 1.5

global_pneuma_timeout = 1.6


####################
# MACRO-SEQUENCES  #
####################

@robot.sequence
async def prise_arr():
    global global_turn_speed
    global global_long_speed

    short_timeout = 0.1
    long_timeout = 0.3

    # approche
    await bras_arr_standby()
    await ventouses_arr_ext_attrape()
    await ventouses_arr_int_attrape()
    await asyncio.sleep(short_timeout)
    await ascenseur_arr_down()
    await asyncio.sleep(short_timeout)
    await propulsion.translation(-0.15, 0.2)
    await asyncio.sleep(short_timeout)

    # verrouillage planches
    await soulageur_arr_up()
    await asyncio.sleep(short_timeout)
    await bras_arr_prise_hard()
    await asyncio.sleep(short_timeout)
    await pump_arr_on()
    await asyncio.sleep(short_timeout)
    await bras_arr_transport()
    await asyncio.sleep(short_timeout)
    await soulageur_arr_transport()
    await asyncio.sleep(short_timeout)

    # wooble..
    # FIXME : TODO
    #await ascenseur_arr_soulage()
    #await asyncio.sleep(short_timeout)
    ## FIXME : TODO : get behaviour from 'preprise_pos' object..
    #if preprise_pos in [-50,-40,40,50]:
    #    if robot.side == pos.Side.Yellow:
    #        await propulsion.faceDirection(95, 1.0)
    #        await asyncio.sleep(short_timeout)
    #        await propulsion.faceDirection(85, 1.0)
    #        await asyncio.sleep(short_timeout)
    #        await propulsion.faceDirection(90, 1.0)
    #        await asyncio.sleep(short_timeout)
    #    elif robot.side == pos.Side.Blue:
    #        await propulsion.faceDirection(-95, 1.0)
    #        await asyncio.sleep(short_timeout)
    #        await propulsion.faceDirection(-85, 1.0)
    #        await asyncio.sleep(short_timeout)
    #        await propulsion.faceDirection(-90, 1.0)
    #        await asyncio.sleep(short_timeout)

    # eloignement
    await ascenseur_arr_transport()
    await asyncio.sleep(short_timeout)
    await propulsion.translation(0.15, 0.2)
    await asyncio.sleep(long_timeout)

@robot.sequence
async def construction_2_etages_arr():
    global global_turn_speed
    global global_pneuma_timeout

    short_timeout = 0.1
    long_timeout = 0.3

    print ("Prise planches")
    await ascenseur_arr_soulage()
    await asyncio.sleep(short_timeout)
    await soulageur_arr_transport()
    await asyncio.sleep(short_timeout)
    await pump_arr_on()
    await asyncio.sleep(short_timeout)
    await bras_arr_prise_hard()
    await asyncio.sleep(short_timeout)
    await bras_arr_transport()
    await asyncio.sleep(short_timeout)
    await soulageur_arr_transport()
    await asyncio.sleep(short_timeout)
    
    print ("Approche initiale du site de construction")
    await propulsion.translation(-0.15, 0.15)
    await asyncio.sleep(long_timeout)

    print ("Construction niveau 1")
    await ecarteur_arr_on()
    await asyncio.sleep(short_timeout)
    await bras_arr_standby()
    await asyncio.sleep(short_timeout)
    await ventouses_arr_int_lache()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(global_pneuma_timeout)
    await soulageur_arr_down()
    await asyncio.sleep(short_timeout)
    await ascenseur_arr_down()
    await asyncio.sleep(short_timeout)

    print ("Translation")
    await propulsion.translation(0.10, 0.15)
    await asyncio.sleep(long_timeout)
    await ecarteur_arr_off()
    await asyncio.sleep(short_timeout)

    print ("Construction niveau 2")
    await ascenseur_arr_stage2_high()
    await asyncio.sleep(long_timeout)
    await propulsion.translation(-0.12, 0.15)
    await asyncio.sleep(short_timeout)
    await bras_arr_prise()
    await asyncio.sleep(short_timeout)
    await ascenseur_arr_stage2_depose()
    await asyncio.sleep(short_timeout)
    await pump_arr_off()
    await asyncio.sleep(short_timeout)
    await ventouses_arr_ext_lache()
    await asyncio.sleep(short_timeout)

    print ("Fin")
    await propulsion.translation(0.17, 0.15)
    await asyncio.sleep(short_timeout)
    await bras_arr_standby()
    await asyncio.sleep(short_timeout)
    await ascenseur_arr_standby()
    await asyncio.sleep(long_timeout)

@robot.sequence
async def construction_1_etage_arr():
    global global_turn_speed
    global global_pneuma_timeout

    # FIXME : DEBUG
    #print ("DEBUG TIMEOUT")
    #await asyncio.sleep(2.0)
    #print ("GO!")

    short_timeout = 0.1
    long_timeout = 0.3

    print ("Prise planches")
    await ascenseur_arr_soulage()
    await asyncio.sleep(short_timeout)
    await soulageur_arr_transport()
    await asyncio.sleep(short_timeout)
    await pump_arr_on()
    await asyncio.sleep(short_timeout)
    await bras_arr_prise_hard()
    await asyncio.sleep(short_timeout)
    await bras_arr_transport()
    await asyncio.sleep(short_timeout)
    await soulageur_arr_transport()
    await asyncio.sleep(short_timeout)
    
    print ("Approche initiale du site de construction")
    await propulsion.translation(-0.20, 0.15)
    await asyncio.sleep(long_timeout)

    print ("Construction niveau 1")
    await ecarteur_arr_on()
    await asyncio.sleep(short_timeout)
    await bras_arr_up()
    await asyncio.sleep(long_timeout)
    await ventouses_arr_int_lache()
    await propulsion.translation(-0.01, 0.15)
    await asyncio.sleep(short_timeout)
    await soulageur_arr_down()
    await asyncio.sleep(short_timeout)
    await ascenseur_arr_transport()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(global_pneuma_timeout)
    await ascenseur_arr_soulage()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)

    print ("Fin")
    await propulsion.translation(0.21, 0.15)
    await asyncio.sleep(short_timeout)
    await bras_arr_standby()
    await asyncio.sleep(short_timeout)
    await ecarteur_arr_off()
    await asyncio.sleep(short_timeout)
    await ascenseur_arr_standby()
    await asyncio.sleep(short_timeout)


@robot.sequence
async def construction_1_etage_bis_arr():
    global global_turn_speed
    global global_pneuma_timeout

    # FIXME : DEBUG
    #print ("DEBUG TIMEOUT")
    #await asyncio.sleep(2.0)
    #print ("GO!")

    short_timeout = 0.1
    long_timeout = 0.3

    print ("Approche initiale du site de construction")
    await propulsion.translation(-0.20, 0.15)
    await asyncio.sleep(long_timeout)

    print ("Construction niveau 1")
    await soulageur_arr_down()
    await asyncio.sleep(short_timeout)
    await ascenseur_arr_down()
    await asyncio.sleep(short_timeout)
    await bras_arr_prise()
    await asyncio.sleep(short_timeout)
    await pump_arr_off()
    await asyncio.sleep(short_timeout)
    await ventouses_arr_ext_lache()
    await asyncio.sleep(short_timeout)
    await ascenseur_arr_transport()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(global_pneuma_timeout)

    print ("Fin")
    await propulsion.translation(0.20, 0.15)
    await asyncio.sleep(short_timeout)
    await bras_arr_standby()
    await asyncio.sleep(short_timeout)
    await ecarteur_arr_off()
    await asyncio.sleep(short_timeout)
    await ascenseur_arr_standby()
    await asyncio.sleep(short_timeout)


########################
# SEQUENCES BASIQUES   #
########################

# POMPE

@robot.sequence
async def pump_arr_off():
    await robot.gpioSet('pompe_g', False)
    # FIXME : DEBUG : failsafe
    await robot.gpioSet('pompe_g', False)

@robot.sequence
async def pump_arr_on():
    await robot.gpioSet('pompe_g', True)
    # FIXME : DEBUG : failsafe
    await robot.gpioSet('pompe_g', True)


# ASCENSEUR

async def ascenseur_move(pose, torque = 1.0, speed = 1.0):

    # Enable Dynamixel
    await servos.setMaxTorque(['ascenseur'], torque)
    await servos.setEnable(['ascenseur'], True)

    # Move Dynamixel
    await servos.moveMultiple({'ascenseur': pose}, speed)

@robot.sequence
async def ascenseur_arr_disable():
    await servos.setMaxTorque(['ascenseur'], 0)
    await servos.setEnable(['ascenseur'], False)

@robot.sequence
async def ascenseur_arr_down():
    await ascenseur_move(pose_asc_down)

@robot.sequence
async def ascenseur_arr_up():
    await ascenseur_move(pose_asc_up)

@robot.sequence
async def ascenseur_arr_up_high():
    await ascenseur_move(pose_asc_up_high)

@robot.sequence
async def ascenseur_arr_up_safe():
    await ascenseur_move(pose_asc_up, 0.5, 0.3)

@robot.sequence
async def ascenseur_arr_down_safe():
    await ascenseur_move(pose_asc_down, 0.3, 0.3)

@robot.sequence
async def ascenseur_arr_standby():
    await ascenseur_move(pose_asc_standby)

@robot.sequence
async def ascenseur_arr_stage2_high():
    await ascenseur_move(pose_asc_stage2_high)

@robot.sequence
async def ascenseur_arr_stage2_depose():
    await ascenseur_move(pose_asc_stage2_depose)

@robot.sequence
async def ascenseur_arr_stage2_low():
    await ascenseur_move(pose_asc_stage2_low)

@robot.sequence
async def ascenseur_arr_soulage():
    await ascenseur_move(pose_asc_soulage)

@robot.sequence
async def ascenseur_arr_transport():
    await ascenseur_move(pose_asc_transport)


# SOULAGEUR

async def soulageur_move(pose, torque = 1.0, speed = 1.0):
    # Enable Dynamixel
    await servos.setMaxTorque(['soulageur'], torque)
    await servos.setEnable(['soulageur'], True)

    # Move Dynamixel
    await servos.moveMultiple({'soulageur': pose}, speed)

@robot.sequence
async def soulageur_arr_up():
    await soulageur_move(pose_soulageur_up)

@robot.sequence
async def soulageur_arr_transport():
    await soulageur_move(pose_soulageur_transport)

@robot.sequence
async def soulageur_arr_down():
    await soulageur_move(pose_soulageur_down)

@robot.sequence
async def soulageur_arr_mid():
    await soulageur_move(pose_soulageur_mid)

@robot.sequence
async def soulageur_arr_disable():
    await servos.setMaxTorque(['soulageur'], 0)
    await servos.setEnable(['soulageur'], False)


# BRAS

async def bras_move(pose, torque = 1.0, speed = 1.0):
    # Enable Dynamixel
    await servos.setMaxTorque(['bras'], torque)
    await servos.setEnable(['bras'], True)

    # Move Dynamixel
    await servos.moveMultiple({'bras': pose}, speed)

@robot.sequence
async def bras_arr_prise():
    await bras_move(pose_bras_prise)

@robot.sequence
async def bras_arr_prise_hard():
    await bras_move(pose_bras_prise_hard)

@robot.sequence
async def bras_arr_standby():
    await bras_move(pose_bras_standby)

@robot.sequence
async def bras_arr_up():
    await bras_move(pose_bras_up)

@robot.sequence
async def bras_arr_transport():
    await bras_move(pose_bras_transport)


# PNEUMATIQUE

@robot.sequence
async def ventouses_arr_int_lache():
    await pneumatic.multiple_valves_on(4,7)

@robot.sequence
async def ventouses_arr_int_attrape():
    await pneumatic.multiple_valves_off(4,7)

@robot.sequence
async def ventouses_arr_ext_lache():
    await pneumatic.multiple_valves_on(2, 8)

@robot.sequence
async def ventouses_arr_ext_attrape():
    await pneumatic.multiple_valves_off(2, 8)

@robot.sequence
async def ecarteur_arr_on():
    await pneumatic.valve_on(5)

@robot.sequence
async def ecarteur_arr_off():
    await pneumatic.valve_off(5)


