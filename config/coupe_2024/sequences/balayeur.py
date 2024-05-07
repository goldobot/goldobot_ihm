import asyncio

balayeur_gauche_inter = 10000
balayeur_gauche_rentre = 8750
balayeur_gauche_sorti = 13500

balayeur_droit_inter = 9600
balayeur_droit_rentre = 10780
balayeur_droit_sorti = 6150

@robot.sequence
async def balayeur_g_degage():
    await servos.setEnable(['balayeur_gauche'], True)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_sorti}, 1)
    await asyncio.sleep(0.2)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_rentre}, 1)

@robot.sequence
async def balayeur_d_degage():
    await servos.setEnable(['balayeur_droit'], True)
    await servos.moveMultiple({'balayeur_droit': balayeur_droit_sorti}, 1)
    await asyncio.sleep(0.2)
    await servos.moveMultiple({'balayeur_droit': balayeur_droit_rentre}, 1)

@robot.sequence
async def balayeur_g_hold():
    await servos.setEnable(['balayeur_gauche'], True)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_inter}, 1)
    await asyncio.sleep(0.1)

@robot.sequence
async def balayeur_d_hold():
    await servos.setEnable(['balayeur_droit'], True)
    await servos.moveMultiple({'balayeur_droit': balayeur_droit_inter}, 1)
    await asyncio.sleep(0.1)

@robot.sequence
async def balayeur_init():
    await servos.setEnable(['balayeur_gauche', 'balayeur_droit'], True)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_rentre, 'balayeur_droit': balayeur_droit_rentre}, 1)

@robot.sequence
async def test_balayeur():
    await servos.setEnable(['balayeur_gauche', 'balayeur_droit'], True)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_rentre, 'balayeur_droit': balayeur_droit_rentre}, 1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_inter, 'balayeur_droit': balayeur_droit_inter}, 1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_rentre, 'balayeur_droit': balayeur_droit_rentre}, 1)