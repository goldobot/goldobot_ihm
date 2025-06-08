# import base modules
import asyncio
import numpy as np
import traceback
import time

# import modules from sequence directory
from . import positions as pos
from . import robot_config as rc
from . import recalages
from . import actuators_pneuma
from . import actuators_lift
from . import actuators_front
from . import actuators_back
from . import dynamic as dyn
from . import sequences_old as oldseq
from . import misc
from . import debug

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

global_long_speed = 0.6
global_turn_speed = 3.0
global_turn_speed_slow = 1.5
global_debug_action_timeout = 0.5
global_debug_timeout = 2.0


@robot.sequence
async def prematch():

    global poses

    if robot.side == pos.Side.Yellow:
        poses = pos.YellowPoses
    elif robot.side == pos.Side.Blue:
        poses = pos.BluePoses
    else:
        raise RuntimeError('Side not set')
    oldseq.set_poses(poses)
    
    await lidar.stop()

    # Pneuma
    await actuators_pneuma.reset_valves()
    await actuators_pneuma.start_compressor()

    # Propulsion
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    
    # Lidar
    #robot._adversary_detection_enable = False
    propulsion.adversary_detection_enable = False
    #await lidar.start()

    # Actionneurs
    await asyncio.sleep(1)
    await actuators_back.bras_arr_standby()
    await asyncio.sleep(2)
    await actuators_back.ascenseur_arr_up()

    # Placement
    await recalages.recalage()

    await asyncio.sleep(1)
    await actuators_back.ascenseur_arr_down()
    await asyncio.sleep(1)
    await actuators_back.bras_arr_up()
    await actuators_back.soulageur_arr_down()

    # Dummy score
    await robot.setScore(0)
    await robot.gpioSet('keyboard_led', True)

    return True


@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """
    global poses
    global test_speed_g
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout

    misc.init_match_time()

    await propulsion.setAccelerationLimits(1,1,20,20)
    #robot._adversary_detection_enable = True
    propulsion.adversary_detection_enable = True

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    # "OLD STATIC" STRATEGY
    if   (robot.start_zone == 1) or (robot.start_zone == 6):
       await oldseq.match_start_ZoneDA()
    elif (robot.start_zone == 2) or (robot.start_zone == 5):
       await oldseq.match_start_ZoneDL()
    elif (robot.start_zone == 3) or (robot.start_zone == 4):
       await oldseq.match_start_ZoneA()

    # "DYNAMIC" STRATEGY
    # await dyn.dyn_strat()
    # await asyncio.sleep(1.0)
    # await dyn.dyn_action4()

    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_time = {}".format(misc.match_time()))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    await lidar.stop()


