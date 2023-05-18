import asyncio
from enum import Enum

# class syntax
class Slice(Enum):
    EMPTY = 1
    UNKNOWN = 2
    BROWN = 3
    YELLOW = 4
    PINK = 5


barillet = [[Slice.EMPTY, Slice.EMPTY, Slice.EMPTY], [Slice.EMPTY, Slice.EMPTY, Slice.EMPTY], [Slice.EMPTY, Slice.EMPTY, Slice.EMPTY]]

barillet_haut = {
    'ascenseur': 424,
}

barillet_niv_1 = {
    'ascenseur': 3089,
}

barillet_niv_2 = {
    'ascenseur': 2292,
}

barillet_niv_3 = {
    'ascenseur': 1525,
}

barillet_1 = {
    'rotor': 1729,
}

barillet_2 = {
    'rotor': 1044,
}

barillet_3 = {
    'rotor': 366,
}

barillet_4 = {
    'rotor': 3782,
}

barillet_5 = {
    'rotor': 3100,
}

barillet_6 = {
    'rotor': 2411,
}

# barillet bas  = 4051


@robot.sequence
async def start_compressor_20():
    await pneumatic.start_compressor(20)

@robot.sequence
async def start_compressor():
    await pneumatic.set_valves(0, 0, 0, 0)
    await pneumatic.start_compressor(30)

@robot.sequence
async def start_compressor_40():
    await pneumatic.start_compressor(36)
@robot.sequence
async def stop_compressor():
    await pneumatic.stop_compressor()

@robot.sequence
async def purge():
    await pneumatic.purge_compressor()
    await pneumatic.set_valves(0, 0, 0, 1)

@robot.sequence
async def valve1():
    await pneumatic.set_valves(1, 0, 0, 0)

@robot.sequence
async def valve5():
    await pneumatic.set_valves(0, 1, 0, 0)

@robot.sequence
async def valve3():
    await pneumatic.set_valves(0, 0, 1, 0)

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
async def barillet_pose_1():
    await servos.moveMultiple(barillet_1, speed=0xFF)

@robot.sequence
async def barillet_pose_2():
    await servos.moveMultiple(barillet_2, speed=0xFF)

@robot.sequence
async def barillet_pose_3():
    await servos.moveMultiple(barillet_3, speed=0xFF)

@robot.sequence
async def barillet_pose_4():
    await servos.moveMultiple(barillet_4, speed=0xFF)

@robot.sequence
async def barillet_pose_5():
    await servos.moveMultiple(barillet_5, speed=0xFF)

@robot.sequence
async def barillet_pose_6():
    await servos.moveMultiple(barillet_6, speed=0xFF)

@robot.sequence
async def barillet_pose_6():
    await servos.moveMultiple(barillet_6, speed=0xFF)

@robot.sequence
async def barillet_niv1():
    await servos.moveMultiple(barillet_niv_1, speed=0xFF)

@robot.sequence
async def barillet_niv2():
    await servos.moveMultiple(barillet_niv_2, speed=0xFF)

@robot.sequence
async def barillet_niv3():
    await servos.moveMultiple(barillet_niv_3, speed=0xFF)
