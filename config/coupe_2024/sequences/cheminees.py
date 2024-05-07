import asyncio

turbine_init = 4000
turbine_l_init = 3600
turbine_low_rpm = 6200
turbine_high_rpm = 8000

porte_g_ouverte = 7000
porte_g_fermee = 8500

porte_d_ouverte = 12100
porte_d_fermee = 10700

async def turbine_g_set_speed(speed):
    await servos.setEnable(['turbine_g'], True)
    await servos.moveMultiple({'turbine_g': speed}, 1)

async def turbine_d_set_speed(speed):
    await servos.setEnable(['turbine_d'], True)
    await servos.moveMultiple({'turbine_d': speed}, 1)

@robot.sequence
async def init_turbines():
    await servos.setEnable(['turbine_g', 'turbine_d'], True)
    await servos.moveMultiple({'turbine_g': turbine_init, 'turbine_d': turbine_init}, 1)

@robot.sequence
async def test_turbines():
    await init_turbines()
    await asyncio.sleep(5)
    await servos.moveMultiple({'turbine_g': turbine_low_rpm, 'turbine_d': turbine_low_rpm}, 1)
    await asyncio.sleep(1)
    await servos.moveMultiple({'turbine_g': turbine_init, 'turbine_d': turbine_init}, 1)

@robot.sequence
async def turbine_g_suck():
    await turbine_g_set_speed(turbine_high_rpm)

@robot.sequence
async def turbine_d_suck():
    await turbine_d_set_speed(turbine_high_rpm)

@robot.sequence
async def turbine_g_enable():
    await turbine_g_set_speed(turbine_low_rpm)

@robot.sequence
async def turbine_d_enable():
    await turbine_d_set_speed(turbine_low_rpm)

@robot.sequence
async def turbine_g_stop():
    await turbine_g_set_speed(turbine_init)

@robot.sequence
async def turbine_d_stop():
    await turbine_d_set_speed(turbine_init)

@robot.sequence
async def porte_g_ouvre():
    await servos.setEnable(['porte_gauche'], True)
    await servos.moveMultiple({'porte_gauche': porte_g_ouverte}, 1)

@robot.sequence
async def porte_g_ferme():
    await servos.setEnable(['porte_gauche'], True)
    await servos.moveMultiple({'porte_gauche': porte_g_fermee}, 1)

@robot.sequence
async def porte_d_ouvre():
    await servos.setEnable(['porte_droite'], True)
    await servos.moveMultiple({'porte_droite': porte_d_ouverte}, 1)

@robot.sequence
async def porte_d_ferme():
    await servos.setEnable(['porte_droite'], True)
    await servos.moveMultiple({'porte_droite': porte_d_fermee}, 1)


@robot.sequence
async def plant_in_left():
    if sensors['haut_cheminee_gauche'] is False:
        await asyncio.sleep(0.05)
        if sensors['haut_cheminee_gauche'] is False:
            return True
    return False
