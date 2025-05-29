pose_asc_down = 4095
pose_asc_soulage = 3800
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

####################################################
##############         PUMPS          ##############
####################################################

@robot.sequence
async def pump_off():
    await robot.gpioSet('pompe_d', False)

@robot.sequence
async def pump_on():
    await robot.gpioSet('pompe_d', True)


####################################################
##############      ASCENSEUR AR      ##############
####################################################
async def ascenseur_move(pose, torque = 1.0, speed = 1.0):

    # Enable Dynamixel
    await servos.setMaxTorque(['ascenseur'], torque)
    await servos.setEnable(['ascenseur'], True)

    # Move Dynamixel
    await servos.moveMultiple({'ascenseur': pose}, speed)

@robot.sequence
async def ascenseur_disable():
    await servos.setMaxTorque(['ascenseur'], 0)
    await servos.setEnable(['ascenseur'], False)

@robot.sequence
async def ascenseur_down():
    await ascenseur_move(pose_asc_down)

@robot.sequence
async def ascenseur_up():
    await ascenseur_move(pose_asc_up)

@robot.sequence
async def ascenseur_up_high():
    await ascenseur_move(pose_asc_up_high)

@robot.sequence
async def ascenseur_up_safe():
    await ascenseur_move(pose_asc_up, 0.5, 0.3)

@robot.sequence
async def ascenseur_down_safe():
    await ascenseur_move(pose_asc_down, 0.3, 0.3)

@robot.sequence
async def ascenseur_standby():
    await ascenseur_move(pose_asc_standby)

@robot.sequence
async def ascenseur_stage2_high():
    await ascenseur_move(pose_asc_stage2_high)

@robot.sequence
async def ascenseur_stage2_depose():
    await ascenseur_move(pose_asc_stage2_depose)

@robot.sequence
async def ascenseur_stage2_low():
    await ascenseur_move(pose_asc_stage2_low)

@robot.sequence
async def ascenseur_soulage():
    await ascenseur_move(pose_asc_soulage)

@robot.sequence
async def ascenseur_transport():
    await ascenseur_move(pose_asc_transport)

####################################################
##############      SOULAGEUR AR      ##############
####################################################
async def soulageur_move(pose, torque = 1.0, speed = 1.0):
    # Enable Dynamixel
    await servos.setMaxTorque(['soulageur'], torque)
    await servos.setEnable(['soulageur'], True)

    # Move Dynamixel
    await servos.moveMultiple({'soulageur': pose}, speed)

@robot.sequence
async def soulageur_up():
    await soulageur_move(pose_soulageur_up)

@robot.sequence
async def soulageur_transport():
    await soulageur_move(pose_soulageur_transport)

@robot.sequence
async def soulageur_down():
    await soulageur_move(pose_soulageur_down)

@robot.sequence
async def soulageur_mid():
    await soulageur_move(pose_soulageur_mid)

@robot.sequence
async def soulageur_disable():
    await servos.setMaxTorque(['soulageur'], 0)
    await servos.setEnable(['soulageur'], False)

####################################################
##############        BRAS AR        ###############
####################################################

async def bras_move(pose, torque = 1.0, speed = 1.0):
    # Enable Dynamixel
    await servos.setMaxTorque(['bras'], torque)
    await servos.setEnable(['bras'], True)

    # Move Dynamixel
    await servos.moveMultiple({'bras': pose}, speed)

@robot.sequence
async def bras_prise():
    await bras_move(pose_bras_prise)

@robot.sequence
async def bras_prise_hard():
    await bras_move(pose_bras_prise_hard)

@robot.sequence
async def bras_standby():
    await bras_move(pose_bras_standby)

@robot.sequence
async def bras_up():
    await bras_move(pose_bras_up)

@robot.sequence
async def bras_transport():
    await bras_move(pose_bras_transport)

####################################################
##############        PNEUMA        ###############
####################################################

@robot.sequence
async def ventouses_int_lache():
    await pneumatic.multiple_valves_on(4, 7)

@robot.sequence
async def ventouses_int_attrape():
    await pneumatic.multiple_valves_off(4, 7)

@robot.sequence
async def ventouses_ext_lache():
    await pneumatic.multiple_valves_on(2, 8)

@robot.sequence
async def ventouses_ext_attrape():
    await pneumatic.multiple_valves_off(2, 8)

@robot.sequence
async def ecarteur_on():
    await pneumatic.valve_on(5)

@robot.sequence
async def ecarteur_off():
    await pneumatic.valve_off(5)