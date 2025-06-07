# FIXME : DEBUG
# import modules from sequence directory
from . import actuators_pneuma
from . import actuators_dyna

from . import actuators_lift
import asyncio

pose_asc_av_down = 0
pose_asc_av_soulage = 3800
pose_asc_av_transport = 3504
pose_asc_av_standby = 2800
pose_asc_av_stage2_high = 450
#pose_asc_av_stage2_depose = 0x7C00
pose_asc_av_stage2_depose = 0x8400
#pose_asc_av_stage2_tassage = 0x7C80
pose_asc_av_stage2_tassage = 0x6E00
pose_asc_av_stage3_predepose = 0xF980
pose_asc_av_stage3_depose = 0xEE80
pose_asc_av_stage2_low = 622
pose_asc_av_up = 0xF980

pose_bras_av_up = 626
pose_bras_av_transport = 410
pose_bras_av_prise = 351

pose_soulageur_av_down = 206
pose_soulageur_av_mid = 380
pose_soulageur_av_up = 530
pose_soulageur_av_transport = 560

pose_ecarteur_d_rentre = 259
pose_ecarteur_d_sorti = 592
pose_ecarteur_g_rentre = 755
pose_ecarteur_g_sorti = 427

pose_ecarteur_int_d_sorti = 777
pose_ecarteur_int_d_rentre = 456
pose_ecarteur_int_g_sorti = 230
pose_ecarteur_int_g_rentre = 567


@robot.sequence
async def actuators_front_prepare_test():

    # Pneuma
    await actuators_pneuma.reset_valves()
    await actuators_pneuma.start_compressor()

    # Propulsion
    await odrive.clearErrors()
    await asyncio.sleep(0.5)
    await propulsion.clearError()
    await asyncio.sleep(0.5)
    await propulsion.setAccelerationLimits(1,1,10,10)
    await asyncio.sleep(0.5)
    await propulsion.setMotorsEnable(True)
    await asyncio.sleep(0.5)
    await propulsion.setEnable(True)
    await asyncio.sleep(1)
    
    # Actionneurs
    await ascenseur_av_homing()
    await asyncio.sleep(1)
    await ascenseur_av_down()
    await asyncio.sleep(1)

@robot.sequence
async def prise_av():
    await ascenseur_av_down()
    await ecarteur_int_av_off()
    await ecarteur_av_off()
    await soulageur_av_mid()
    await bras_av_transport()
    await asyncio.sleep(0.5)
    
    print ("MOVE !!!!")
    #await asyncio.sleep(10)
    try:
        await propulsion.reposition(0.2, 0.2)
    except:
        await propulsion.reposition(0.2, 0.2)

    await pump_av_on()
    await asyncio.sleep(0.2)
    await soulageur_av_up()
    await bras_av_prise()
    await soulageur_av_transport()
    await bras_av_transport()
    await ascenseur_av_transport()
    await asyncio.sleep(0.2)

@robot.sequence
async def construction_2_etages_av():
    delay = 2
    await ecarteur_av_on()
    await asyncio.sleep(delay)
    await ecarteur_int_av_on()
    await asyncio.sleep(delay)
    await soulageur_av_mid()
    await ascenseur_av_stage2_depose()
    await asyncio.sleep(delay)
    await ecarteur_av_off()
    await asyncio.sleep(delay)
    await ascenseur_av_stage2_tassage()
    await pump_av_off()

@robot.sequence
async def depose_3_etages_av():
    await bras_av_up()
    await ascenseur_av_stage3_predepose()
    await asyncio.sleep(2)
    print ("MOVE !!!!")
    #await asyncio.sleep(10)
    try:
        await propulsion.reposition(0.2, 0.2)
    except:
        await propulsion.reposition(0.2, 0.2)

    await soulageur_av_mid()
    await asyncio.sleep(1)
    
    await ascenseur_av_stage3_depose()
    await asyncio.sleep(2)

    await ventouses_av_ext_lache()
    await ventouses_av_int_lache()
    await asyncio.sleep(1)
    await soulageur_av_down()

    print ("MOVE !!!!")
    await asyncio.sleep(10)
    try:
        await propulsion.reposition(-0.2, 0.2)
    except:
        await propulsion.reposition(-0.2, 0.2)


@robot.sequence
async def ecarteur_av_on(torque = 1.0, speed = 1.0):
    # Enable Dynamixel
    await servos.setMaxTorque(['ecarteur_g', 'ecarteur_d'], torque)
    await servos.setEnable(['ecarteur_g', 'ecarteur_d'], True)

    # Move Dynamixel
    await servos.moveMultiple({'ecarteur_d': pose_ecarteur_d_sorti,
                               'ecarteur_g': pose_ecarteur_g_sorti}, speed)

@robot.sequence
async def ecarteur_av_off(torque = 1.0, speed = 1.0):
    # Enable Dynamixel
    await servos.setMaxTorque(['ecarteur_g', 'ecarteur_d'], torque)
    await servos.setEnable(['ecarteur_g', 'ecarteur_d'], True)

    # Move Dynamixel
    await servos.moveMultiple({'ecarteur_d': pose_ecarteur_d_rentre,
                               'ecarteur_g': pose_ecarteur_g_rentre}, speed)

@robot.sequence
async def ecarteur_int_av_on(torque = 1.0, speed = 1.0):
    # Enable Dynamixel
    await servos.setMaxTorque(['ecarteur_int_g', 'ecarteur_int_d'], torque)
    await servos.setEnable(['ecarteur_int_g', 'ecarteur_int_d'], True)

    # Move Dynamixel
    await servos.moveMultiple({'ecarteur_int_d': pose_ecarteur_int_d_sorti,
                               'ecarteur_int_g': pose_ecarteur_int_g_sorti}, speed)

@robot.sequence
async def ecarteur_int_av_off(torque = 1.0, speed = 1.0):
    # Enable Dynamixel
    await servos.setMaxTorque(['ecarteur_int_g', 'ecarteur_int_d'], torque)
    await servos.setEnable(['ecarteur_int_g', 'ecarteur_int_d'], True)

    # Move Dynamixel
    await servos.moveMultiple({'ecarteur_int_d': pose_ecarteur_int_d_rentre,
                               'ecarteur_int_g': pose_ecarteur_int_g_rentre}, speed)
    
@robot.sequence
async def ecarteur_int_av_disable():
    # Enable Dynamixel
    await servos.setMaxTorque(['ecarteur_int_g', 'ecarteur_int_d'], 0)
    await servos.setEnable(['ecarteur_int_g', 'ecarteur_int_d'], False)

@robot.sequence
async def ecarteur_av_disable():
    # Enable Dynamixel
    await servos.setMaxTorque(['ecarteur_g', 'ecarteur_d'], 0)
    await servos.setEnable(['ecarteur_g', 'ecarteur_d'], False)
####################################################
##############         PUMPS          ##############
####################################################

@robot.sequence
async def pump_av_off():
    await robot.gpioSet('pompe_d', False)
    await robot.gpioSet('pompe_d', False)

@robot.sequence
async def pump_av_on():
    await robot.gpioSet('pompe_d', True)
    await robot.gpioSet('pompe_d', True)

@robot.sequence
async def ascenseur_av_homing():
    await bras_av_prise()
    await ecarteur_av_on()
    await asyncio.sleep(2)
    await bras_av_disable()
    await actuators_lift.lift_homing()
    await asyncio.sleep(15)
    await ecarteur_av_off()
    await asyncio.sleep(1)
    await ecarteur_int_av_off()
    await asyncio.sleep(1)
    await ecarteur_av_disable()
    #await ascenseur_av_down()

async def ascenseur_av_move(pose, speed = 0x200):
    # Enable Dynamixel
    await actuators_lift.lift_move(pose, speed)

@robot.sequence
async def ascenseur_av_disable():
    await actuators_lift.lift_asserv_disable()

@robot.sequence
async def ascenseur_av_down():
    await ascenseur_av_move(pose_asc_av_down+6000)
    await asyncio.sleep(2)
    await ascenseur_av_move(pose_asc_av_down+3000)
    await asyncio.sleep(2)
    await ascenseur_av_move(pose_asc_av_down)

@robot.sequence
async def ascenseur_av_up():
    await ascenseur_av_move(pose_asc_av_up)

@robot.sequence
async def ascenseur_av_standby():
    await ascenseur_av_move(pose_asc_av_standby)

@robot.sequence
async def ascenseur_av_stage2_high():
    await ascenseur_av_move(pose_asc_av_stage2_high)

@robot.sequence
async def ascenseur_av_stage2_depose():
    await ascenseur_av_move(pose_asc_av_stage2_depose)

@robot.sequence
async def ascenseur_av_stage2_tassage():
    await ascenseur_av_move(pose_asc_av_stage2_tassage)

@robot.sequence
async def ascenseur_av_stage3_predepose():
    await ascenseur_av_move(pose_asc_av_stage3_predepose)

@robot.sequence
async def ascenseur_av_stage3_depose():
    await ascenseur_av_move(pose_asc_av_stage3_depose)

@robot.sequence
async def ascenseur_av_stage2_low():
    await ascenseur_av_move(pose_asc_av_stage2_low)

@robot.sequence
async def ascenseur_av_soulage():
    await ascenseur_av_move(pose_asc_av_soulage)

@robot.sequence
async def ascenseur_av_transport():
    await ascenseur_av_move(pose_asc_av_transport)

####################################################
##############      SOULAGEUR AR      ##############
####################################################
async def soulageur_av_move(pose, torque = 1.0, speed = 1.0):
    # Enable Dynamixel
    await servos.setMaxTorque(['soulageur_av'], torque)
    await servos.setEnable(['soulageur_av'], True)

    # Move Dynamixel
    await servos.moveMultiple({'soulageur_av': pose}, speed)

@robot.sequence
async def soulageur_av_up():
    await soulageur_av_move(pose_soulageur_av_up)

@robot.sequence
async def soulageur_av_transport():
    await soulageur_av_move(pose_soulageur_av_transport)

@robot.sequence
async def soulageur_av_down():
    await soulageur_av_move(pose_soulageur_av_down)

@robot.sequence
async def soulageur_av_mid():
    await soulageur_av_move(pose_soulageur_av_mid)

@robot.sequence
async def soulageur_av_disable():
    await servos.setMaxTorque(['soulageur_av'], 0)
    await servos.setEnable(['soulageur_av'], False)

####################################################
##############        BRAS AR        ###############
####################################################

async def bras_av_move(pose, torque = 1.0, speed = 1.0):
    # Enable Dynamixel
    await servos.setMaxTorque(['bras_av'], torque)
    await servos.setEnable(['bras_av'], True)

    # Move Dynamixel
    await servos.moveMultiple({'bras_av': pose}, speed)

async def bras_av_disable():
    # Enable Dynamixel
    await servos.setMaxTorque(['bras_av'], 0)
    await servos.setEnable(['bras_av'], False)

@robot.sequence
async def bras_av_prise():
    await bras_av_move(pose_bras_av_prise)

@robot.sequence
async def bras_av_prise_hard():
    await bras_av_move(pose_bras_av_prise_hard)

@robot.sequence
async def bras_av_standby():
    await bras_av_move(pose_bras_av_standby)

@robot.sequence
async def bras_av_up():
    await bras_av_move(pose_bras_av_up)

@robot.sequence
async def bras_av_transport():
    await bras_av_move(pose_bras_av_transport)

####################################################
##############        PNEUMA        ###############
####################################################
@robot.sequence
async def ventouses_av_int_lache():
    await pneumatic.valve_on(11)

@robot.sequence
async def ventouses_av_int_attrape():
    await pneumatic.valve_off(11)

@robot.sequence
async def ventouses_av_ext_lache():
    # G : 3 / D : 6
    await pneumatic.multiple_valves_on(3, 6)

@robot.sequence
async def ventouses_av_ext_attrape():
    # G : 3 / D : 6
    await pneumatic.multiple_valves_off(3, 6)
