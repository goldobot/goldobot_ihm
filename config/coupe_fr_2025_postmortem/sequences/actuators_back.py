from . import actuators_pneuma
from . import actuators_dyna

import asyncio

global_long_speed = 0.60
global_turn_speed = 3.2
global_turn_speed_slow = 1.5

@robot.sequence
async def preprise_arr():
    global global_turn_speed
    global global_long_speed

    short_timeout = 0.1
    long_timeout = 0.3

    # recul
    await actuators_dyna.bras_standby()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ventouses_ext_attrape()
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ventouses_int_attrape()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.ascenseur_down()
    await asyncio.sleep(short_timeout)
    await propulsion.translation(-0.10, 0.2)
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)

    # verrouillage planches
    await actuators_dyna.soulageur_up()
    await actuators_dyna.bras_prise_hard()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.pump_on()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_transport()
    await asyncio.sleep(short_timeout)

    # wooble..
    # FIXME : TODO
    #await actuators_dyna.ascenseur_soulage()
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
    await actuators_dyna.ascenseur_transport()
    await asyncio.sleep(short_timeout)
    await propulsion.translation(0.10, 0.2)
    await asyncio.sleep(long_timeout)

@robot.sequence
async def construction_2_etages_arr():
    global global_turn_speed

    short_timeout = 0.1
    long_timeout = 0.3

    print ("Prise planches")
    await actuators_dyna.ascenseur_soulage()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.soulageur_transport()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.pump_on()
    await actuators_dyna.pump_on()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_prise_hard()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_transport()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.soulageur_transport()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)
    
    print ("Approche initiale du site de construction")
    await propulsion.translation(-0.15, 0.15)
    await asyncio.sleep(long_timeout)

    print ("Construction niveau 1")
    await actuators_pneuma.ecarteur_on()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_standby()
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ventouses_int_lache()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(1.0)
    await actuators_dyna.soulageur_down()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.ascenseur_down()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(1.0)

    print ("Translation")
    await propulsion.translation(0.10, 0.15)
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ecarteur_off()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)

    print ("Construction niveau 2")
    await actuators_dyna.ascenseur_stage2_high()
    await asyncio.sleep(long_timeout)
    await propulsion.translation(-0.12, 0.15)
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_prise()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.ascenseur_stage2_depose()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.pump_off()
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ventouses_ext_lache()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)

    print ("Fin")
    await propulsion.translation(0.17, 0.15)
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_standby()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.ascenseur_standby()
    await asyncio.sleep(short_timeout)

@robot.sequence
async def construction_1_etage_arr():
    global global_turn_speed

    short_timeout = 0.1
    long_timeout = 0.3

    print ("Prise planches")
    await actuators_dyna.ascenseur_soulage()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.soulageur_transport()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.pump_on()
    await actuators_dyna.pump_on()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_prise_hard()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_transport()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.soulageur_transport()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)
    
    print ("Approche initiale du site de construction")
    await propulsion.translation(-0.20, 0.15)
    await asyncio.sleep(long_timeout)

    print ("Construction niveau 1")
    await actuators_pneuma.ecarteur_on()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_standby()
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ventouses_int_lache()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(1.0)
    await actuators_dyna.soulageur_down()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.ascenseur_down()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(1.0)

    print ("Fin")
    await propulsion.translation(0.20, 0.15)
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_standby()
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ecarteur_off()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.ascenseur_standby()
    await asyncio.sleep(short_timeout)

