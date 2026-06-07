import asyncio
import copy


global_lift_left_bias = 10
global_lift_factor = 1.090

global_drop_height = 240
global_grab_height = 180
#global_grab_height = 190
global_lift_prep_take = 400

global_grab_x_bias = 0

class GoldoLift:
    Unknown = 0
    Left = 1
    Right = 2

def set_global_grab_height(val):
    global global_grab_height
    global_grab_height = val

def set_global_grab_x_bias(val):
    global global_grab_x_bias
    global_grab_x_bias = val

async def goldo_lift_move(side,pos):
    global global_lift_factor
    global global_lift_left_bias
    if (side==GoldoLift.Left):
        await servos.liftsRaw(int((pos+global_lift_left_bias)*global_lift_factor), 80, 0, 0)
    if (side==GoldoLift.Right):
        await servos.liftsRaw(0, 0, int(pos*global_lift_factor), 80)

async def goldo_lift_left_move(pos):
    global global_lift_factor
    global global_lift_left_bias
    await servos.liftsRaw(int((pos+global_lift_left_bias)*global_lift_factor), 80, 0, 0)

async def goldo_lift_right_move(pos):
    global global_lift_factor
    global global_lift_left_bias
    await servos.liftsRaw(0, 0, int(pos*global_lift_factor), 80)

async def goldo_lifts_move(pos, speed = 80):
    global global_lift_factor
    global global_lift_left_bias
    await servos.liftsRaw(int((pos+global_lift_left_bias)*global_lift_factor), speed, int(pos*global_lift_factor), speed)


async def pump_on(left, right):
    if left:
        await robot.gpioSet('pompe_g', True)
        await robot.gpioSet('pompe_g', True)
        await robot.gpioSet('pompe_g', True)
    if right:
        await robot.gpioSet('pompe_d', True)
        await robot.gpioSet('pompe_d', True)
        await robot.gpioSet('pompe_d', True)


async def pump_off(left, right):
    if left:
        await robot.gpioSet('pompe_g', False)
        await robot.gpioSet('pompe_g', False)
        await robot.gpioSet('pompe_g', False)
    if right:
        await robot.gpioSet('pompe_d', False)
        await robot.gpioSet('pompe_d', False)
        await robot.gpioSet('pompe_d', False)

@robot.sequence
async def pumps_on():
    await pump_on(True, True)

@robot.sequence
async def pumps_off():
    await pump_off(True, True)

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


arms_initialize_epaules_devant = {
    'epaule_g': 2052,
    'epaule_d': 2035
}

arms_initialize_epaules_rentrees = {
    'epaule_g': 2952,
    'epaule_d': 1131
}

arms_initialize_coudes_leves = {
    'coude_g': 827,
    'coude_d': 204
}

@robot.sequence
async def arms_initialize():

    # Activation dynamixels
    await servos.setMaxTorque(['epaule_g', 'epaule_d'], 0.30)
    await asyncio.sleep(0.1)
    await servos.setMaxTorque(['coude_g', 'coude_d'], 0.20)
    await asyncio.sleep(0.1)
    
    await servos.setEnable(['epaule_g', 'epaule_d'], True)
    await asyncio.sleep(0.1)
    await servos.setEnable(['coude_g', 'coude_d'], True)
    await asyncio.sleep(0.1)
    
    # Init bras
    await servos.moveMultiple(arms_initialize_epaules_devant, speed=0.7)
    await asyncio.sleep(0.2)
    await servos.moveMultiple(arms_initialize_coudes_leves, speed=0.7)
    await asyncio.sleep(0.2)
    
    # initialisation ascenseurs    
    await servos.liftDoHoming(0)
    await servos.liftDoHoming(1)
    await asyncio.sleep(2.0)
    
#    await servos.liftsRaw(120, 60, 120, 60)
    await goldo_lifts_move(pos = 120, speed = 80)
    await asyncio.sleep(1)
    await servos.moveMultiple(arms_initialize_epaules_rentrees, speed=0.7)
    await asyncio.sleep(0.1)
    await servos.setMaxTorque(['epaule_g', 'epaule_d'], 1)
    await asyncio.sleep(0.1)
    await servos.setMaxTorque(['coude_g', 'coude_d'], 1)
    await asyncio.sleep(0.1)


@robot.sequence
async def arms_disable():
    await servos.setMaxTorque(['epaule_g', 'epaule_d'], 0.0)
    await asyncio.sleep(0.1)
    await servos.setMaxTorque(['coude_g', 'coude_d'], 0.0)
    await asyncio.sleep(0.1)
    await servos.setEnable(['epaule_g', 'epaule_d'], False)
    await asyncio.sleep(0.1)
    await servos.setEnable(['coude_g', 'coude_d'], False)
    await asyncio.sleep(0.1)
    # WTF ?!!!!
    await servos.moveMultiple(arms_initialize_epaules_devant, speed=0.7)
    await asyncio.sleep(0.2)
    await servos.moveMultiple(arms_initialize_coudes_leves, speed=0.7)
    await asyncio.sleep(0.2)
    

@robot.sequence
async def arms_final_state():
    await pumps_off()
    await asyncio.sleep(0.1)
    await arms_close()
    await asyncio.sleep(0.1)


@robot.sequence
async def lifts_high():
    await goldo_lifts_move(pos = 950, speed = 80)
    await asyncio.sleep(0.3)


arms_open_epaules_ouvertes = {
    'epaule_g': 1609,
    'epaule_d': 2277
}

arms_open_coudes_leves = {
    'coude_g': 827,
    'coude_d': 204
}

@robot.sequence
async def arms_open():
    await servos.moveMultiple(arms_open_epaules_ouvertes, speed=1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple(arms_open_coudes_leves, speed=1)
    await asyncio.sleep(0.1)


arms_open_extreme_epaules_ouvertes = {
    'epaule_g': 1090,
    'epaule_d': 3000
}

arms_open_extreme_coudes_leves = {
    'coude_g': 827,
    'coude_d': 204
}

@robot.sequence
async def arms_open_extreme():
    await servos.moveMultiple(arms_open_extreme_epaules_ouvertes, speed=1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple(arms_open_extreme_coudes_leves, speed=1)
    await asyncio.sleep(0.1)


arms_close_epaules_rentrees = {
    'epaule_g': 2952,
    'epaule_d': 1131
}

arms_close_coudes_leves = {
    'coude_g': 827,
    'coude_d': 204
}

@robot.sequence
async def arms_close():
    await servos.moveMultiple(arms_close_epaules_rentrees, speed=1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple(arms_close_coudes_leves, speed=1)
    await asyncio.sleep(0.1)

arms_close_epaules_rentrees_extreme = {
    'epaule_g': 3050,
    'epaule_d': 1030
}

@robot.sequence
async def arms_close_extreme():
    await servos.moveMultiple(arms_close_coudes_leves, speed=1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple(arms_close_epaules_rentrees_extreme, speed=1)
    await asyncio.sleep(0.1)


position_defensive_laterale_epaules_ouvertes = {
    'epaule_g': 1090,
    'epaule_d': 3000
}

position_defensive_laterale_coudes_leves = {
    'coude_g': 827,
    'coude_d': 204
}

@robot.sequence
async def position_defensive_laterale():
    await goldo_lifts_move(pos = 800, speed = 80)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(position_defensive_laterale_epaules_ouvertes, speed=1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple(position_defensive_laterale_coudes_leves, speed=1)
    await asyncio.sleep(0.1)


position_defensive_laterale_servos_d = {
    'epaule_d': 3000,
    'coude_d': 204
}

@robot.sequence
async def position_defensive_laterale_d():
    await goldo_lift_move(GoldoLift.Right,800)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(position_defensive_laterale_servos_d, speed=1)
    await asyncio.sleep(0.1)


position_defensive_laterale_servos_g = {
    'epaule_g': 1090,
    'coude_g': 827
}

@robot.sequence
async def position_defensive_laterale_g():
    await goldo_lift_move(GoldoLift.Left,800)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(position_defensive_laterale_servos_g, speed=1)
    await asyncio.sleep(0.1)


### PREP TAKE ###
0
bras_d_prep_take = {
    'epaule_d': 1400,
    'coude_d': 204,
}

@robot.sequence
async def arm_right_prep_take():
    global global_lift_prep_take
    await goldo_lift_move(GoldoLift.Right, global_lift_prep_take)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(bras_d_prep_take, speed=1)
    await asyncio.sleep(0.1)


bras_g_prep_take = {
    'epaule_g': 2740,
    'coude_g': 824,
}

@robot.sequence
async def arm_left_prep_take():
    global global_lift_prep_take
    await goldo_lift_move(GoldoLift.Left, global_lift_prep_take)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(bras_g_prep_take, speed=1)
    await asyncio.sleep(0.1)

bras_d_g_prep_take = {
    'epaule_d': 1400,
    'coude_d': 204,
    'epaule_g': 2740,
    'coude_g': 824,
}

@robot.sequence
async def arm_right_left_prep_take():
    global global_lift_prep_take
    await goldo_lifts_move(pos = global_lift_prep_take, speed = 80)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(bras_d_g_prep_take, speed=1)
    await asyncio.sleep(0.1)


### GRAB X ("SOUTH->NORTH" ALIGNEMENT) ###

bras_d_take = {
    'epaule_d': 1400,
#    'coude_d': 530,
    'coude_d': 545,
}

@robot.sequence
async def arm_right_take():
    global global_grab_height
    global global_grab_x_bias
    bras_dico = copy.deepcopy(bras_d_take)
    bras_dico['epaule_d'] += global_grab_x_bias
    await servos.moveMultiple(bras_dico, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lift_move(GoldoLift.Right,global_grab_height)
    await asyncio.sleep(0.3)
@robot.sequence
async def arm_right_drop():
    global global_drop_height
    await servos.moveMultiple(bras_d_take, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lift_move(GoldoLift.Right,global_drop_height)
    await asyncio.sleep(0.3)


bras_g_take = {
    'epaule_g': 2740,
#    'coude_g': 497,
    'coude_g': 485,
}

@robot.sequence
async def arm_left_take():
    global global_grab_height
    global global_grab_x_bias
    bras_dico = copy.deepcopy(bras_g_take)
    bras_dico['epaule_g'] += global_grab_x_bias
    await servos.moveMultiple(bras_dico, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lift_move(GoldoLift.Left,global_grab_height)
    await asyncio.sleep(0.3)
@robot.sequence
async def arm_left_drop():
    global global_drop_height
    await servos.moveMultiple(bras_g_take, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lift_move(GoldoLift.Left,global_drop_height)
    await asyncio.sleep(0.3)


### GRAB Y ("EAST->WEST" ALIGNEMENT) ###

# EXPERIMENTAL
# max -30mm : 1838
# +134
# nominal   : 1704
# -134
# max +30mm : 1570
bras_d_take_y_0 = {
    'epaule_d': 1704,
#    'coude_d': 530,
    'coude_d': 545,
}
@robot.sequence
async def arm_right_take_y_0(y_shift_mm=0.0):
    global global_grab_height
    if (abs(y_shift_mm)>30.0): return
    bras_dico = copy.deepcopy(bras_d_take_y_0)
    if (y_shift_mm<0.0):
        bras_dico['epaule_d'] += int((134)*abs(y_shift_mm)/30.0)
    elif (y_shift_mm>0.0):
        bras_dico['epaule_d'] += int((-134)*abs(y_shift_mm)/30.0)
    await servos.moveMultiple(bras_dico, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lift_move(GoldoLift.Right,global_grab_height)
    await asyncio.sleep(0.3)

# EXPERIMENTAL
# max -30mm : 1628
# +140
# nominal   : 1488
# -151
# max +30mm : 1337
bras_d_take_y_1 = {
    'epaule_d': 1488,
#    'coude_d': 530,
    'coude_d': 545,
}
@robot.sequence
async def arm_right_take_y_1(y_shift_mm=0.0):
    global global_grab_height
    if (abs(y_shift_mm)>30.0): return
    bras_dico = copy.deepcopy(bras_d_take_y_1)
    if (y_shift_mm<0.0):
        bras_dico['epaule_d'] += int((140)*abs(y_shift_mm)/30.0)
    elif (y_shift_mm>0.0):
        bras_dico['epaule_d'] += int((-151)*abs(y_shift_mm)/30.0)
    await servos.moveMultiple(bras_dico, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lift_move(GoldoLift.Right,global_grab_height)
    await asyncio.sleep(0.3)

# EXPERIMENTAL
# max -30mm : 1398
# +162
# nominal   : 1240
# -126
# max +30mm : 1114
bras_d_take_y_2 = {
    'epaule_d': 1240,
#    'coude_d': 530,
    'coude_d': 545,
}
@robot.sequence
async def arm_right_take_y_2(y_shift_mm=0.0):
    global global_grab_height
    if (abs(y_shift_mm)>30.0): return
    bras_dico = copy.deepcopy(bras_d_take_y_2)
    if (y_shift_mm<0.0):
        bras_dico['epaule_d'] += int((162)*abs(y_shift_mm)/30.0)
    elif (y_shift_mm>0.0):
        bras_dico['epaule_d'] += int((-126)*abs(y_shift_mm)/30.0)
    await servos.moveMultiple(bras_dico, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lift_move(GoldoLift.Right,global_grab_height)
    await asyncio.sleep(0.3)


# EXPERIMENTAL
# max -30mm : 2514
# +139
# nominal   : 2375
# -121
# max +30mm : 2254
bras_g_take_y_0 = {
    'epaule_g': 2375,
#    'coude_g': 497,
    'coude_g': 485,
}
@robot.sequence
async def arm_left_take_y_0(y_shift_mm=0.0):
    global global_grab_height
    if (abs(y_shift_mm)>30.0): return
    bras_dico = copy.deepcopy(bras_g_take_y_0)
    if (y_shift_mm<0.0):
        bras_dico['epaule_g'] += int((139)*abs(y_shift_mm)/30.0)
    elif (y_shift_mm>0.0):
        bras_dico['epaule_g'] += int((-121)*abs(y_shift_mm)/30.0)
    await servos.moveMultiple(bras_dico, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lift_move(GoldoLift.Left,global_grab_height)
    await asyncio.sleep(0.3)

# EXPERIMENTAL
# max -30mm : 2733
# +141
# nominal   : 2592
# -133
# max +30mm : 2459
bras_g_take_y_1 = {
    'epaule_g': 2592,
#    'coude_g': 497,
    'coude_g': 485,
}
@robot.sequence
async def arm_left_take_y_1(y_shift_mm=0.0):
    global global_grab_height
    if (abs(y_shift_mm)>30.0): return
    bras_dico = copy.deepcopy(bras_g_take_y_1)
    if (y_shift_mm<0.0):
        bras_dico['epaule_g'] += int((141)*abs(y_shift_mm)/30.0)
    elif (y_shift_mm>0.0):
        bras_dico['epaule_g'] += int((-133)*abs(y_shift_mm)/30.0)
    await servos.moveMultiple(bras_dico, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lift_move(GoldoLift.Left,global_grab_height)
    await asyncio.sleep(0.3)

# EXPERIMENTAL
# max -30mm : 2976
# +124
# nominal   : 2852
# -161
# max +30mm : 2691
bras_g_take_y_2 = {
    'epaule_g': 2852,
#    'coude_g': 497,
    'coude_g': 485,
}
@robot.sequence
async def arm_left_take_y_2(y_shift_mm=0.0):
    global global_grab_height
    if (abs(y_shift_mm)>30.0): return
    bras_dico = copy.deepcopy(bras_g_take_y_2)
    if (y_shift_mm<0.0):
        bras_dico['epaule_g'] += int((124)*abs(y_shift_mm)/30.0)
    elif (y_shift_mm>0.0):
        bras_dico['epaule_g'] += int((-161)*abs(y_shift_mm)/30.0)
    await servos.moveMultiple(bras_dico, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lift_move(GoldoLift.Left,global_grab_height)
    await asyncio.sleep(0.3)


#bras_d_g_take_y_0_0 = bras_d_take_y_0 | bras_g_take_y_0
bras_d_g_take_y_0_0 = {}
bras_d_g_take_y_0_0.update(bras_d_take_y_0)
bras_d_g_take_y_0_0.update(bras_g_take_y_0)
@robot.sequence
async def arm_right_left_take_y_0_0(y_shift_mm=0.0):
    global global_grab_height
    if (abs(y_shift_mm)>30.0): return
    bras_dico = copy.deepcopy(bras_d_g_take_y_0_0)
    if (y_shift_mm<0.0):
        bras_dico['epaule_d'] += int((134)*abs(y_shift_mm)/30.0)
        bras_dico['epaule_g'] += int((139)*abs(y_shift_mm)/30.0)
    elif (y_shift_mm>0.0):
        bras_dico['epaule_d'] += int((-134)*abs(y_shift_mm)/30.0)
        bras_dico['epaule_g'] += int((-121)*abs(y_shift_mm)/30.0)
    await servos.moveMultiple(bras_dico, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lifts_move(pos = global_grab_height, speed = 60)
    await asyncio.sleep(0.3)
@robot.sequence
async def arm_right_left_drop_y_0_0():
    global global_drop_height
    await servos.moveMultiple(bras_d_g_take_y_0_0, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lifts_move(pos = global_drop_height, speed = 60)
    await asyncio.sleep(0.3)


#bras_d_g_take_y_0_1 = bras_d_take_y_0 | bras_g_take_y_1
bras_d_g_take_y_0_1 = {}
bras_d_g_take_y_0_1.update(bras_d_take_y_0)
bras_d_g_take_y_0_1.update(bras_g_take_y_1)
@robot.sequence
async def arm_right_left_take_y_0_1(y_shift_mm=0.0):
    global global_grab_height
    if (abs(y_shift_mm)>30.0): return
    bras_dico = copy.deepcopy(bras_d_g_take_y_0_1)
    if (y_shift_mm<0.0):
        bras_dico['epaule_d'] += int((134)*abs(y_shift_mm)/30.0)
        bras_dico['epaule_g'] += int((141)*abs(y_shift_mm)/30.0)
    elif (y_shift_mm>0.0):
        bras_dico['epaule_d'] += int((-134)*abs(y_shift_mm)/30.0)
        bras_dico['epaule_g'] += int((-133)*abs(y_shift_mm)/30.0)
    await servos.moveMultiple(bras_dico, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lifts_move(pos = global_grab_height, speed = 60)
    await asyncio.sleep(0.3)

#bras_d_g_take_y_1_0 = bras_d_take_y_1 | bras_g_take_y_0
bras_d_g_take_y_1_0 = {}
bras_d_g_take_y_1_0.update(bras_d_take_y_1)
bras_d_g_take_y_1_0.update(bras_g_take_y_0)
@robot.sequence
async def arm_right_left_take_y_1_0(y_shift_mm=0.0):
    global global_grab_height
    if (abs(y_shift_mm)>30.0): return
    bras_dico = copy.deepcopy(bras_d_g_take_y_1_0)
    if (y_shift_mm<0.0):
        bras_dico['epaule_d'] += int((140)*abs(y_shift_mm)/30.0)
        bras_dico['epaule_g'] += int((139)*abs(y_shift_mm)/30.0)
    elif (y_shift_mm>0.0):
        bras_dico['epaule_d'] += int((-151)*abs(y_shift_mm)/30.0)
        bras_dico['epaule_g'] += int((-121)*abs(y_shift_mm)/30.0)
    await servos.moveMultiple(bras_dico, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lifts_move(pos = global_grab_height, speed = 60)
    await asyncio.sleep(0.3)

#bras_d_g_take_y_1_1 = bras_d_take_y_1 | bras_g_take_y_1
bras_d_g_take_y_1_1 = {}
bras_d_g_take_y_1_1.update(bras_d_take_y_1)
bras_d_g_take_y_1_1.update(bras_g_take_y_1)
@robot.sequence
async def arm_right_left_take_y_1_1(y_shift_mm=0.0):
    global global_grab_height
    if (abs(y_shift_mm)>30.0): return
    bras_dico = copy.deepcopy(bras_d_g_take_y_1_1)
    if (y_shift_mm<0.0):
        bras_dico['epaule_d'] += int((140)*abs(y_shift_mm)/30.0)
        bras_dico['epaule_g'] += int((141)*abs(y_shift_mm)/30.0)
    elif (y_shift_mm>0.0):
        bras_dico['epaule_d'] += int((-151)*abs(y_shift_mm)/30.0)
        bras_dico['epaule_g'] += int((-133)*abs(y_shift_mm)/30.0)
    await servos.moveMultiple(bras_dico, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lifts_move(pos = global_grab_height, speed = 60)
    await asyncio.sleep(0.3)
@robot.sequence
async def arm_right_left_drop_y_1_1():
    global global_drop_height
    await servos.moveMultiple(bras_d_g_take_y_1_1, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lifts_move(pos = global_drop_height, speed = 60)
    await asyncio.sleep(0.3)

bras_d_g_drop_y_42 = {
    'epaule_d': 2000,
#    'coude_d': 530,
    'coude_d': 545,
    'epaule_g': 2010,
#    'coude_g': 497,
    'coude_g': 485,
}
@robot.sequence
async def arm_right_left_drop_y_42():
    global global_drop_height
    await servos.moveMultiple(bras_d_g_drop_y_42, speed=1)
    await asyncio.sleep(0.1)
    await goldo_lifts_move(pos = global_drop_height, speed = 60)
    await asyncio.sleep(0.3)


@robot.sequence
async def sleight_of_hand_prep():
    await arms_close_extreme()
    await asyncio.sleep(0.2)
    await left_pump_on()
    await asyncio.sleep(0.2)
    await right_pump_off()
    await asyncio.sleep(0.5)
    await position_defensive_laterale_d()
    await asyncio.sleep(0.2)

@robot.sequence
async def sleight_of_hand_drop():
    await asyncio.sleep(0.2)
    await arm_left_drop()
    await asyncio.sleep(0.2)
    await left_pump_off()
    await asyncio.sleep(0.2)
    await position_defensive_laterale_g()
    await asyncio.sleep(0.2)

@robot.sequence
async def sleight_of_hand():
    await sleight_of_hand_prep()
    await sleight_of_hand_drop()


### THERMO ###

@robot.sequence
async def arms_prep_thermo():
    await arms_close()
    await asyncio.sleep(0.1)
    await lifts_high()
    await asyncio.sleep(0.3)


bras_g_push_thermo = {
#    'epaule_g': 2090,
#    'epaule_g': 2030,
    'epaule_g': 1950,
    'coude_g': 490,
}

@robot.sequence
async def arm_left_push_thermo():
    await goldo_lift_move(GoldoLift.Left,950)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(bras_g_push_thermo, speed=0.5)
    await asyncio.sleep(0.1)


bras_d_push_thermo = {
#    'epaule_d': 2090,
#    'epaule_d': 2150,
    'epaule_d': 2230,
#    'coude_d': 490,
    'coude_d': 530,
}

@robot.sequence
async def arm_right_push_thermo():
    await goldo_lift_move(GoldoLift.Right,950)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(bras_d_push_thermo, speed=0.5)
    await asyncio.sleep(0.1)



## TESTS ##

@robot.sequence
async def test_grab_right():
    #await arm_right_prep_take()
    #await asyncio.sleep(0.1)
    await right_pump_on()
    await asyncio.sleep(0.1)
    await arm_right_take()
    await asyncio.sleep(0.1)
    await position_defensive_laterale_d()
    await asyncio.sleep(0.1)


@robot.sequence
async def test_grab_left():
    #await arm_left_prep_take()
    #await asyncio.sleep(0.1)
    await left_pump_on()
    await asyncio.sleep(0.1)
    await arm_left_take()
    await asyncio.sleep(0.1)
    await position_defensive_laterale_g()
    await asyncio.sleep(0.1)


@robot.sequence
async def test_crazy_grab():
    # Propulsion
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    
    await test_grab_right()
    await asyncio.sleep(0.5)

    await propulsion.translation(0.05, 0.2)
    await asyncio.sleep(0.5)

    await test_grab_left()
    await asyncio.sleep(0.5)


@robot.sequence
async def goldo_lifts_test_initialize():
    # initialisation ascenseurs    
    await servos.liftDoHoming(0)
    await servos.liftDoHoming(1)
    await asyncio.sleep(6)
    await servos.liftsRaw(65, 60, 65, 60)
    await asyncio.sleep(3)


@robot.sequence
async def goldo_lifts_test_pos_0():
    await goldo_lifts_move(0,25)

@robot.sequence
async def goldo_lifts_test_pos_65():
    await goldo_lifts_move(65,25)

@robot.sequence
async def goldo_lifts_test_pos_200():
    await goldo_lifts_move(200,25)

@robot.sequence
async def goldo_lifts_test_pos_250():
    await goldo_lifts_move(400,25)

@robot.sequence
async def goldo_lifts_test_pos_600():
    await goldo_lifts_move(600,25)

@robot.sequence
async def goldo_lifts_test_pos_800():
    await goldo_lifts_move(800,25)

@robot.sequence
async def goldo_lifts_test_pos_1000():
    await goldo_lifts_move(1000,25)


