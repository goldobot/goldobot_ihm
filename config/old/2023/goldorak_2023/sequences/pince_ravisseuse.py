import asyncio

from numpy import true_divide

import inspect

def debug_goldo(caller):
    print ()
    print ("************************************************")
    print (" GOLDO DEBUG :  {:32s}".format(inspect.currentframe().f_back.f_code.co_name))
    print ("************************************************")
    print ()

class Side:
    Unknown = 0
    Purple = 1
    Yellow = 2

mors_d_closed = 12
mors_d_opened = 1023
mors_g_closed = 4
mors_g_opened = 1023

chariot_g_mid = 512
chariot_d_mid = 512
chariot_g_closed = 130
chariot_d_closed = 130
chariot_g_opened = 1023
chariot_d_opened = 1023

lift_up = 3379
# FIXME : TODO : remove
#lift_tryohm = 2393
lift_tryohm = 2400
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
mors_g_hold_replica = 700
# FIXME : TODO : remove
#chariot_g_take_replica = 353
chariot_g_take_replica = 335

lift_pos_put_replica = 1552

#distributeur
lift_distributeur = 550
chariot_distributeur = 662
mors_distributeur = 580


#tryohm
mors_opened = {
    'mors_g': mors_g_opened,
    'mors_d': mors_d_opened
}

mors_closed = {
    'mors_g': mors_g_closed,
    'mors_d': mors_d_closed
}

pince_d_opened = {
    'mors_d': mors_d_opened,
    'chariot_d': chariot_d_opened
}

chariot_opened = {
    'chariot_g': chariot_g_mid,
    'chariot_d': chariot_d_mid
}

chariot_closed = {
    'chariot_g': chariot_g_closed,
    'chariot_d': chariot_d_closed
}

pince_left_init_pos = {
    'mors_g': mors_g_closed,
    'chariot_g': chariot_g_closed,
}

pince_right_init_pos = {
    'mors_d': mors_d_closed,
    'chariot_d': chariot_d_closed,
}

pince_d_prise_distrib = {
    'mors_d': 580,
    'chariot_d': 662
}

lift_pre_storage = 2950
lift_storage_ = 2872
chariot_d_storage_d = 295

@robot.sequence
async def prise_distri_d():
    await servos.setEnable(['chariot_d', 'mors_d', 'lift_pince'], True)
    await servos.setMaxTorque(['chariot_d', 'mors_d','lift_pince'], 0.80)
    await lift_pince_top()
    await servos.moveMultiple(pince_d_opened, 1.0)
    await servos.moveMultiple({'lift_pince': lift_distributeur}, 1.0)
    await servos.moveMultiple(pince_d_prise_distrib, 1.0)
    await servos.moveMultiple({'lift_pince':lift_pre_storage}, 1.0)
    if(sensors['sick_lat_d'] == False):
        await servos.moveMultiple({'chariot_d', chariot_d_storage_d}, 1.0)
        await servos.moveMultiple({'lift_pince':lift_storage}, 1.0)

@robot.sequence
async def disable_pince():
    await servos.setEnable(['chariot_g', 'chariot_d', 'mors_d', 'mors_g', 'lift_pince'], False)

@robot.sequence
async def disable_pince_only():
    await servos.setEnable(['chariot_g', 'chariot_d', 'mors_d', 'mors_g'], False)

@robot.sequence
async def initialize_pince():
    debug_goldo(__name__)

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
async def close_pince():
    await servos.setMaxTorque(['chariot_g', 'chariot_d', 'mors_g', 'mors_d'], 0.80)    
    await servos.setEnable(['chariot_g', 'chariot_d'], True)
    await servos.setEnable(['mors_g', 'mors_d'], True)
    await servos.moveMultiple(mors_closed, 1.0)
    await servos.moveMultiple(chariot_closed, 1.0)

@robot.sequence
async def take_replica_right():
    debug_goldo(__name__)

    await servos.setMaxTorque(['chariot_g', 'chariot_d', 'mors_g', 'mors_d', 'lift_pince'], 0.80)    
    await servos.setEnable(['chariot_g', 'chariot_d'], True)
    await servos.setEnable(['mors_g', 'mors_d','lift_pince'], True)

    await servos.moveMultiple({'lift_pince': lift_wait_replica}, 0.8)
    await servos.moveMultiple({'chariot_d': chariot_d_wait_replica}, 0.8)
    await servos.moveMultiple({'mors_d': mors_d_wait_replica}, 0.8)

    while sensors['sick_lat_d'] == True:
        await asyncio.sleep(0.1)
        
    await asyncio.sleep(3)
    await servos.moveMultiple({'lift_pince': lift_take_replica}, 0.8)
    await servos.moveMultiple({'chariot_d': chariot_d_take_replica}, 0.8)
    await servos.moveMultiple({'mors_d': mors_d_take_replica}, 0.8)

    await asyncio.sleep(1)

@robot.sequence
async def take_replica_left():
    debug_goldo(__name__)

    await servos.setMaxTorque(['chariot_g', 'mors_g', 'lift_pince'], 0.80)    
    await servos.setEnable(['chariot_g'], True)
    await servos.setEnable(['mors_g', 'lift_pince'], True)

    await servos.moveMultiple({'lift_pince': lift_wait_replica}, 0.8)
    await servos.moveMultiple({'chariot_g': chariot_g_wait_replica}, 0.8)
    await servos.moveMultiple({'mors_g': mors_g_wait_replica}, 0.8)

    while sensors['sick_lat_g'] == True:
        await asyncio.sleep(0.1)
        
    await asyncio.sleep(3)
    await servos.moveMultiple({'lift_pince': lift_take_replica}, 0.8)
    await servos.moveMultiple({'chariot_g': chariot_g_take_replica}, 0.8)
    await servos.moveMultiple({'mors_g': mors_g_take_replica}, 0.8)

    await asyncio.sleep(1)

@robot.sequence
async def lift_put_replica():
    await servos.setMaxTorque(['lift_pince'], 0.80)   
    await servos.setMaxTorque(['mors_g'], 0.50) 
    await servos.setEnable(['lift_pince', 'mors_g'], True)
    await servos.moveMultiple({'mors_g': mors_g_hold_replica}, 0.8)
    await servos.moveMultiple({'lift_pince': lift_pos_put_replica}, 0.8)

@robot.sequence
async def lift_pince_top():
    await servos.setMaxTorque(['lift_pince'], 1)  
    await servos.setEnable(['lift_pince'], True)
    await servos.moveMultiple({'lift_pince': lift_up}, 1)

@robot.sequence
async def lift_pince_bottom():
    await servos.setMaxTorque(['lift_pince'], 1)  
    await servos.setEnable(['lift_pince'], True)
    await servos.moveMultiple({'lift_pince': lift_push_square}, 1)

@robot.sequence
async def pince_put_replica():
    await servos.setMaxTorque(['chariot_g', 'mors_g'], 1)  
    await servos.setEnable(['chariot_g', 'mors_g'], True)
    await servos.moveMultiple({'chariot_g': chariot_g_opened}, 1)
    await servos.moveMultiple({'mors_g': mors_g_wait_replica}, 1)

async def open_chariot_g():
    await servos.moveMultiple({'chariot_g': chariot_g_opened}, 0.4)
    tryohm_g_touched = True
    return

async def open_chariot_d():
    await servos.moveMultiple({'chariot_g': chariot_d_opened}, 0.4)
    truc = True
    return

@robot.sequence
async def measure_tryohm_left():
    debug_goldo(__name__)

    tryohm_val = None
    push = False
    await servos.setMaxTorque(['chariot_g', 'mors_g'], 0.50)
    await servos.setMaxTorque(['lift_pince'], 1)
    await servos.setEnable(['chariot_g', 'mors_g', 'lift_pince'], True)
    await servos.moveMultiple({'mors_g': mors_g_closed}, 0.4)
    await servos.moveMultiple({'lift_pince': lift_tryohm}, 1)
    task = asyncio.create_task(open_chariot_g())
    while robot.tryOhm == None and not task.done():
        await asyncio.sleep(0.01)
    task.cancel()
    tryohm_val = robot.tryOhm
    await servos.moveMultiple({'lift_pince': lift_tryohm+400, 'chariot_g': servos.states['chariot_g'].measured_position}, 1)
    await servos.moveMultiple({'chariot_g': 300}, 1)
    return tryohm_val
    # FIXME : TODO : OK to remove this?
    #if robot.side == Side.Purple and tryohm_val == 'purple':
    #    push = True
    #elif robot.side == Side.Yellow and tryohm_val == 'yellow':
    #    push = True
    #if push:
    #    await servos.setMaxTorque(['chariot_g'], 1)
    #    await servos.moveMultiple({'lift_pince': lift_push_square}, 1)
    #    await servos.moveMultiple({'chariot_g':chariot_g_opened}, 1)
    #    await asyncio.sleep(0.5)
    #    await servos.moveMultiple({'chariot_g':chariot_g_closed}, 1)

@robot.sequence
async def measure_tryohm_right():
    debug_goldo(__name__)

    tryohm_val = None
    push = False
    await servos.setMaxTorque(['chariot_d', 'mors_d'], 0.50)
    await servos.setMaxTorque(['lift_pince'], 0.5)
    await servos.setEnable(['chariot_d', 'mors_d', 'lift_pince'], True)
    await servos.moveMultiple(pince_right_init_pos, 1)
    await servos.moveMultiple({'lift_pince': lift_tryohm}, 1)
    task = asyncio.create_task(open_chariot_d())
    while robot.tryOhm == None and not task.done():
        await asyncio.sleep(0.01)
    task.cancel()
    tryohm_val = robot.tryOhm
    await servos.moveMultiple({'lift_pince': lift_tryohm+400, 'chariot_d': servos.states['chariot_d'].measured_position}, 1)
    await servos.moveMultiple({'chariot_d': 300}, 1)
    return tryohm_val
    # FIXME : TODO : OK to remove this?
    #if robot.side == Side.Purple and tryohm_val == 'purple':
    #    push = True
    #elif robot.side == Side.Yellow and tryohm_val == 'yellow':
    #    push = True
    #if push:
    #    await servos.setMaxTorque(['chariot_g'], 1)
    #    await servos.moveMultiple({'lift_pince': lift_push_square}, 1)
    #    await servos.moveMultiple({'chariot_g':chariot_g_opened}, 1)
    #    await asyncio.sleep(0.5)
    #    await servos.moveMultiple({'chariot_g':chariot_g_closed}, 1)

@robot.sequence
async def push_square_right():
    debug_goldo(__name__)

    await servos.setEnable(['chariot_d', 'mors_d', 'lift_pince'], True)
    await servos.setMaxTorque(['chariot_d'], 1)
    await servos.moveMultiple({'lift_pince': lift_push_square}, 1)
    await servos.moveMultiple({'chariot_d':chariot_d_opened}, 1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple({'chariot_d':chariot_d_closed}, 1)

@robot.sequence
async def push_square_left():
    debug_goldo(__name__)

    await servos.setEnable(['chariot_g', 'mors_g', 'lift_pince'], True)
    await servos.setMaxTorque(['chariot_g'], 1)
    await servos.moveMultiple({'lift_pince': lift_push_square}, 1)
    await servos.moveMultiple({'chariot_g':chariot_g_opened}, 1)
    #await asyncio.sleep(0)
    await servos.moveMultiple({'chariot_g':chariot_g_closed}, 1)
