import asyncio
from time import sleep

ejecteur_lock_pos = 8550 # ou 8600 pour moins forcer
ejecteur_neutral_pos = 9500
ejecteur_trigger_pos = 11850

@robot.sequence
async def ejecteur_neutral():
    await servos.moveMultiple({'ejecteur': ejecteur_neutral_pos}, 1)

@robot.sequence
async def ejecteur_trigger():
    await servos.setEnable(['ejecteur'], True)
    await servos.moveMultiple({'ejecteur': ejecteur_trigger_pos}, 1)
    await asyncio.sleep(0.3)
    await servos.moveMultiple({'ejecteur': ejecteur_neutral_pos}, 1)
    await asyncio.sleep(0.3)
    await servos.setEnable(['ejecteur'], False)

@robot.sequence
async def ejecteur_lock():
    await servos.moveMultiple({'ejecteur': ejecteur_lock_pos}, 1)

@robot.sequence
async def ejecteur_initialize():
    await servos.setEnable(['ejecteur'], True)
    await servos.moveMultiple({'ejecteur': ejecteur_neutral_pos}, 1)
    while sensors['switch_ejecteur'] == False:
        await asyncio.sleep(0.02)
    await asyncio.sleep(1)
    await servos.moveMultiple({'ejecteur': ejecteur_lock_pos}, 1)