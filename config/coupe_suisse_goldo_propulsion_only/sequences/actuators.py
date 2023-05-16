import asyncio


class GoldoLift:
    Unknown = 0
    Left = 1
    Right = 2


async def goldo_lift_move(side,pos):
    pass

async def goldo_lifts_move(pos, speed = 80):
    pass


async def pump_on(left, right):
    pass


async def pump_off(left, right):
    pass

@robot.sequence
async def left_pump_on():
    pass

@robot.sequence
async def left_pump_off():
    pass

@robot.sequence
async def right_pump_on():
    pass

@robot.sequence
async def right_pump_off():
    pass


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
#bras_droit_prise_jaune = {
#    'epaule_d': 3124,
#    'coude_d': 515
#}
bras_droit_prise_jaune = {
    'epaule_d': 3124,
    'coude_d': 530
}

bras_droit_depose_jaune = {
    'epaule_d': 1499,
    'coude_d': 515
}

# Cote rose
#bras_droit_prise_rose = {
#    'epaule_d': 2411,
#    'coude_d': 515
#}
bras_droit_prise_rose = {
    'epaule_d': 2411,
    'coude_d': 530
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
    'coude_d': 520
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
    pass


@robot.sequence
async def arms_open():
    pass

@robot.sequence
async def arms_take():
    pass

@robot.sequence
async def arms_centering():
    pass

@robot.sequence
async def arms_close():
    pass

# Constructions vertes
@robot.sequence
async def construction_gateau_haut_vert():
    pass

@robot.sequence
async def construction_gateau_milieu_vert():
    pass

@robot.sequence
async def construction_gateau_bas_vert():
    pass


@robot.sequence
async def test_prise_gauche():
    pass

# Constructions bleues
async def construction_gateau_haut_bleu():
    pass

async def construction_gateau_haut_bleu():
    pass

async def construction_gateau_bas_bleu():
    pass
