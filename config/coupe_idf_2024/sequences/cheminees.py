import asyncio

turbine_init = 4000
turbine_l_init = 3600
turbine_low_rpm = 6200
turbine_hold_rpm = 6250
turbine_high_rpm = 8250

porte_g_ouverte = 7000
porte_g_fermee = 8800

porte_d_ouverte = 12100
porte_d_fermee = 10500


async def turbine_g_set_speed(speed):
    await servos.setEnable(['turbine_g'], True)
    await servos.moveMultiple({'turbine_g': speed}, 1)


async def turbine_d_set_speed(speed):
    await servos.setEnable(['turbine_d'], True)
    await servos.moveMultiple({'turbine_d': speed}, 1)


# Met les turbines a leur consigne d'arret, permet que les ESC arretent de biper
@robot.sequence
async def init_turbines():
    await servos.setEnable(['turbine_g', 'turbine_d'], True)
    await servos.moveMultiple({'turbine_g': turbine_init, 'turbine_d': turbine_init}, 1)


# Sequence d'autotest, fait un petit pulse de turbines pendant 1 seconde
@robot.sequence
async def test_turbines():
    await init_turbines()
    await asyncio.sleep(5)
    await servos.moveMultiple({'turbine_g': turbine_low_rpm, 'turbine_d': turbine_low_rpm}, 1)
    await asyncio.sleep(1)
    await servos.moveMultiple({'turbine_g': turbine_init, 'turbine_d': turbine_init}, 1)


# Met la turbine droite en vitesse d'aspiration
@robot.sequence
async def turbine_d_suck():
    await turbine_d_set_speed(turbine_high_rpm)


# Met la turbine gauche en vitesse d'aspiration
@robot.sequence
async def turbine_g_suck():
    await turbine_g_set_speed(turbine_high_rpm)


# Met la turbine droite en vitesse de maintien
@robot.sequence
async def turbine_d_enable():
    await turbine_d_set_speed(turbine_hold_rpm)

# Met la turbine gauche en vitesse de maintien
@robot.sequence
async def turbine_g_hold():
    await turbine_g_set_speed(turbine_hold_rpm)

# Arrete la turbine gauche
@robot.sequence
async def turbine_g_stop():
    await turbine_g_set_speed(turbine_init)


# Arrete la turbine droite
@robot.sequence
async def turbine_d_stop():
    await turbine_d_set_speed(turbine_init)


# Met la turbine droite en vitesse de maintien (legacy)
@robot.sequence
async def turbine_d_hold():
    await turbine_d_set_speed(turbine_hold_rpm)

# Met la turbine gauche en vitesse de maintien (legacy)
@robot.sequence
async def turbine_g_enable():
    await turbine_g_set_speed(turbine_hold_rpm)


# Sequence d'autotest des portes
@robot.sequence
async def portes_test():
    await servos.setEnable(['porte_gauche', 'porte_droite'], True)
    await servos.moveMultiple({'porte_gauche': porte_g_fermee, 'porte_droite': porte_d_ferme}, 1)
    await asyncio.sleep(1)
    await servos.moveMultiple({'porte_gauche': porte_g_fermee, 'porte_droite': porte_d_ferme}, 1)


# Ouvre la porte gauche (laisse passer les plantes)
@robot.sequence
async def porte_g_ouvre():
    await servos.setEnable(['porte_gauche'], True)
    await servos.moveMultiple({'porte_gauche': porte_g_ouverte}, 1)


# Ferme la porte gauche (bloque les plantes)
@robot.sequence
async def porte_g_ferme():
    await servos.setEnable(['porte_gauche'], True)
    await servos.moveMultiple({'porte_gauche': porte_g_fermee}, 1)


# Ouvre la porte droite (laisse passer les plantes)
@robot.sequence
async def porte_d_ouvre():
    await servos.setEnable(['porte_droite'], True)
    await servos.moveMultiple({'porte_droite': porte_d_ouverte}, 1)


# Ferme la porte droite (bloque les plantes)
@robot.sequence
async def porte_d_ferme():
    await servos.setEnable(['porte_droite'], True)
    await servos.moveMultiple({'porte_droite': porte_d_fermee}, 1)
