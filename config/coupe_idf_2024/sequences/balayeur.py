import asyncio

balayeur_gauche_inter = 9900
balayeur_gauche_rentre = 8760
balayeur_gauche_push = 9200
balayeur_gauche_sorti = 13500

balayeur_droit_inter = 9700
balayeur_droit_rentre = 10780
balayeur_droit_push = 10230
balayeur_droit_sorti = 6150

#donne un coup avec le balayeur gauche pour ejecter une plante couchée
@robot.sequence
async def balayeur_g_degage():
    await servos.setEnable(['balayeur_gauche'], True)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_sorti}, 1)
    await asyncio.sleep(0.2)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_rentre}, 1)

#donne un coup avec le balayeur droit pour ejecter une plante couchée
@robot.sequence
async def balayeur_d_degage():
    await servos.setEnable(['balayeur_droit'], True)
    await servos.moveMultiple({'balayeur_droit': balayeur_droit_sorti}, 1)
    await asyncio.sleep(0.2)
    await servos.moveMultiple({'balayeur_droit': balayeur_droit_rentre}, 1)

@robot.sequence
async def push_right():
    await servos.setEnable(['balayeur_droit'], True)
    await servos.moveMultiple({'balayeur_droit': balayeur_droit_push}, 1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple({'balayeur_droit': balayeur_droit_rentre}, 1)

@robot.sequence
async def push_left():
    await servos.setEnable(['balayeur_droit'], True)
    await servos.moveMultiple({'balayeur_droit': balayeur_droit_push}, 1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple({'balayeur_droit': balayeur_droit_rentre}, 1)

# maintient une plante ou un pot avec le balayeur gauche
@robot.sequence
async def balayeur_g_hold():
    await servos.setEnable(['balayeur_gauche'], True)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_inter}, 1)
    await asyncio.sleep(0.1)

# maintient une plante ou un pot avec le balayeur droit
@robot.sequence
async def balayeur_d_hold():
    await servos.setEnable(['balayeur_droit'], True)
    await servos.moveMultiple({'balayeur_droit': balayeur_droit_inter}, 1)
    await asyncio.sleep(0.1)

# positionnement initial (au centre du balayeur)
@robot.sequence
async def balayeur_init():
    await servos.setEnable(['balayeur_gauche', 'balayeur_droit'], True)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_rentre, 'balayeur_droit': balayeur_droit_rentre}, 1)

# sequence d'autotest du balayeur
@robot.sequence
async def test_balayeur():
    await servos.setEnable(['balayeur_gauche', 'balayeur_droit'], True)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_rentre, 'balayeur_droit': balayeur_droit_rentre}, 1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_inter, 'balayeur_droit': balayeur_droit_inter}, 1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple({'balayeur_gauche': balayeur_gauche_rentre, 'balayeur_droit': balayeur_droit_rentre}, 1)