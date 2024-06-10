# import base modules
import asyncio
from enum import Enum
import numpy as np

# import modules from sequences folder
import time
import sys
sys.path.append("./actuators")

from .positions import *
from .recalages import *
from .carousel import *
from .toboggan import *
from .fourche import *
from .cheminees import *
from . import tourne_panneau
from . import balayeur
from . import robot_config as rc

@robot.sequence
async def feed_2_plants():
    pass

