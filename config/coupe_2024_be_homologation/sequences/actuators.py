import asyncio


class GoldoLift:
    Unknown = 0
    Left = 1
    Right = 2


async def goldo_lift_move(side,pos):
    lift_factor = 1.090
    if (side==GoldoLift.Left):
        await servos.liftsRaw(int(pos*lift_factor), 80, 0, 0)
    if (side==GoldoLift.Right):
        await servos.liftsRaw(0, 0, int(pos*lift_factor), 80)


async def goldo_lifts_move(pos, speed = 80):
    lift_factor = 1.090
    await servos.liftsRaw(int(pos*lift_factor), speed, int(pos*lift_factor), speed)


@robot.sequence
async def goldo_lifts_test_initialize():
    # initialisation ascenseurs    
    await servos.liftDoHoming(0)
    await servos.liftDoHoming(1)
    await asyncio.sleep(3)
    await servos.liftsRaw(65, 60, 65, 60)
    await asyncio.sleep(3)


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
    'epaule_g': 1714,
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

#positions match
prepare_panel_left = {
    'epaule_g': 2042,
    'coude_g': 428
}

prepare_panel_right = {
    'epaule_d': 1923,
    'coude_d': 580
}

hit_panel_left = {
    'epaule_g': 1822,
    'coude_g': 428
}

hit_panel_right = {
    'epaule_d': 2200,
    'coude_d': 580
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
    
    # initialisation ascenseurs    
    await servos.liftDoHoming(0)
    await servos.liftDoHoming(1)
    await asyncio.sleep(3)
    
    await servos.liftsRaw(80, 60, 80, 60)
    await asyncio.sleep(1)
    await servos.moveMultiple(epaules_rentrees, speed=0.7)
    await servos.setMaxTorque(['epaule_g', 'epaule_d'], 1)
    await servos.setMaxTorque(['coude_g', 'coude_d'], 1)

@robot.sequence
async def arms_safe():
    # Init bras
    await servos.moveMultiple(coudes_leves, speed=0.7)
    await asyncio.sleep(0.2)
    await servos.moveMultiple(epaules_devant, speed=0.7)
    await asyncio.sleep(0.5)
    await servos.moveMultiple(epaules_rentrees, speed=0.7)

@robot.sequence
async def arms_collect():
    await servos.moveMultiple(epaules_ouvertes, speed=0.7)

@robot.sequence
async def arms_down():
    await servos.liftsRaw(80, 60, 80, 60)    

@robot.sequence
async def lift_left_solar_panel():
    await goldo_lift_move(GoldoLift.Left,900)

@robot.sequence
async def lift_right_solar_panel():
    await goldo_lift_move(GoldoLift.Right,900)

@robot.sequence
async def prepare_solar_panel_left():
    await servos.setMaxTorque(['epaule_g', 'epaule_d'], 0.20)
    await servos.setMaxTorque(['coude_g', 'coude_d'], 0.20)
    await servos.moveMultiple(prepare_panel_left, speed = 1)

@robot.sequence
async def prepare_solar_panel_right():
    await servos.setMaxTorque(['epaule_g', 'epaule_d'], 0.20)
    await servos.setMaxTorque(['coude_g', 'coude_d'], 0.20)
    await servos.moveMultiple(prepare_panel_right, speed = 1)

@robot.sequence
async def hit_solar_panel_left():
    await servos.setMaxTorque(['epaule_g', 'epaule_d'], 0.20)
    await servos.setMaxTorque(['coude_g', 'coude_d'], 0.20)

    await servos.moveMultiple(hit_panel_left, speed = 1)
    await asyncio.sleep(0.2)
    await servos.moveMultiple(prepare_panel_left, speed = 1)

@robot.sequence
async def hit_solar_panel_right():
    await servos.setMaxTorque(['epaule_g', 'epaule_d'], 0.20)
    await servos.setMaxTorque(['coude_g', 'coude_d'], 0.20)

    await servos.moveMultiple(hit_panel_right, speed = 1)
    await asyncio.sleep(0.2)
    await servos.moveMultiple(prepare_panel_right, speed = 1)