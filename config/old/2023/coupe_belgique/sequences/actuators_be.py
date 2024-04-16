import asyncio


class GoldoLift:
    Unknown = 0
    Left = 1
    Right = 2


async def goldo_lift_move(side,pos):
    if (side==GoldoLift.Left):
        await servos.liftsRaw(pos, 80, 0, 0)
    if (side==GoldoLift.Right):
        await servos.liftsRaw(0, 0, pos, 80)


async def goldo_lifts_move(pos, speed = 80):
    await servos.liftsRaw(pos, speed, pos, speed)


async def pump_on(left, right):
    if left:
        await robot.gpioSet('pompe_g', True)
        await robot.gpioSet('pompe_g', True)
    if right:
        await robot.gpioSet('pompe_d', True)
        await robot.gpioSet('pompe_d', True)


async def pump_off(left, right):
    if left:
        await robot.gpioSet('pompe_g', False)
        await robot.gpioSet('pompe_g', False)
    if right:
        await robot.gpioSet('pompe_d', False)
        await robot.gpioSet('pompe_d', False)

@robot.sequence
async def left_pump_on():
    await pump_on(True, False)

@robot.sequence
async def left_pump_off():
    await pump_off(True, False)

@robot.sequence
async def right_pump_on():
    await pump_on(False, True)

@robot.sequence
async def right_pump_off():
    await pump_off(False, True)


epaules_devant = {
    'epaule_g': 2052,
    'epaule_d': 2035
}

epaules_rentrees = {
    'epaule_g': 2952,
    'epaule_d': 1131
}

epaules_ouvertes = {
    'epaule_g': 1609,
    'epaule_d': 2277
}

epaules_prise = {
    'epaule_g': 2240,
    'epaule_d': 1845
}

coudes_leves = {
    'coude_g': 827,
    'coude_d': 204
}

# Cote vert
bras_droit_prise_jaune = {
    'epaule_d': 3124,
    'coude_d': 510
}

bras_droit_depose_jaune = {
    'epaule_d': 1499,
    'coude_d': 515
}

bras_droit_prise_rose = {
    'epaule_d': 2411,
    'coude_d': 515
}

bras_droit_depose_rose = {
    'epaule_d': 1450,
    'coude_d': 510
}

bras_gauche_prise_marron = {
    'epaule_g': 1628,
    'coude_g': 500
}

bras_gauche_depose_marron = {
    'epaule_g': 2555,
    'coude_g': 500
}


# Cote bleu
bras_droit_prise_marron = {
    'epaule_d': 2411,
    'coude_d': 515
}

bras_droit_depose_marron = {
    'epaule_d': 1450,
    'coude_d': 510
}

bras_gauche_prise_jaune = {
    'epaule_g': 937,
    'coude_g': 500
}

bras_gauche_depose_jaune = {
    'epaule_g': 2630,
    'coude_g': 500
}

bras_gauche_prise_rose = {
    'epaule_g': 1628,
    'coude_g': 500
}

bras_gauche_depose_rose = {
    'epaule_g': 2555,
    'coude_g': 500
}




@robot.sequence
async def arms_initialize():

    # Activation dynamixels
    await servos.setMaxTorque(['epaule_g', 'epaule_d'], 0.30)
    await servos.setMaxTorque(['coude_g', 'coude_d'], 0.20)
    
    await servos.setEnable(['epaule_g', 'epaule_d'], True)
    await servos.setEnable(['coude_g', 'coude_d'], True)
    
    # Init bras
    await servos.moveMultiple(epaules_devant, speed=0.7)
    await asyncio.sleep(0.2)
    await servos.moveMultiple(coudes_leves, speed=0.7)
    await asyncio.sleep(0.2)
    
    # initialisation ascenceurs    
    await servos.liftDoHoming(0)
    await servos.liftDoHoming(1)
    await asyncio.sleep(3)
    
    await servos.liftsRaw(60, 60, 0, 0)
    await asyncio.sleep(1)
    await servos.liftsRaw(0, 0, 60, 60)
    await asyncio.sleep(3)
    await servos.moveMultiple(epaules_rentrees, speed=0.7)
    await servos.setMaxTorque(['epaule_g', 'epaule_d'], 1)
    await servos.setMaxTorque(['coude_g', 'coude_d'], 1)


@robot.sequence
async def arms_open():
    await servos.moveMultiple(epaules_ouvertes, speed=1)

@robot.sequence
async def test_lift_left_40():
    await goldo_lift_move(GoldoLift.Left, 40)

@robot.sequence
async def test_lift_right_40():
    await goldo_lift_move(GoldoLift.Right, 40)

@robot.sequence
async def test_lift_left_800():
    await goldo_lift_move(GoldoLift.Left, 800)

@robot.sequence
async def test_lift_right_800():
    await goldo_lift_move(GoldoLift.Right, 800)


async def arms_take():
    await servos.moveMultiple(epaules_prise, speed=1)

# Constructions vertes
async def construction_gateau_haut_vert():
    await goldo_lifts_move(500, 80)
    await pump_on(True, True)
    # bras au dessus du jaune et du marron
    taskarms = asyncio.create_task(servos.moveMultiple(bras_droit_prise_jaune, 1))
    await servos.moveMultiple(bras_gauche_prise_marron, 1)
    await taskarms
    await asyncio.sleep(0.2)
    # descente pour prise
    await goldo_lifts_move(450, 80)
    await asyncio.sleep(0.2)
    # depose marron
    tasklifts = asyncio.create_task(goldo_lifts_move(450, 80))
    await servos.moveMultiple(bras_gauche_depose_marron, 1)
    await asyncio.sleep(0.2)
    await tasklifts
    await goldo_lift_move(GoldoLift.Left, 143)
    await asyncio.sleep(0.2)
    await left_pump_off()
    await asyncio.sleep(0.2)

    # retrait bras gauche
    await goldo_lift_move(GoldoLift.Left, 476)
    taskarms = asyncio.create_task(servos.moveMultiple(bras_gauche_prise_marron, 1))

    # depose jaune
    await goldo_lift_move(GoldoLift.Right, 762)
    await servos.moveMultiple(bras_droit_depose_jaune, 1)
    await goldo_lift_move(GoldoLift.Right, 571)
    await asyncio.sleep(0.2)
    await right_pump_off()
    await asyncio.sleep(0.2)

    # prise rose
    await servos.moveMultiple(bras_droit_prise_rose, 1)
    await asyncio.sleep(0.2)
    await goldo_lift_move(GoldoLift.Right, 429)
    await right_pump_on()
    await asyncio.sleep(0.2)

    # depose rose
    await goldo_lift_move(GoldoLift.Right, 524)
    await servos.moveMultiple(bras_droit_depose_rose, 1)
    await asyncio.sleep(0.2)
    await right_pump_off()
    await taskarms
    await asyncio.sleep(0.2)

    # ecartement bras
    taskarms = asyncio.create_task(servos.moveMultiple(coudes_leves, 1))
    await servos.moveMultiple(epaules_ouvertes, 1)
    await taskarms

async def construction_gateau_milieu_vert():
    await goldo_lifts_move(300, 80)
    await pump_on(True, True)
    # bras au dessus du jaune et du marron
    taskarms = asyncio.create_task(servos.moveMultiple(bras_droit_prise_jaune, 1))
    await servos.moveMultiple(bras_gauche_prise_marron, 1)
    await taskarms
    await asyncio.sleep(0.2)
    # descente pour prise
    await goldo_lifts_move(220, 80)
    await asyncio.sleep(0.2)
    # depose marron
    tasklifts = asyncio.create_task(goldo_lifts_move(300, 80))
    await servos.moveMultiple(bras_gauche_depose_marron, 1)
    await asyncio.sleep(0.2)
    await tasklifts
    await goldo_lift_move(GoldoLift.Left, 143)
    await left_pump_off()
    await asyncio.sleep(0.2)

    # retrait bras gauche
    await goldo_lift_move(GoldoLift.Left, 286)
    taskarms = asyncio.create_task(servos.moveMultiple(bras_gauche_prise_marron, 1))

    # depose jaune
    await goldo_lift_move(GoldoLift.Right, 571)
    await servos.moveMultiple(bras_droit_depose_jaune, 1)
    await asyncio.sleep(0.2)
    await goldo_lift_move(GoldoLift.Right, 381)
    await asyncio.sleep(0.2)
    await right_pump_off()
    await asyncio.sleep(0.2)

    # prise rose
    await servos.moveMultiple(bras_droit_prise_rose, 1)
    await asyncio.sleep(0.2)
    await goldo_lift_move(GoldoLift.Right, 210)
    await right_pump_on()
    await asyncio.sleep(0.2)

    # depose rose
    await goldo_lift_move(GoldoLift.Right, 571)
    await asyncio.sleep(0.2)
    await servos.moveMultiple(bras_droit_depose_rose, 1)
    await asyncio.sleep(0.2)
    await right_pump_off()
    await taskarms
    await asyncio.sleep(0.2)

    # ecartement bras
    taskarms = asyncio.create_task(servos.moveMultiple(coudes_leves, 1))
    await servos.moveMultiple(epaules_ouvertes, 1)
    await taskarms

async def construction_gateau_bas_vert():
    await goldo_lifts_move(100, 80)
    await pump_on(True, True)
    # bras au dessus du jaune et du marron
    taskarms = asyncio.create_task(servos.moveMultiple(bras_droit_prise_jaune, 1))
    await servos.moveMultiple(bras_gauche_prise_marron, 1)
    await taskarms
    await asyncio.sleep(0.2)
    # descente pour prise
    await goldo_lifts_move(40, 80)
    await asyncio.sleep(0.2)
    # depose marron
    tasklifts = asyncio.create_task(goldo_lifts_move(100, 80))
    await servos.moveMultiple(bras_gauche_depose_marron, 1)
    await asyncio.sleep(0.2)
    await tasklifts
    await goldo_lift_move(GoldoLift.Left, 95)
    await left_pump_off()
    await asyncio.sleep(0.2)

    # retrait bras gauche
    await goldo_lift_move(GoldoLift.Left, 95)
    taskarms = asyncio.create_task(servos.moveMultiple(bras_gauche_prise_marron, 1))

    # depose jaune
    await goldo_lift_move(GoldoLift.Right, 381)
    await servos.moveMultiple(bras_droit_depose_jaune, 1)
    await asyncio.sleep(0.2)
    await goldo_lift_move(GoldoLift.Right, 381)
    await right_pump_off()
    await asyncio.sleep(0.1)

    # prise rose
    await servos.moveMultiple(bras_droit_prise_rose, 1)
    await asyncio.sleep(0.2)
    await goldo_lift_move(GoldoLift.Right, 38)
    await right_pump_on()
    await asyncio.sleep(0.2)

    # depose rose
    await goldo_lift_move(GoldoLift.Right, 571)
    await asyncio.sleep(0.1)
    await servos.moveMultiple(bras_droit_depose_rose, 1)
    await asyncio.sleep(0.1)
    await right_pump_off()
    await taskarms
    await asyncio.sleep(0.2)

    # ecartement bras
    taskarms = asyncio.create_task(servos.moveMultiple(coudes_leves, 1))
    await servos.moveMultiple(epaules_ouvertes, 1)
    await taskarms


# Constructions bleues
async def construction_gateau_haut_bleu():
    await goldo_lifts_move(500, 80)
    await pump_on(True, True)
    # bras au dessus du jaune et du marron
    taskarms = asyncio.create_task(servos.moveMultiple(bras_gauche_prise_jaune, 1))
    await servos.moveMultiple(bras_droit_prise_marron, 1)
    await taskarms
    await asyncio.sleep(0.2)
    # descente pour prise
    await goldo_lifts_move(450, 80)
    await asyncio.sleep(0.2)
    # depose marron
    tasklifts = asyncio.create_task(goldo_lifts_move(450, 80))
    await servos.moveMultiple(bras_droit_depose_marron, 1)
    await asyncio.sleep(0.2)
    await tasklifts
    await goldo_lift_move(GoldoLift.Right, 143)
    await asyncio.sleep(0.2)
    await right_pump_off()
    await asyncio.sleep(0.2)

    # retrait bras droit
    await goldo_lift_move(GoldoLift.Right, 476)
    taskarms = asyncio.create_task(servos.moveMultiple(bras_droit_prise_marron, 1))

    # depose jaune
    await goldo_lift_move(GoldoLift.Left, 762)
    await servos.moveMultiple(bras_gauche_depose_jaune, 1)
    await goldo_lift_move(GoldoLift.Left, 571)
    await asyncio.sleep(0.2)
    await left_pump_off()
    await asyncio.sleep(0.2)

    # prise rose
    await servos.moveMultiple(bras_gauche_prise_rose, 1)
    await asyncio.sleep(0.2)
    await goldo_lift_move(GoldoLift.Left, 429)
    await left_pump_on()
    await asyncio.sleep(0.2)

    # depose rose
    await goldo_lift_move(GoldoLift.Left, 524)
    await servos.moveMultiple(bras_gauche_depose_rose, 1)
    await asyncio.sleep(0.2)
    await left_pump_off()
    await taskarms
    await asyncio.sleep(0.2)

    # ecartement bras
    taskarms = asyncio.create_task(servos.moveMultiple(coudes_leves, 1))
    await servos.moveMultiple(epaules_ouvertes, 1)
    await taskarms

async def construction_gateau_milieu_bleu():
    await goldo_lifts_move(300, 80)
    await pump_on(True, True)
    # bras au dessus du jaune et du marron
    taskarms = asyncio.create_task(servos.moveMultiple(bras_gauche_prise_jaune, 1))
    await servos.moveMultiple(bras_droit_prise_marron, 1)
    await taskarms
    await asyncio.sleep(0.2)
    # descente pour prise
    await goldo_lifts_move(220, 80)
    await asyncio.sleep(0.2)
    # depose marron
    tasklifts = asyncio.create_task(goldo_lifts_move(300, 80))
    await servos.moveMultiple(bras_droit_depose_marron, 1)
    await asyncio.sleep(0.2)
    await tasklifts
    await goldo_lift_move(GoldoLift.Right, 143)
    await right_pump_off()
    await asyncio.sleep(0.2)

    # retrait bras droit
    await goldo_lift_move(GoldoLift.Right, 286)
    taskarms = asyncio.create_task(servos.moveMultiple(bras_droit_prise_marron, 1))

    # depose jaune
    await goldo_lift_move(GoldoLift.Left, 571)
    await servos.moveMultiple(bras_gauche_depose_jaune, 1)
    await asyncio.sleep(0.2)
    await goldo_lift_move(GoldoLift.Left, 381)
    await asyncio.sleep(0.2)
    await left_pump_off()
    await asyncio.sleep(0.2)

    # prise rose
    await servos.moveMultiple(bras_gauche_prise_rose, 1)
    await asyncio.sleep(0.2)
    await goldo_lift_move(GoldoLift.Left, 210)
    await left_pump_on()
    await asyncio.sleep(0.2)

    # depose rose
    await goldo_lift_move(GoldoLift.Left, 571)
    await asyncio.sleep(0.2)
    await servos.moveMultiple(bras_gauche_depose_rose, 1)
    await asyncio.sleep(0.2)
    await left_pump_off()
    await taskarms
    await asyncio.sleep(0.2)

    # ecartement bras
    taskarms = asyncio.create_task(servos.moveMultiple(coudes_leves, 1))
    await servos.moveMultiple(epaules_ouvertes, 1)
    await taskarms

async def construction_gateau_bas_bleu():
    await goldo_lifts_move(100, 80)
    await pump_on(True, True)
    # bras au dessus du jaune et du marron
    taskarms = asyncio.create_task(servos.moveMultiple(bras_gauche_prise_jaune, 1))
    await servos.moveMultiple(bras_droit_prise_marron, 1)
    await taskarms
    await asyncio.sleep(0.2)
    # descente pour prise
    await goldo_lifts_move(40, 80)
    await asyncio.sleep(0.2)
    # depose marron
    tasklifts = asyncio.create_task(goldo_lifts_move(100, 80))
    await servos.moveMultiple(bras_droit_depose_marron, 1)
    await asyncio.sleep(0.2)
    await tasklifts
    await goldo_lift_move(GoldoLift.Right, 95)
    await right_pump_off()
    await asyncio.sleep(0.2)

    # retrait bras droit
    await goldo_lift_move(GoldoLift.Right, 95)
    taskarms = asyncio.create_task(servos.moveMultiple(bras_droit_prise_marron, 1))

    # depose jaune
    await goldo_lift_move(GoldoLift.Left, 381)
    await servos.moveMultiple(bras_gauche_depose_jaune, 1)
    await asyncio.sleep(0.2)
    await goldo_lift_move(GoldoLift.Left, 381)
    await left_pump_off()
    await asyncio.sleep(0.1)

    # prise rose
    await servos.moveMultiple(bras_gauche_prise_rose, 1)
    await asyncio.sleep(0.2)
    await goldo_lift_move(GoldoLift.Left, 38)
    await left_pump_on()
    await asyncio.sleep(0.2)

    # depose rose
    await goldo_lift_move(GoldoLift.Left, 571)
    await asyncio.sleep(0.1)
    await servos.moveMultiple(bras_gauche_depose_rose, 1)
    await asyncio.sleep(0.1)
    await left_pump_off()
    await taskarms
    await asyncio.sleep(0.2)

    # ecartement bras
    taskarms = asyncio.create_task(servos.moveMultiple(coudes_leves, 1))
    await servos.moveMultiple(epaules_ouvertes, 1)
    await taskarms
