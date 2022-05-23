import asyncio

from numpy import true_divide

class Side:
    Unknown = 0
    Blue = 1
    Yellow = 2

mors_d_closed = 12
mors_d_opened = 1023
mors_g_closed = 4
mors_g_opened = 1023

chariot_g_mid = 512
chariot_d_mid = 512
chariot_g_closed = 0
chariot_d_closed = 0
chariot_g_opened = 1023

lift_up = 3379
lift_tryohm = 2393
lift_push_square = 1355

#replica
lift_wait_replica = 805
mors_d_wait_replica = 761
chariot_d_wait_replica = 371
mors_g_wait_replica = 760
chariot_g_wait_replica = 372

lift_take_replica = 482
mors_d_take_replica = 721
chariot_d_take_replica = 340
mors_g_take_replica = 722
chariot_g_take_replica = 353

truc = False

#tryohm
mors_opened = {
    'mors_g': mors_g_opened,
    'mors_d': mors_d_opened
}

mors_closed = {
    'mors_g': mors_g_closed,
    'mors_d': mors_d_closed
}

chariot_opened = {
    'chariot_g': chariot_g_mid,
    'chariot_d': chariot_d_mid
}

chariot_closed = {
    'chariot_g': chariot_g_closed,
    'chariot_d': chariot_d_closed
}


@robot.sequence
async def initialize_pince():
    await servos.setMaxTorque(['chariot_g', 'chariot_d', 'mors_g', 'mors_d'], 0.50)    
    await servos.setEnable(['chariot_g', 'chariot_d'], False)
    await servos.setEnable(['mors_g', 'mors_d'], True)
    await servos.moveMultiple(mors_opened, 0.8)
    await servos.setMaxTorque(['chariot_g', 'chariot_d', 'mors_g', 'mors_d'], 0.5)    
    await servos.moveMultiple(mors_closed, 1.0)
    await servos.setEnable(['chariot_g', 'chariot_d'], True)
    await servos.moveMultiple(chariot_opened, 1.0)
    await asyncio.sleep(0.3)
    await servos.moveMultiple(chariot_closed, 1.0)
    await asyncio.sleep(1)
    await servos.setEnable(['chariot_g', 'chariot_d', 'mors_g', 'mors_d'], False)

@robot.sequence
async def take_replica_right():
    await servos.setMaxTorque(['chariot_g', 'chariot_d', 'mors_g', 'mors_d', 'lift_pince'], 0.80)    
    await servos.setEnable(['chariot_g', 'chariot_d'], True)
    await servos.setEnable(['mors_g', 'mors_d','lift_pince'], True)

    await servos.moveMultiple({'lift_pince': lift_wait_replica}, 0.8)
    await servos.moveMultiple({'chariot_d': chariot_d_wait_replica}, 0.8)
    await servos.moveMultiple({'mors_d': mors_d_wait_replica}, 0.8)

    while sensors['sick_lat_d'] == True:
        await asyncio.sleep(0.1)
        
    await asyncio.sleep(5)
    await servos.moveMultiple({'lift_pince': lift_take_replica}, 0.8)
    await servos.moveMultiple({'chariot_d': chariot_d_take_replica}, 0.8)
    await servos.moveMultiple({'mors_d': mors_d_take_replica}, 0.8)

    await asyncio.sleep(1)

@robot.sequence
async def take_replica_left():
    await servos.setMaxTorque(['chariot_g', 'mors_g', 'lift_pince'], 0.80)    
    await servos.setEnable(['chariot_g'], True)
    await servos.setEnable(['mors_g', 'lift_pince'], True)

    await servos.moveMultiple({'lift_pince': lift_wait_replica}, 0.8)
    await servos.moveMultiple({'chariot_g': chariot_g_wait_replica}, 0.8)
    await servos.moveMultiple({'mors_g': mors_g_wait_replica}, 0.8)

    while sensors['sick_lat_g'] == True:
        await asyncio.sleep(0.1)
        
    await asyncio.sleep(5)
    await servos.moveMultiple({'lift_pince': lift_take_replica}, 0.8)
    await servos.moveMultiple({'chariot_g': chariot_d_take_replica}, 0.8)
    await servos.moveMultiple({'mors_g': mors_d_take_replica}, 0.8)

    await asyncio.sleep(1)

async def open_chariot():
    await servos.moveMultiple({'chariot_g': chariot_g_opened}, 0.4)
    truc = True
    return

@robot.sequence
async def measure_tryohm_left():
    tryohm_val = None
    push = False
    truc = False
    await servos.setMaxTorque(['chariot_g', 'mors_g'], 0.50)
    await servos.setMaxTorque(['lift_pince'], 1)
    await servos.setEnable(['chariot_g', 'mors_g', 'lift_pince'], True)
    await servos.moveMultiple({'mors_g': mors_g_closed}, 0.4)
    await servos.moveMultiple({'lift_pince': lift_tryohm}, 1)
    task = asyncio.create_task(open_chariot())
    while robot.tryOhm == None and truc == False:
        await asyncio.sleep(0.01)
    task.cancel()
    tryohm_val = robot.tryOhm
    await servos.moveMultiple({'lift_pince': lift_tryohm+400, 'chariot_g': servos.states['chariot_g'].measured_position}, 1)
    await servos.moveMultiple({'chariot_g': 300}, 1)
    if robot.side == Side.Blue and tryohm_val == 'purple':
        push = True
    elif robot.side == Side.Yellow and tryohm_val == 'yellow':
        push = True
    if push:
        await servos.setMaxTorque(['chariot_g'], 1)
        await servos.moveMultiple({'lift_pince': lift_push_square}, 1)
        await servos.moveMultiple({'chariot_g':chariot_g_opened}, 1)
        await asyncio.sleep(0.5)
        await servos.moveMultiple({'chariot_g':chariot_g_closed}, 1)