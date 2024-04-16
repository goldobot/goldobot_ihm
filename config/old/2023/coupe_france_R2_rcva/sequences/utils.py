import asyncio
import numpy as np

@robot.sequence
async def get_cake_layers():
    count = 0
    if sensors['sick_niveau_1'] == False:
        count = count + 1
        if sensors['sick_niveau_2'] == False:
            count = count + 1
            if sensors['sick_niveau_3'] == False:
                count = count + 1
                if sensors['sick_niveau_4'] == False:
                    count = count + 1
    return count

@robot.sequence
async def init_field():
    await field.init()

@robot.sequence
async def start_field():
    await field.start()

@robot.sequence
async def stop_field():
    await field.stop()

@robot.sequence
async def clear_field():
    await field.clear()

@robot.sequence
async def deguisement_on():
    await pneumatic.lcd_on()

@robot.sequence
async def deguisement_off():
    await pneumatic.lcd_off()

@robot.sequence
async def led_on():
    await pneumatic.led_on()

@robot.sequence
async def led_off():
    await pneumatic.led_off()