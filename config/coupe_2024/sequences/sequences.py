# import base modules
import asyncio
import numpy as np

# import modules from sequences folder

import sys
sys.path.append("./actuators")

from .positions import *
from .recalages import *
from .carousel import *
from . import cheminees
from . import tourne_panneau
from . import balayeur

carousel = Carousel()

@robot.sequence
async def prematch():
    await cheminees.init_turbines()
    await cheminees.test_turbines()

@robot.sequence
async def start_match():
    pass

@robot.sequence
async def test_synchro():
    await slot_ejecteur_gauche(3)
    await tourne_panneau.tourne_panneau_out()
    await tourne_panneau.tourne_panneau_in()

@robot.sequence
async def test_stockage():
    plante = False
    await slot_cheminee_gauche(2)
    await cheminees.turbine_g_suck()
    while plante is False:
        plante = await cheminees.plant_in_left()
        await asyncio.sleep(0.05)
    await slot_cheminee_droite(2)
    await cheminees.turbine_g_stop()

@robot.sequence
async def print_sensors():
    print(sensors)
