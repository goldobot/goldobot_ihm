# import base modules
import asyncio
import numpy as np
import traceback

import time

# import modules from sequence directory
from . import positions as pos
from . import recalages
from . import actuators_pneuma
from . import actuators_lift
from . import actuators_front
from . import actuators_dyna
from . import robot_config as rc
from . import dynamic as dyn

import logging

LOGGER = logging.getLogger(__name__)

@robot.sequence
async def debug_test_exception():
    MIAU

@robot.sequence
async def debug_propulsion_enable():
    await odrive.clearErrors()
    await asyncio.sleep(0.5)
    await propulsion.clearError()
    await asyncio.sleep(0.5)
    await propulsion.setAccelerationLimits(1,1,10,10)
    await asyncio.sleep(0.5)
    await propulsion.setMotorsEnable(True)
    await asyncio.sleep(0.5)
    await propulsion.setEnable(True)
    await asyncio.sleep(1)
    

@robot.sequence
async def debug_propulsion_disable():
    await propulsion.setMotorsEnable(False)
    await asyncio.sleep(0.5)
    await propulsion.setEnable(False)
    await asyncio.sleep(1)


@robot.sequence
async def debug_translation(*args):
    dist=float(args[0])
    print ("debug_translation : dist={}".format(dist))
    await propulsion.translation(dist, 0.2)
    
@robot.sequence
async def debug_reposition(*args):
    dist=float(args[0])
    print ("debug_reposition : dist={}".format(dist))
    await propulsion.reposition(dist, 0.2)
    
@robot.sequence
async def debug_face_dir_0(*args):
    await propulsion.faceDirection( 0, 2.0)

@robot.sequence
async def debug_face_dir_90(*args):
    await propulsion.faceDirection(90, 2.0)

@robot.sequence
async def debug_face_dir_180(*args):
    await propulsion.faceDirection(180, 2.0)

@robot.sequence
async def debug_face_dir_m90(*args):
    await propulsion.faceDirection(-90, 2.0)

