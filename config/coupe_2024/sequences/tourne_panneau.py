import asyncio

tourne_panneau_out_pos = 650
tourne_panneau_in_pos = 510

@robot.sequence
async def tourne_panneau_out():
    await servos.setMaxTorque(['tourne_panneau'], 0.50)
    await servos.setEnable(['tourne_panneau'], True)
    await servos.moveMultiple({'tourne_panneau': tourne_panneau_out_pos}, speed=1)

@robot.sequence
async def tourne_panneau_in():
    await servos.setMaxTorque(['tourne_panneau'], 0.50)
    await servos.setEnable(['tourne_panneau'], True)
    await servos.moveMultiple({'tourne_panneau': tourne_panneau_in_pos}, speed=1)