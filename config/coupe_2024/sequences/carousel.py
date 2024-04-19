
slots_prise = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
slots_depose = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

@robot.sequence
async def empty_carousel():
    # Activation dynamixels
    await servos.setMaxTorque(['carousel'], 0.30)
    await servos.setMaxTorque(['ejecteur_gauche', 'ejecteur_centre', 'ejecteur_droit'], 0.20)
    await servos.setEnable(['epaule_g', 'ejecteur_gauche', 'ejecteur_centre', 'ejecteur_droit'], True)
    
    # Init bras
    for s in slots_depose():
        await servos.moveMultiple({'carousel': s}, speed=1.0)
        await asyncio.sleep(0.5)
        if (servos.states['chariot_d'].measured_position > s-10) and (servos.states['chariot_d'].measured_position < s+10):
            await eject_left()
            await eject_center()
            await eject_right()

@robot.sequence
async def eject_left():

@robot.sequence
async def eject_center():

@robot.sequence
async def eject_right():

