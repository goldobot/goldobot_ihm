import asyncio
from enum import Enum

# VALVE 1 : ecarteurs
valve_1 = 0
# VALVE 2 : ventouses int
valve_2 = 0
# VALVE 3 : ventouses ext
valve_3 = 0
valve_purge = 0

@robot.sequence
async def start_compressor():
    await pneumatic.compressor_on(30)

@robot.sequence
async def stop_compressor():
    await pneumatic.compressor_off()

@robot.sequence
async def purge():
    await pneumatic.purge()

@robot.sequence
async def reset_valves():
    await pneumatic.multiple_valves_on(1,2,3,4,5,6,7,8,9,10,11,12)

@robot.sequence
async def ventouses_int_lache():
    global valve_1
    global valve_2
    global valve_3
    global valve_purge
    valve_2 = 1
    pneumatic.set_valves(valve_1, valve_2, valve_3, valve_purge)

@robot.sequence
async def ventouses_int_attrape():
    global valve_1
    global valve_2
    global valve_3
    global valve_purge
    valve_2 = 0
    pneumatic.set_valves(valve_1, valve_2, valve_3, valve_purge)

@robot.sequence
async def ventouses_ext_lache():
    global valve_1
    global valve_2
    global valve_3
    global valve_purge
    valve_3 = 1
    pneumatic.set_valves(valve_1, valve_2, valve_3, valve_purge)

@robot.sequence
async def ventouses_ext_attrape():
    global valve_1
    global valve_2
    global valve_3
    global valve_purge
    valve_3 = 0
    pneumatic.set_valves(valve_1, valve_2, valve_3, valve_purge)

@robot.sequence
async def ecarteur_on():
    global valve_1
    global valve_2
    global valve_3
    global valve_purge
    valve_1 = 1
    pneumatic.set_valves(valve_1, valve_2, valve_3, valve_purge)

@robot.sequence
async def ecarteur_off():
    global valve_1
    global valve_2
    global valve_3
    global valve_purge
    valve_1 = 0
    pneumatic.set_valves(valve_1, valve_2, valve_3, valve_purge)


###########################################################
################## TEST VALVES SEQUENCES ##################
###########################################################

@robot.sequence
async def valve_1_on():
    await pneumatic.valve_on(1)

@robot.sequence
async def valve_2_on():
    await pneumatic.valve_on(2)

@robot.sequence
async def valve_3_on():
    await pneumatic.valve_on(3)

@robot.sequence
async def valve_4_on():
    await pneumatic.valve_on(4)

@robot.sequence
async def valve_5_on():
    await pneumatic.valve_on(5)

@robot.sequence
async def valve_6_on():
    await pneumatic.valve_on(6)

@robot.sequence
async def valve_7_on():
    await pneumatic.valve_on(7)
    
@robot.sequence
async def valve_8_on():
    await pneumatic.valve_on(8)

@robot.sequence
async def valve_9_on():
    await pneumatic.valve_on(9)

@robot.sequence
async def valve_10_on():
    await pneumatic.valve_on(10)

@robot.sequence
async def valve_11_on():
    await pneumatic.valve_on(11)

@robot.sequence
async def valve_12_on():
    await pneumatic.valve_on(12)

@robot.sequence
async def valve_1_off():
    await pneumatic.valve_off(1)

@robot.sequence
async def valve_2_off():
    await pneumatic.valve_off(2)

@robot.sequence
async def valve_3_off():
    await pneumatic.valve_off(3)

@robot.sequence
async def valve_4_off():
    await pneumatic.valve_off(4)

@robot.sequence
async def valve_5_off():
    await pneumatic.valve_off(5)

@robot.sequence
async def valve_6_off():
    await pneumatic.valve_off(6)

@robot.sequence
async def valve_7_off():
    await pneumatic.valve_off(7)
    
@robot.sequence
async def valve_8_off():
    await pneumatic.valve_off(8)

@robot.sequence
async def valve_9_off():
    await pneumatic.valve_off(9)

@robot.sequence
async def valve_10_off():
    await pneumatic.valve_off(10)

@robot.sequence
async def valve_11_off():
    await pneumatic.valve_off(11)

@robot.sequence
async def valve_12_off():
    await pneumatic.valve_off(12)

@robot.sequence
async def all_valves_on():
    await pneumatic.multiple_valves_on(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

@robot.sequence
async def all_valves_off():
    await pneumatic.multiple_valves_off(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
