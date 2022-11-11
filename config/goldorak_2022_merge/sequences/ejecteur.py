import asyncio
from time import sleep

import inspect

def debug_goldo(caller):
    print ()
    print ("************************************************")
    print (" GOLDO DEBUG :  {:32s}".format(inspect.currentframe().f_back.f_code.co_name))
    print ("************************************************")
    print ()

ejecteur_lock_pos = 8550 # ou 8600 pour moins forcer
ejecteur_neutral_pos = 9500
ejecteur_trigger_pos = 11850

@robot.sequence
async def ejecteur_neutral():
    debug_goldo(__name__)

    await servos.moveMultiple({'ejecteur': ejecteur_neutral_pos}, 1)

@robot.sequence
async def ejecteur_trigger():
    debug_goldo(__name__)

    await servos.setEnable(['ejecteur'], True)
    await servos.moveMultiple({'ejecteur': ejecteur_trigger_pos}, 1)
    await asyncio.sleep(0.3)
    await servos.moveMultiple({'ejecteur': ejecteur_neutral_pos}, 1)
    await asyncio.sleep(0.3)
    await servos.setEnable(['ejecteur'], False)

@robot.sequence
async def ejecteur_lock():
    debug_goldo(__name__)

    await servos.moveMultiple({'ejecteur': ejecteur_lock_pos}, 1)

@robot.sequence
async def ejecteur_initialize():
    debug_goldo(__name__)

    await servos.setEnable(['ejecteur'], True)
    await servos.moveMultiple({'ejecteur': ejecteur_neutral_pos}, 1)
    while sensors['switch_ejecteur'] == False:
        await asyncio.sleep(0.02)
    await asyncio.sleep(1)
    await servos.moveMultiple({'ejecteur': ejecteur_lock_pos}, 1)
