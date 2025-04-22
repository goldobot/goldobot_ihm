# FIXME : TODO

import asyncio
from enum import Enum

@robot.sequence
async def test_ascenseur_haut():
    await servos.moveMultiple({'ascenseur_arr_mx28':3700}, speed=0.7)

@robot.sequence
async def test_ascenseur():
    await servos.moveMultiple({'ascenseur_arr_mx28':3000}, speed=0.7)

@robot.sequence
async def test_ascenseur_bas():
    await servos.moveMultiple({'ascenseur_arr_mx28':2500}, speed=0.7)

