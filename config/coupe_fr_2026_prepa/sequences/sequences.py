# Sequences principales 2026

# import base modules
import asyncio
import numpy as np

import time

# NOTE : prise_offset_back_robot = 0.305
# NOTE : robot_back_length       = 0.084
# NOTE : prise_offset            = 0.220

# import modules from sequence directory
from . import positions as pos
from . import recalages
from . import actuators
from . import vision as cam
from . import robot_config as rc

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

poses = None

start_long_speed = 0.30
start_turn_speed = 2.0

global_long_speed = 0.45
#global_long_speed = 0.25
global_turn_speed = 2.5

global_short_sleep = 0.3
global_long_sleep  = 2.0

global_danger_threshold = 0.5

@robot.sequence
async def prematch():
    global poses
    global start_long_speed
    global start_turn_speed
    global global_long_speed
    global global_turn_speed

    if robot.side == 1: # YELLOW
        poses = pos.YellowPoses
    elif robot.side == 2: # BLUE
        poses = pos.BluePoses
    else:
        raise RuntimeError('Side not set')

    # Propulsion
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    
    # Lidar
    robot._adversary_detection_enable = False
    #await lidar.start()

    # Actionneurs
    await actuators.arms_initialize()
    await asyncio.sleep(1.0)

    await actuators.arms_close()
    await asyncio.sleep(0.5)

    await actuators.arms_close()
    await asyncio.sleep(2.0)

    # Placement
    await recalages.recalage()
    await asyncio.sleep(1.0)

    await actuators.position_defensive_laterale()
    await asyncio.sleep(0.5)

    # Dummy score
    await robot.setScore(42)
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print ("$ Dummy score 42")
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    await robot.gpioSet('keyboard_led', True)

    await propulsion.setAccelerationLimits(1,1,20,20)

    return True


@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """

    global poses
    global start_long_speed
    global start_turn_speed
    global global_long_speed
    global global_turn_speed

    T0 = time.time()

    await propulsion.setAccelerationLimits(1,1,20,20)

    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    robot._adversary_detection_enable = True
    await lidar.start()

    try:
        await action_0()
        await asyncio.sleep(1.0)
    except:
        print ("EXCEPTION!")
        await escape_procedure(poses.Final_escape_wp0)
        await asyncio.sleep(0.1)

    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    try:
        await action_1()
        await asyncio.sleep(0.1)
    except:
        print ("EXCEPTION!")
        await escape_procedure(poses.Final_escape_wp0)
        await asyncio.sleep(0.1)

    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    try:
        await action_2()
        await asyncio.sleep(0.1)
    except:
        print ("EXCEPTION!")
        await escape_procedure(poses.Final_escape_wp0)
        await asyncio.sleep(0.1)
 
    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    try:
        await action_42()
        await asyncio.sleep(0.1)
    except:
        print ("EXCEPTION!")
        await escape_procedure(poses.Final_escape_wp0)
        await asyncio.sleep(0.1)
 
    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    try:
        await action_3()
        await asyncio.sleep(0.1)
    except:
        print ("EXCEPTION!")
        await escape_procedure(poses.Final_escape_wp0)
        await asyncio.sleep(0.1)
    
    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    print()
    print("=======")
    print("GO HOME")
    print("=======")
    print()

    t1 = asyncio.create_task(actuators.arms_final_state())

    await propulsion.pointTo(poses.Final_escape_wp0, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y
    final_excape = [
        (p0_x, p0_y, 0),
        poses.Final_escape_wp0,
        poses.Final_escape_wp1,
        poses.Final_pose_wp
    ]
    try :
        await propulsion.trajectorySpline(final_excape, speed=global_long_speed)
    except:
        print ("EXCEPTION!")
        await propulsion.setEnable(False)
        await asyncio.sleep(0.2)
        await propulsion.setEnable(True)
        await asyncio.sleep(0.2)
        await propulsion.setMotorsEnable(True)
        await asyncio.sleep(0.2)
        await propulsion.clearError()
        await asyncio.sleep(0.2)
        await propulsion.moveToRetry(poses.Final_pose_wp, global_long_speed)
        await asyncio.sleep(global_short_sleep)

    await t1

    await lidar.stop()

    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")


def compute_dist(p0, p1):
    delta_x = p1[0] - p0[0]
    delta_y = p1[1] - p0[1]
    return np.sqrt(delta_x*delta_x + delta_y*delta_y)

def is_danger():
    global global_danger_threshold
    detections = lidar.getDetections()
    if (len(detections)>0):
        first_det = detections[0]
        print ("Lidar detections : ")
        print (first_det)
        p0 = (propulsion.pose.position.x, propulsion.pose.position.y)
        p1 = (first_det.x, first_det.y)
        dist = compute_dist(p0, p1)
        if (dist<global_danger_threshold):
            return True
    return False

@robot.sequence
async def reset_and_reenable_propulsion():
    await propulsion.setEnable(False)
    await asyncio.sleep(0.2)
    await propulsion.setEnable(True)
    await asyncio.sleep(0.2)
    await propulsion.setMotorsEnable(True)
    await asyncio.sleep(0.2)
    await propulsion.clearError()
    await asyncio.sleep(0.2)

@robot.sequence
async def escape_procedure(escape_point):
    await actuators.pumps_off()
    await asyncio.sleep(0.1)
    await actuators.position_defensive_laterale()
    await asyncio.sleep(0.1)
    for i in range (0,5):
        if (is_danger()):
            print ("DANGER!")
            await asyncio.sleep(1.0)
        else:
            await reset_and_reenable_propulsion()
            return
    # adversary refuses to go away.. try to go to the escape_point..
    await propulsion.pointTo(escape_point, global_long_speed)
    await asyncio.sleep(0.1)
    await propulsion.moveToRetry(escape_point, global_long_speed)
    await asyncio.sleep(0.1)


@robot.sequence
async def action_0():
    global poses
    global start_long_speed
    global start_turn_speed
    global global_long_speed
    global global_turn_speed

    print()
    print("=======")
    print("ACTION0")
    print("=======")
    print()

    aruco_x_configuration = "0000"

    await propulsion.moveTo(poses.First_grab_wp1, 0.3)
    await asyncio.sleep(global_short_sleep)

    for i in range(0,5):
        print()
        print("================")
        print ("ARUCO TRY {}".format(i))
        print("----------------")
        try:
            aruco_x_configuration = cam.aruco_x_detection()
        except:
            print ("aruco_x_detection() failed")
            aruco_x_configuration = "0000"
        if (aruco_x_configuration!="0000"):
            print("VVVVVVVVVVVVVVVV")
            print()
            break
        print("----------------")
        print()
        await asyncio.sleep(0.3)

    if (aruco_x_configuration not in grab_and_push_x_funcs.keys()):
        await do_push_0000()
    else:
        await grab_and_push_x_funcs[aruco_x_configuration]()

    robot._adversary_detection_enable = True

    t1 = asyncio.create_task(actuators.arms_prep_thermo())

    #await propulsion.pointTo(poses.Inter_wp1, global_turn_speed)
    #await asyncio.sleep(global_short_sleep)
    #await propulsion.moveTo(poses.Inter_wp1, global_long_speed)
    #await asyncio.sleep(global_short_sleep)

    #await propulsion.pointTo(poses.Inter_wp2, global_turn_speed)
    #await asyncio.sleep(global_short_sleep)
    #await propulsion.moveTo(poses.Inter_wp2, global_long_speed)
    #await asyncio.sleep(global_short_sleep)

    await propulsion.pointTo(poses.Inter_wp1, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    p0_x = propulsion.pose.position.x
    p0_y = propulsion.pose.position.y
    goto_corner = [
        (p0_x, p0_y, 0),
        poses.Inter_wp1,
        poses.Inter_wp2
    ]
    await propulsion.trajectorySpline(goto_corner, speed=global_long_speed)

    await propulsion.pointTo(poses.Corner_wp, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Corner_wp, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.pointTo(pt=poses.Border_wp1, yaw_rate=global_turn_speed, back=True)
    await asyncio.sleep(global_short_sleep)

    await t1

    print("CORNER!")

    if (robot.start_zone==1):   # BLUE   (Y+)
        await actuators.arm_right_push_thermo()
        await asyncio.sleep(global_short_sleep)
    elif (robot.start_zone==2): # YELLOW (Y-)
        await actuators.arm_left_push_thermo()
        await asyncio.sleep(global_short_sleep)
    else:
        print("No start zone!")

    #await asyncio.sleep(global_long_sleep)
    await asyncio.sleep(global_short_sleep)

    await propulsion.moveTo(poses.Border_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)

    await actuators.arms_close()
    await asyncio.sleep(global_short_sleep)


@robot.sequence
async def action_1():
    global poses
    global start_long_speed
    global start_turn_speed
    global global_long_speed
    global global_turn_speed

    print()
    print("=======")
    print("ACTION1")
    print("=======")
    print()

    aruco_y_configuration = "0000"

    await propulsion.pointTo(pt=poses.Action1_grab_wp1, yaw_rate=global_turn_speed, back=False)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action1_grab_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action1_grab_wp1[2], global_turn_speed)
    await asyncio.sleep(global_short_sleep)

    await actuators.position_defensive_laterale()
    await asyncio.sleep(global_short_sleep)

    await asyncio.sleep(0.1)
    for i in range(0,5):
        print()
        print("================")
        print ("ARUCO TRY {}".format(i))
        print("----------------")
        try:
            aruco_y_configuration = cam.aruco_y_detection()
        except:
            print ("aruco_y_detection() failed")
            aruco_y_configuration = "0000"
        if (aruco_y_configuration!="0000"):
            print("VVVVVVVVVVVVVVVV")
            print()
            break
        print("----------------")
        print()
        await asyncio.sleep(0.5)

    if (aruco_y_configuration not in grab_y_funcs.keys()):
        print("Cannot do Action1!")
        await asyncio.sleep(1.0)
        return
    else:
        await grab_y_funcs[aruco_y_configuration]()

    await propulsion.pointTo(pt=poses.Action1_drop_wp1, yaw_rate=global_turn_speed, back=True)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action1_drop_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action1_drop_wp1[2], global_turn_speed)
    await asyncio.sleep(global_short_sleep)

    await do_drop_y_1001()


@robot.sequence
async def action_2():
    global poses
    global start_long_speed
    global start_turn_speed
    global global_long_speed
    global global_turn_speed

    print()
    print("=======")
    print("ACTION2")
    print("=======")
    print()

    await propulsion.pointTo(pt=poses.Action2_grab_wp0, yaw_rate=global_turn_speed, back=False)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action2_grab_wp0, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action2_grab_wp1[2], global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action2_grab_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)

    await actuators.position_defensive_laterale()
    await asyncio.sleep(global_short_sleep)

    await asyncio.sleep(0.1)
    for i in range(0,5):
        print()
        print("================")
        print ("ARUCO TRY {}".format(i))
        print("----------------")
        try:
            aruco_y_configuration = cam.aruco_y_detection()
        except:
            print ("aruco_y_detection() failed")
            aruco_y_configuration = "0000"
        if (aruco_y_configuration!="0000"):
            print("VVVVVVVVVVVVVVVV")
            print()
            break
        print("----------------")
        print()
        await asyncio.sleep(0.5)

    if (aruco_y_configuration not in grab_y_funcs.keys()):
        print("Cannot do Action2!")
        await asyncio.sleep(1.0)
        return
    else:
        await grab_y_funcs[aruco_y_configuration]()

    await propulsion.pointTo(pt=poses.Action2_drop_wp1, yaw_rate=global_turn_speed, back=True)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action2_drop_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action2_drop_wp1[2], global_turn_speed)
    await asyncio.sleep(global_short_sleep)

    await do_drop_y_1001()


@robot.sequence
async def action_42():
    global poses
    global start_long_speed
    global start_turn_speed
    global global_long_speed
    global global_turn_speed

    print()
    print("=======")
    print("ACTION42")
    print("=======")
    print()

    await propulsion.pointTo(pt=poses.Action42_grab_wp0, yaw_rate=global_turn_speed, back=False)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action42_grab_wp0, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action42_grab_wp1[2], global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action42_grab_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)

    await actuators.position_defensive_laterale()
    await asyncio.sleep(global_short_sleep)

    await asyncio.sleep(0.1)
    for i in range(0,5):
        print()
        print("================")
        print ("ARUCO TRY {}".format(i))
        print("----------------")
        try:
            aruco_y_configuration = cam.aruco_y_detection()
        except:
            print ("aruco_y_detection() failed")
            aruco_y_configuration = "0000"
        if (aruco_y_configuration!="0000"):
            print("VVVVVVVVVVVVVVVV")
            print()
            break
        print("----------------")
        print()
        await asyncio.sleep(0.5)

    if (aruco_y_configuration not in grab_y_funcs.keys()):
        print("Cannot do Action42!")
        await asyncio.sleep(1.0)
        return
    else:
        await grab_y_funcs[aruco_y_configuration]()

    await propulsion.pointTo(pt=poses.Action42_drop_wp0, yaw_rate=global_turn_speed, back=True)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action42_drop_wp0, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.pointTo(pt=poses.Action42_drop_wp1, yaw_rate=global_turn_speed, back=False)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action42_drop_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action42_drop_wp1[2], global_turn_speed)
    await asyncio.sleep(global_short_sleep)

    await do_drop_y_42()


@robot.sequence
async def action_3():
    global poses
    global start_long_speed
    global start_turn_speed
    global global_long_speed
    global global_turn_speed

    print()
    print("=======")
    print("ACTION3")
    print("=======")
    print()

    await propulsion.pointTo(pt=poses.Action3_grab_wp0, yaw_rate=global_turn_speed, back=False)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action3_grab_wp0, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action3_grab_wp1[2], global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action3_grab_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)

    await actuators.position_defensive_laterale()
    await asyncio.sleep(global_short_sleep)

    await asyncio.sleep(0.1)
    for i in range(0,5):
        print()
        print("================")
        print ("ARUCO TRY {}".format(i))
        print("----------------")
        try:
            aruco_y_configuration = cam.aruco_y_detection()
        except:
            print ("aruco_y_detection() failed")
            aruco_y_configuration = "0000"
        if (aruco_y_configuration!="0000"):
            print("VVVVVVVVVVVVVVVV")
            print()
            break
        print("----------------")
        print()
        await asyncio.sleep(0.5)

    if (aruco_y_configuration not in grab_y_funcs.keys()):
        print("Cannot do Action3!")
        await asyncio.sleep(1.0)
        return
    else:
        await grab_y_funcs[aruco_y_configuration]()

    await propulsion.pointTo(pt=poses.Action3_drop_wp1, yaw_rate=global_turn_speed, back=True)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action3_drop_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action3_drop_wp1[2], global_turn_speed)
    await asyncio.sleep(global_short_sleep)

    await do_drop_y_1001()


########################################################################################
### GRAB & PUSH X
########################################################################################

async def do_push_0000():
    await propulsion.moveTo(poses.First_push, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_grab_wp2, global_long_speed)
    await asyncio.sleep(global_short_sleep)

async def do_first_drop():
    #await propulsion.pointTo(pt=poses.First_return_wp, yaw_rate=global_turn_speed, back=True)
    #await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_return_wp, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(-180, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.arm_right_left_drop_y_0_0()
    await asyncio.sleep(global_short_sleep)
    await actuators.pumps_off()
    await asyncio.sleep(0.5)
    await actuators.goldo_lifts_move(400)
    await asyncio.sleep(0.5)
    await actuators.position_defensive_laterale()
    await asyncio.sleep(global_short_sleep)

async def do_grab_and_push_x_0011():
    #await propulsion.moveTo(poses.First_grab_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.test_grab_right()
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_grab_wp2, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.test_grab_left()
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_push_out, global_long_speed)
    await asyncio.sleep(global_short_sleep)

    await do_first_drop()

async def do_grab_and_push_x_0101():
    #await propulsion.moveTo(poses.First_grab_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.test_grab_right()
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_grab_wp3, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.test_grab_left()
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_push_out, global_long_speed)
    await asyncio.sleep(global_short_sleep)

    await do_first_drop()

async def do_grab_and_push_x_0110():
    #await propulsion.moveTo(poses.First_grab_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.test_grab_right()
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_push_out, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await asyncio.sleep(global_short_sleep)

    #await do_first_drop()

    await propulsion.translation(-0.150, global_long_speed)
    await asyncio.sleep(global_short_sleep)

    await actuators.arms_close_extreme()
    await asyncio.sleep(global_short_sleep)
    await actuators.left_pump_on()
    await asyncio.sleep(global_short_sleep)
    await actuators.right_pump_off()
    await asyncio.sleep(0.5)
    await actuators.position_defensive_laterale_d()
    await asyncio.sleep(global_short_sleep)
    await actuators.arm_left_take()
    await asyncio.sleep(global_short_sleep)
    await actuators.left_pump_off()
    await asyncio.sleep(global_short_sleep)
    await actuators.position_defensive_laterale_g()
    await asyncio.sleep(global_short_sleep)

    await propulsion.translation(-0.150, global_long_speed)
    await asyncio.sleep(0.1)

async def do_grab_and_push_x_1001():
    await propulsion.moveTo(poses.First_grab_wp2, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.test_grab_right()
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_grab_wp3, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.test_grab_left()
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_push_out, global_long_speed)
    await asyncio.sleep(global_short_sleep)

    await do_first_drop()

async def do_grab_and_push_x_1010():
    await propulsion.moveTo(poses.First_grab_wp2, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.test_grab_right()
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_push_out, global_long_speed)
    await asyncio.sleep(global_short_sleep)

    await do_first_drop()

async def do_grab_and_push_x_1100():
    await propulsion.moveTo(poses.First_push_out, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_grab_wp2, global_long_speed)
    await asyncio.sleep(global_short_sleep)

grab_and_push_x_funcs = {
    "0011":do_grab_and_push_x_0011,
    "0101":do_grab_and_push_x_0101,
    "0110":do_grab_and_push_x_0110,
    "1001":do_grab_and_push_x_1001,
    "1010":do_grab_and_push_x_1010,
    "1100":do_grab_and_push_x_1100,
}


########################################################################################
### GRAB Y
########################################################################################

@robot.sequence
async def do_grab_y_0011():
    #await actuators.arm_left_prep_take()
    #await asyncio.sleep(0.1)
    await actuators.left_pump_on()
    await asyncio.sleep(0.1)
    await actuators.arm_left_take_y_0()
    await asyncio.sleep(0.1)
    #await actuators.position_defensive_laterale_g()
    await actuators.goldo_lift_left_move(800)
    await asyncio.sleep(0.2)

    await propulsion.translation(0.040, 0.2)
    await asyncio.sleep(0.1)

    #await actuators.arm_right_prep_take()
    #await asyncio.sleep(0.1)
    await actuators.right_pump_on()
    await asyncio.sleep(0.1)
    await actuators.arm_right_take_y_2()
    await asyncio.sleep(0.1)
    #await actuators.position_defensive_laterale_d()
    await actuators.goldo_lift_right_move(800)
    await asyncio.sleep(0.5)

@robot.sequence
async def do_grab_y_0101():
    #await actuators.arm_right_left_prep_take()
    #await asyncio.sleep(0.1)
    await actuators.pumps_on()
    await asyncio.sleep(0.1)
    await actuators.arm_right_left_take_y_1_0()
    await asyncio.sleep(0.1)
    #await actuators.position_defensive_laterale()
    await actuators.goldo_lifts_move(800)
    await asyncio.sleep(0.5)

@robot.sequence
async def do_grab_y_0110():
    #await actuators.arm_right_left_prep_take()
    #await asyncio.sleep(0.1)
    await actuators.pumps_on()
    await asyncio.sleep(0.1)
    await actuators.arm_right_left_take_y_1_1()
    await asyncio.sleep(0.1)
    #await actuators.position_defensive_laterale()
    await actuators.goldo_lifts_move(800)
    await asyncio.sleep(0.5)

@robot.sequence
async def do_grab_y_1001():
    #await actuators.arm_right_left_prep_take()
    #await asyncio.sleep(0.1)
    await actuators.pumps_on()
    await asyncio.sleep(0.1)
    await actuators.arm_right_left_take_y_0_0()
    await asyncio.sleep(0.1)
    #await actuators.position_defensive_laterale()
    await actuators.goldo_lifts_move(800)
    await asyncio.sleep(0.5)

@robot.sequence
async def do_grab_y_1010():
    #await actuators.arm_right_left_prep_take()
    #await asyncio.sleep(0.1)
    await actuators.pumps_on()
    await asyncio.sleep(0.1)
    await actuators.arm_right_left_take_y_0_1()
    await asyncio.sleep(0.1)
    #await actuators.position_defensive_laterale()
    await actuators.goldo_lifts_move(800)
    await asyncio.sleep(0.5)

@robot.sequence
async def do_grab_y_1100():
    #await actuators.arm_right_prep_take()
    #await asyncio.sleep(0.1)
    await actuators.right_pump_on()
    await asyncio.sleep(0.1)
    await actuators.arm_right_take_y_0()
    await asyncio.sleep(0.1)
    #await actuators.position_defensive_laterale_d()
    await actuators.goldo_lift_right_move(800)
    await asyncio.sleep(0.2)

    await propulsion.translation(0.040, 0.2)
    await asyncio.sleep(0.1)

    #await actuators.arm_left_prep_take()
    #await asyncio.sleep(0.1)
    await actuators.left_pump_on()
    await asyncio.sleep(0.1)
    await actuators.arm_left_take_y_2()
    await asyncio.sleep(0.1)
    #await actuators.position_defensive_laterale_g()
    await actuators.goldo_lift_left_move(800)
    await asyncio.sleep(0.5)

grab_y_funcs = {
    "0011":do_grab_y_0011,
    "0101":do_grab_y_0101,
    "0110":do_grab_y_0110,
    "1001":do_grab_y_1001,
    "1010":do_grab_y_1010,
    "1100":do_grab_y_1100,
}


########################################################################################
### DROP Y
########################################################################################

@robot.sequence
async def do_drop_y_1001():
    #await actuators.arm_right_left_prep_take()
    #await asyncio.sleep(0.1)
    await actuators.arm_right_left_drop_y_0_0()
    await asyncio.sleep(0.1)
    await actuators.pumps_off()
    await asyncio.sleep(0.1)
    await actuators.position_defensive_laterale()
    await asyncio.sleep(0.1)

@robot.sequence
async def do_drop_y_0110():
    #await actuators.arm_right_left_prep_take()
    #await asyncio.sleep(0.1)
    await actuators.arm_right_left_drop_y_1_1()
    await asyncio.sleep(0.1)
    await actuators.pumps_off()
    await asyncio.sleep(0.1)
    await actuators.position_defensive_laterale()
    await asyncio.sleep(0.1)

@robot.sequence
async def do_drop_y_42():
    #await actuators.arm_right_left_prep_take()
    #await asyncio.sleep(0.1)
    await actuators.arm_right_left_drop_y_42()
    await asyncio.sleep(0.1)
    await actuators.pumps_off()
    await asyncio.sleep(0.1)
    await actuators.position_defensive_laterale()
    await asyncio.sleep(0.1)




########################################################################################
### TEST & EXPERIMENTAL 
########################################################################################

@robot.sequence
async def test_goto_first_grab_wp1():
    await propulsion.moveTo(poses.First_grab_wp1, global_long_speed)
    await asyncio.sleep(global_long_sleep)

@robot.sequence
async def test_goto_inter_test_wp():
    await propulsion.pointTo(poses.Inter_wp0, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Inter_wp0, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    #await propulsion.pointTo(poses.Inter_wp1, global_turn_speed)
    #await asyncio.sleep(global_short_sleep)
    #await propulsion.moveTo(poses.Inter_wp1, global_long_speed)
    #await asyncio.sleep(global_short_sleep)
    await propulsion.pointTo(poses.Inter_test_wp, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Inter_test_wp, global_long_speed)
    await asyncio.sleep(global_short_sleep)

@robot.sequence
async def test_goto_action1_grab_wp1():
    await propulsion.pointTo(poses.Action1_grab_wp1, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action1_grab_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action1_grab_wp1[2], global_turn_speed)

@robot.sequence
async def test_goto_action1_drop_wp1():
    await propulsion.pointTo(pt=poses.Action1_drop_wp1, yaw_rate=global_turn_speed, back=True)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action1_drop_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action1_drop_wp1[2], global_turn_speed)

@robot.sequence
async def test_goto_action2_grab_wp1():
    await propulsion.pointTo(poses.Action2_grab_wp1, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action2_grab_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action2_grab_wp1[2], global_turn_speed)

@robot.sequence
async def test_goto_action2_drop_wp1():
    await propulsion.pointTo(pt=poses.Action2_drop_wp1, yaw_rate=global_turn_speed, back=False)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action2_drop_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action2_drop_wp1[2], global_turn_speed)

@robot.sequence
async def test_goto_action3_grab_wp1():
    await propulsion.pointTo(poses.Action3_grab_wp1, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action3_grab_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action3_grab_wp1[2], global_turn_speed)

@robot.sequence
async def test_goto_action3_drop_wp1():
    await propulsion.pointTo(pt=poses.Action3_drop_wp1, yaw_rate=global_turn_speed, back=False)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Action3_drop_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.faceDirection(poses.Action3_drop_wp1[2], global_turn_speed)


@robot.sequence
async def aruco_x_detection_async():
    print ("aruco_x_detection_async()")
    cam.aruco_x_detection()

@robot.sequence
async def aruco_y_detection_async():
    cam.aruco_y_detection()

