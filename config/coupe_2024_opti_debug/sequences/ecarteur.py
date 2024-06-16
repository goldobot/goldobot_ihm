import asyncio

# millieu theorique (non utilise en match, sauf sequence autotest => /!\ attention au placement du robot avant prematch)
ecarteur_middle_var = 10000

# force un peu sur le servo mais permet de bien rentrer
ecarteur_close_overshoot_var = 13500

# position ecarteur rentre (pour recallage etc..)
ecarteur_iddle_var = 13400

# ecarte les 2 pots en comptant sur l'overshoot..
ecarteur_spread_var = 9500

# position pour inserer l'ecarteur entre les 2 pots (en position initiale)
ecarteur_pointy_var = 7100


@robot.sequence
async def ecarteur_pointy():
    await servos.setEnable(['ecarteur'], True)
    await servos.moveMultiple({'ecarteur': ecarteur_pointy_var}, 1)
    await asyncio.sleep(0.2)

@robot.sequence
async def ecarteur_middle():
    await servos.setEnable(['ecarteur'], True)
    await servos.moveMultiple({'ecarteur': ecarteur_middle_var}, 1)
    await asyncio.sleep(0.2)

@robot.sequence
async def ecarteur_iddle():
    await servos.setEnable(['ecarteur'], True)
    await servos.moveMultiple({'ecarteur': ecarteur_close_overshoot_var}, 1)
    await asyncio.sleep(0.2)
    await servos.moveMultiple({'ecarteur': ecarteur_iddle_var}, 1)
    await asyncio.sleep(0.2)

@robot.sequence
async def ecarteur_spread():
    await servos.setEnable(['ecarteur'], True)
    await servos.moveMultiple({'ecarteur': ecarteur_spread_var}, 0.2)
    await asyncio.sleep(0.2)

@robot.sequence
async def ecarteur_autotest():
    await ecarteur_iddle()
    await asyncio.sleep(0.5)
    await ecarteur_middle()
    await ecarteur_iddle()
    await asyncio.sleep(0.5)
