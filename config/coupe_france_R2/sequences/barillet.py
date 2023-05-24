import asyncio
from enum import Enum

# class syntax
class Slice(Enum):
    EMPTY = 1
    UNKNOWN = 2
    BROWN = 3
    YELLOW = 4
    PINK = 5


valve_1 = 0
valve_3 = 0
valve_5 = 0
valve_purge = 0


barillet = [[Slice.EMPTY, Slice.EMPTY, Slice.EMPTY], [Slice.EMPTY, Slice.EMPTY, Slice.EMPTY], [Slice.EMPTY, Slice.EMPTY, Slice.EMPTY]]

barillet_haut = {
    'ascenseur': 367,
}

barillet_niv_1_c = {
    'ascenseur': 3089,
}

barillet_niv_2_c = {
    'ascenseur': 2292,
}

barillet_niv_3_c = {
    'ascenseur': 1570,
}

barillet_niv_1_g = {
    'ascenseur': 4043
}

barillet_niv_2_g = {
    'ascenseur': 3206
}

barillet_niv_3_g = {
    'ascenseur': 2518
}

barillet_niv_4_g = {
    'ascenseur': 1693
}

barillet_0 = {
    'rotor': 0,
}
"""
barillet_1 = {
    'rotor': 1729,
}
"""

barillet_1 = {
    'rotor': 1723,
}

barillet_2 = {
    'rotor': 1044,
}

barillet_3 = {
    'rotor': 364,
}

barillet_4 = {
    'rotor': 3777,
}

"""
barillet_5 = {
    'rotor': 3100,
}
"""
barillet_5 = {
    'rotor': 3096,
}

barillet_6 = {
    'rotor': 2409,
}

# barillet bas  = 4051


@robot.sequence
async def start_compressor():
    await pneumatic.set_valves(0, 0, 0, 0)
    await pneumatic.start_compressor(30)

@robot.sequence
async def stop_compressor():
    await pneumatic.stop_compressor()

@robot.sequence
async def purge():
    await pneumatic.purge_compressor()
    await pneumatic.set_valves(0, 0, 0, 1)

@robot.sequence
async def valve1():
    global valve_1
    global valve_3
    global valve_5
    global valve_purge
    valve_1 = 1
    await pneumatic.set_valves(valve_1, valve_5, valve_3, valve_purge)

@robot.sequence
async def valve5():
    global valve_1
    global valve_3
    global valve_5
    global valve_purge
    valve_5 = 1
    await pneumatic.set_valves(valve_1, valve_5, valve_3, valve_purge)

@robot.sequence
async def valve3():
    global valve_1
    global valve_3
    global valve_5
    global valve_purge
    valve_3 = 1
    await pneumatic.set_valves(valve_1, valve_5, valve_3, valve_purge)

@robot.sequence
async def valves():
    await pneumatic.set_valves(1, 1, 1, 0)

@robot.sequence
async def pulse1():
    await pneumatic.pulse_valves(1, 0, 0, 0)

@robot.sequence
async def pulse5():
    await pneumatic.pulse_valves(0, 1, 0, 0)

@robot.sequence
async def pulse3():
    await pneumatic.pulse_valves(0, 0, 1, 0)

@robot.sequence
async def reset_valves():
    global valve_1
    global valve_3
    global valve_5
    global valve_purge
    valve_1 = 0
    valve_3 = 0
    valve_5 = 0
    valve_purge = 0
    await pneumatic.set_valves(0, 0, 0, 0)

@robot.sequence
async def test_valves():
    await pneumatic.set_valves(1, 1, 1, 1)

@robot.sequence
async def barillet_init():
    await servos.setMaxTorque(['ascenseur', 'rotor'], 1.0)    
    await servos.setEnable(['ascenseur', 'rotor'], True)
    await servos.moveMultiple(barillet_haut, speed=1)

@robot.sequence
async def barillet_init_test():
    await servos.setMaxTorque(['ascenseur'], 1.0) 
    await servos.setMaxTorque(['rotor'], 0.0)    
    await servos.setEnable(['ascenseur'], True)
    await servos.setEnable(['rotor'], False)
    await servos.moveMultiple(barillet_haut, speed=1)

@robot.sequence
async def init_rotor():
    await servos.setMaxTorque(['rotor'], 1.0)    
    await servos.setEnable(['rotor'], True)

@robot.sequence
async def barillet_pose_haut():
    await servos.moveMultiple(barillet_haut, speed=1)

@robot.sequence
async def barillet_pose_0():
    await servos.moveMultiple(barillet_0, speed=1)

@robot.sequence
async def barillet_pose_1():
    await servos.moveMultiple(barillet_1, speed=1)

@robot.sequence
async def barillet_pose_2():
    await servos.moveMultiple(barillet_2, speed=1)

@robot.sequence
async def barillet_pose_3():
    await servos.moveMultiple(barillet_3, speed=1)

@robot.sequence
async def barillet_pose_4():
    await servos.moveMultiple(barillet_4, speed=1)

@robot.sequence
async def barillet_pose_5():
    await servos.moveMultiple(barillet_5, speed=1)

@robot.sequence
async def barillet_pose_6():
    await servos.moveMultiple(barillet_6, speed=1)

@robot.sequence
async def barillet_niv1_cerise():
    await servos.moveMultiple(barillet_niv_1_c, speed=1)

@robot.sequence
async def barillet_niv2_cerise():
    await servos.moveMultiple(barillet_niv_2_c, speed=1)

@robot.sequence
async def barillet_niv3_cerise():
    await servos.moveMultiple(barillet_niv_3_c, speed=1)

@robot.sequence
async def barillet_niv1_gateau():
    await servos.moveMultiple(barillet_niv_1_g, speed=1)

@robot.sequence
async def barillet_niv2_gateau():
    await servos.moveMultiple(barillet_niv_2_g, speed=1)

@robot.sequence
async def barillet_niv3_gateau():
    await servos.moveMultiple(barillet_niv_3_g, speed=1)

@robot.sequence
async def barillet_niv4_gateau():
    await servos.moveMultiple(barillet_niv_4_g, speed=1)

async def barillet_spin(pos):
    if pos == 1:
        await barillet_pose_1()
    elif pos == 2:
        await barillet_pose_2()
    elif pos == 3:
        await barillet_pose_3()
    elif pos == 4:
        await barillet_pose_4()
    elif pos == 5:
        await barillet_pose_5()
    elif pos == 6:
        await barillet_pose_6()

async def barillet_pulse(pos):
    if pos == 1:
        await pulse1()
    elif pos == 3:
        await pulse3()
    elif pos == 5:
        await pulse5()

@robot.sequence
async def print_sensors():
    print(sensors)