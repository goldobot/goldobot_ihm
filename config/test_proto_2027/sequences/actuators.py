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

@robot.sequence
async def lifts_high():
    await goldo_lifts_move(pos = 950, speed = 80)
    await asyncio.sleep(0.3)


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


