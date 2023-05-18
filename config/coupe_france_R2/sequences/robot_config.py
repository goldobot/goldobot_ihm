import asyncio

#values for 07 2021
robot_width = 0.255
robot_front_length = 0.1197
robot_back_length = 0.0837
robot_rotation_distance= 0.2
robot_rotation_distance_figurine = 0.25

@robot.sequence
async def init_field():
    field.init()

@robot.sequence
async def start_field():
    field.start()

@robot.sequence
async def stop_field():
    field.stop()

@robot.sequence
async def test_remove_cakes():
    await field.remove_cake(3)
    await asyncio.sleep(3)
    await field.remove_cake(7)
    await asyncio.sleep(2)
    await field.remove_cake(4)

@robot.sequence
async def test_add_cakes():
    await field.add_cake(20, 0.2, 0.3, 4)
    await asyncio.sleep(3)
    await field.add_cake(20, 0.4, 0.3, 4)
    await asyncio.sleep(3)
    await field.add_cake(20, 0.6, 0.3, 4)

@robot.sequence
async def deguisement_on():
    await pneumatic.lcd_on()

@robot.sequence
async def deguisement_off():
    await pneumatic.lcd_off()