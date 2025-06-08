# import base modules
import asyncio
import numpy as np
import traceback
import time

# import modules from sequence directory
from . import misc
from . import positions as pos
from . import recalages
from . import actuators_pneuma
from . import actuators_lift
from . import actuators_front
from . import actuators_back
from . import robot_config as rc
from . import dynamic as dyn
from . import sequences_old as oldseq

import logging

LOGGER = logging.getLogger(__name__)

@robot.sequence
async def debug_test_exception():
    MIAU

@robot.sequence
async def debug_test_print(*args):
    my_val = float(args[0])
    print ("my_val={}".format(my_val))

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


@robot.sequence
async def debug_prep_test_goldo_back():
    # Pneuma
    await actuators_pneuma.reset_valves()
    await actuators_pneuma.start_compressor()
    await asyncio.sleep(1)

    # Propulsion
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await asyncio.sleep(1)
    
    # Actionneurs
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(1)
    await actuators_back.bras_arr_up()
    await actuators_back.soulageur_arr_down()

@robot.sequence
async def debug_prise_goldo_back():
    global poses
    global test_speed_g
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout

    short_timeout = 0.2
    long_timeout = 0.5

    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(short_timeout)
    await actuators_back.bras_arr_up()
    await actuators_back.soulageur_arr_down()

    print ("Pre-prise")
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(long_timeout)
    await actuators_back.ventouses_arr_ext_attrape()
    await asyncio.sleep(short_timeout)
    await actuators_back.ventouses_arr_int_attrape()
    await asyncio.sleep(short_timeout)
    await actuators_back.bras_arr_standby()
    await asyncio.sleep(short_timeout)
    await propulsion.translation(-0.20, 0.15)
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)

@robot.sequence
async def debug_test_construction_goldo_back():
    await debug_prise_goldo_back()
    await oldseq.construction_goldo()


@robot.sequence
async def debug_prep_test_goldo_front():

    # Pneuma
    await actuators_pneuma.reset_valves()
    await actuators_pneuma.start_compressor()

    # Propulsion
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
    
    # Actionneurs
    await actuators_front.ascenseur_av_homing()
    await asyncio.sleep(1)
    await actuators_front.ascenseur_av_down()
    await asyncio.sleep(1)


@robot.sequence
async def debug_print_detections():
    detections = lidar.getDetections()
    print ("Lidar Detections:")
    for d in detections:
        print (d)

@robot.sequence
async def debug_print_sensors():
    print("SENSORS:")
    for k in sensors:
        print("  {} : {}".format(k,sensors[k]))

@robot.sequence
async def debug_stop_lidar():
    await lidar.stop()

@robot.sequence
async def debug_start_lidar():
    await lidar.start()


