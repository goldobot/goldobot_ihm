import asyncio

pales_ouvertes = {
    'pale_g': 577,
    'pale_d': 425
}

pales_fermees = {
    'pale_g': 297,
    'pale_d': 709
}

pales_prise = {
    'pale_g': 373,
    'pale_d': 621
}

chariot_rentre = {
    'chariot_g': 807,
    'chariot_d': 213
}

chariot_sorti = {
    'chariot_g': 518,
    'chariot_d': 493
}

@robot.sequence
async def pince_init():
    # Activation dynamixels
    await servos.setMaxTorque(['pale_g', 'pale_d'], 1.0)
    await servos.setMaxTorque(['chariot_g', 'chariot_d'], 1.0)
    
    await servos.setEnable(['pale_g', 'pale_d'], True)
    await servos.setEnable(['chariot_g', 'chariot_d'], True)

@robot.sequence
async def pince_open():
    await servos.moveMultiple(pales_ouvertes, speed=1)

@robot.sequence
async def pince_close():
    await servos.moveMultiple(pales_fermees, speed=1)

@robot.sequence
async def pince_take():
    await servos.moveMultiple(pales_prise, speed=1)

@robot.sequence
async def chariot_open():
    await servos.moveMultiple(chariot_sorti, speed=1)

@robot.sequence
async def chariot_close():
    await servos.moveMultiple(chariot_rentre, speed=1)
    