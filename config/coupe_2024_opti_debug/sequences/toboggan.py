import asyncio

toboggan_pos_rentre = 3626
toboggan_pos_depose = 2650
toboggan_pos_depose2 = 2450
toboggan_pos_depose_pot = 2488
toboggan_pos_ouvert = 2297
toboggan_pos_deplacement_var = 2560

@robot.sequence
async def toboggan_rentre():
    await servos.setMaxTorque(['carousel'], 0.80)
    await servos.setEnable(['toboggan'], True)
    await servos.moveMultiple({'toboggan': toboggan_pos_rentre}, 1)

@robot.sequence
async def toboggan_depose():
    await servos.setMaxTorque(['carousel'], 0.80)
    await servos.setEnable(['toboggan'], True)
    await servos.moveMultiple({'toboggan': toboggan_pos_depose}, 1)

@robot.sequence
async def toboggan_depose2():
    await servos.setMaxTorque(['carousel'], 0.80)
    await servos.setEnable(['toboggan'], True)
    await servos.moveMultiple({'toboggan': toboggan_pos_depose2}, 1)


@robot.sequence
async def toboggan_ouvre():
    await servos.setMaxTorque(['carousel'], 0.80)
    await servos.setEnable(['toboggan'], True)
    await servos.moveMultiple({'toboggan': toboggan_pos_ouvert}, 1)

@robot.sequence
async def toboggan_deplacement():
    await servos.setMaxTorque(['carousel'], 0.80)
    await servos.setEnable(['toboggan'], True)
    await servos.moveMultiple({'toboggan': toboggan_pos_deplacement_var}, 1)

