# Sequences de la Coupe de France 2023 - gardees pour test & debug

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
from . import robot_config as rc

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

global_long_speed = 0.45
global_turn_speed = 2.0

global_short_sleep = 0.3
global_long_sleep  = 2.0

aruco_start_configuration = "0000"

@robot.sequence
async def prematch():

    global poses

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

    return True


@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """

    global aruco_start_configuration

    T0 = time.time()

    await propulsion.setAccelerationLimits(1,1,20,20)

    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    #robot._adversary_detection_enable = True
    await lidar.start()

    try:
        await strat_0()
    except:
        print ("EXCEPTION!")

    await actuators.pumps_off()
    await asyncio.sleep(global_short_sleep)
    await actuators.arms_close()
    await asyncio.sleep(global_short_sleep)

    await propulsion.pointTo(poses.Final_escape_wp, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveToRetry(poses.Final_escape_wp, global_long_speed)
    await asyncio.sleep(global_short_sleep)

    await propulsion.pointTo(poses.Final_pose_wp, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveToRetry(poses.Final_pose_wp, global_long_speed)
    await asyncio.sleep(global_short_sleep)

    await lidar.stop()

    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")


#reference x values:
# 501 -> ref_x1 = 0.510
# 562 -> ref_x2 = 0.560
# 616 -> ref_x3 = 0.610
# 671 -> ref_x4 = 0.660
@robot.sequence
async def aruco_start_detection():
    global aruco_start_configuration

    aruco_start_configuration = "0000"

    ref_x = [0.510, 0.560, 0.610, 0.660]
    segm_ref_x = [0.535, 0.585, 0.635]

    if (robot.start_zone==1):   # BLUE   (Y+,id=36)
        print("my_color = BLUE (id=36)")
        my_color = 36
    elif (robot.start_zone==2): # YELLOW (Y-,id=47)
        print("my_color = YELLOW (id=47)")
        my_color = 47
    else:
        print("No start zone!")
        return

    #detections_file = "/tmp/detections.txt"
    detections_file = "/tmp/last_good_detections.txt"

    detections = []
    try:
        with open(detections_file) as f:
            for line in f:
                print ("DETECTIONS FILE: {}".format(line)) 
                line = line.strip()
                parts = line.split()
                if len(parts) != 4:
                    continue
                ts_str, my_id_str, x_str, y_str = parts
                ts = float(ts_str)
                my_id = int(my_id_str)
                x_real = float(x_str)/1000.0
                y_real = float(y_str)/1000.0
                detections.append((ts,my_id,x_real,y_real))
    except:
        print ("Cannot read (and parse) {}".format(detections_file))
        return

    detections.sort(key=lambda d: d[2])

    pres_idx = []

    for i in range(len(detections)):
        ts, my_id, x_real, y_real = detections[i]
        print ("ts={:.2f} id={:d} x={:6.3f} y={:6.3f}".format(ts, my_id, x_real, y_real))
        if (x_real<segm_ref_x[0]):
            pres_idx.append(0)
        elif (x_real<segm_ref_x[1]):
            pres_idx.append(1)
        elif (x_real<segm_ref_x[2]):
            pres_idx.append(2)
        else:
            pres_idx.append(3)
    print("Present: {}".format(pres_idx))

    if (len(detections)<3 or len(detections)>4):
        print("len(detectionss)={}".format(len(detections)))
        print("Cannot detect aruco_start_configuration!")
        return

    if (len(detections)==3):
        miss_idx = None
        miss_color_code = None
        my_color_cnt = 0
        adv_color_cnt = 0
        for i in range(0,4):
            if (i not in pres_idx):
                miss_idx = i
        for i in range(0,3):
            if (detections[i][1]==my_color):
                my_color_cnt = my_color_cnt + 1
            else:
                adv_color_cnt = adv_color_cnt + 1
        print ("miss_idx={}".format(miss_idx))
        print ("my_color_cnt={}".format(my_color_cnt))
        print ("adv_color_cnt={}".format(adv_color_cnt))
        if (my_color_cnt>adv_color_cnt):
            miss_color_code = '0'
        else:
            miss_color_code = '1'
        print ("miss_color_code={}".format(miss_color_code))
        for i in range(0,3):
            if (detections[i][1]==my_color):
                aruco_start_configuration = aruco_start_configuration[:pres_idx[i]] + '1' + aruco_start_configuration[pres_idx[i]+1:]
            print("  STEP {} : {}".format(i,aruco_start_configuration))
        aruco_start_configuration = aruco_start_configuration[:miss_idx] + miss_color_code + aruco_start_configuration[miss_idx+1:]

    elif (len(detections)==4):
        for i in range(0,4):
            if (detections[i][1]==my_color):
                aruco_start_configuration = aruco_start_configuration[:i] + '1' + aruco_start_configuration[i+1:]

    print("aruco_start_configuration = {}".format(aruco_start_configuration))


async def do_push_0000():
    await propulsion.moveTo(poses.First_push, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_grab_wp2, global_long_speed)
    await asyncio.sleep(global_short_sleep)

async def do_grab_and_push_0011():
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
    await propulsion.pointTo(pt=poses.First_return_wp, yaw_rate=global_turn_speed, back=True)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_return_wp, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.pumps_off()
    await asyncio.sleep(global_short_sleep)


async def do_grab_and_push_0101():
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
    await propulsion.pointTo(pt=poses.First_return_wp, yaw_rate=global_turn_speed, back=True)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_return_wp, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.pumps_off()
    await asyncio.sleep(global_short_sleep)

async def do_grab_and_push_0110():
    #await propulsion.moveTo(poses.First_grab_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.test_grab_right()
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_push_out, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.pointTo(pt=poses.First_return_wp, yaw_rate=global_turn_speed, back=True)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_return_wp, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.pumps_off()
    await asyncio.sleep(global_short_sleep)

async def do_grab_and_push_1001():
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
    await propulsion.pointTo(pt=poses.First_return_wp, yaw_rate=global_turn_speed, back=True)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_return_wp, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.pumps_off()
    await asyncio.sleep(global_short_sleep)

async def do_grab_and_push_1010():
    await propulsion.moveTo(poses.First_grab_wp2, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.test_grab_right()
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_push_out, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.pointTo(pt=poses.First_return_wp, yaw_rate=global_turn_speed, back=True)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_return_wp, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await actuators.pumps_off()
    await asyncio.sleep(global_short_sleep)

async def do_grab_and_push_1100():
    await propulsion.moveTo(poses.First_push_out, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.First_grab_wp2, global_long_speed)
    await asyncio.sleep(global_short_sleep)


grab_and_push_funcs = {
    "0011":do_grab_and_push_0011,
    "0101":do_grab_and_push_0101,
    "0110":do_grab_and_push_0110,
    "1001":do_grab_and_push_1001,
    "1010":do_grab_and_push_1010,
    "1100":do_grab_and_push_1100,
}

@robot.sequence
async def strat_0():
    global aruco_start_configuration

    await propulsion.moveTo(poses.First_grab_wp1, global_long_speed)
    await asyncio.sleep(global_long_sleep)

    for i in range(0,5):
        print()
        print("================")
        print ("ARUCO TRY {}".format(i))
        print("----------------")
        try:
            await aruco_start_detection()
        except:
            print ("aruco_start_detection() failed")
            aruco_start_configuration = "0000"
        if (aruco_start_configuration!="0000"):
            print("VVVVVVVVVVVVVVVV")
            print()
            break
        print("----------------")
        print()
        await asyncio.sleep(1.0)

    if (aruco_start_configuration not in grab_and_push_funcs.keys()):
        await do_push_0000()
    else:
        await grab_and_push_funcs[aruco_start_configuration]()

    robot._adversary_detection_enable = True

    await propulsion.pointTo(poses.Inter_wp1, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Inter_wp1, global_long_speed)
    await asyncio.sleep(global_short_sleep)

    await propulsion.pointTo(poses.Inter_wp2, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Inter_wp2, global_long_speed)
    await asyncio.sleep(global_short_sleep)

    await actuators.arms_close()
    await asyncio.sleep(global_short_sleep)

    await actuators.lifts_high()
    await asyncio.sleep(global_short_sleep)

    await propulsion.pointTo(poses.Corner_wp, global_turn_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.moveTo(poses.Corner_wp, global_long_speed)
    await asyncio.sleep(global_short_sleep)
    await propulsion.pointTo(pt=poses.Border_wp1, yaw_rate=global_turn_speed, back=True)
    await asyncio.sleep(global_short_sleep)

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

    #await propulsion.pointTo(poses.Final_escape_wp, global_turn_speed)
    #await asyncio.sleep(global_short_sleep)
    #await propulsion.moveTo(poses.Final_escape_wp, global_long_speed)
    #await asyncio.sleep(global_short_sleep)
    #await propulsion.pointTo(poses.Final_pose_wp, global_turn_speed)
    #await asyncio.sleep(global_short_sleep)
    #await propulsion.moveTo(poses.Final_pose_wp, global_long_speed)
    #await asyncio.sleep(global_short_sleep)


@robot.sequence
async def test_dry_run():
    await propulsion.moveTo(poses.TEST_wp1, global_long_speed)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(poses.TEST_wp2, global_long_speed)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(poses.TEST_wp3, global_long_speed)
    await asyncio.sleep(0.5)
    await propulsion.moveTo(poses.TEST_wp4, global_long_speed)
    await asyncio.sleep(0.5)

    await propulsion.moveTo(poses.TEST_wp5, global_long_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp6, global_long_speed)
    await asyncio.sleep(1.0)

    await propulsion.pointTo(poses.TEST_wp7, global_turn_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp7, global_long_speed)
    await asyncio.sleep(1.0)

    await actuators.arms_close()
    await asyncio.sleep(0.5)

    await propulsion.pointTo(poses.TEST_wp8, global_turn_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp8, global_long_speed)
    await asyncio.sleep(1.0)

    await propulsion.pointTo(poses.TEST_wp9, global_turn_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp9, global_long_speed)
    await asyncio.sleep(1.0)

    await propulsion.pointTo(poses.TEST_wp10_N, global_turn_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp10, global_long_speed)
    await asyncio.sleep(10.0)

    await propulsion.pointTo(poses.TEST_wp11, global_turn_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp11, global_long_speed)
    await asyncio.sleep(1.0)

    await propulsion.pointTo(poses.TEST_wp12, global_turn_speed)
    await asyncio.sleep(1.0)
    await propulsion.moveTo(poses.TEST_wp12, global_long_speed)
    await asyncio.sleep(1.0)


@robot.sequence
async def test_start_adversary_detection():
    robot._adversary_detection_enable = False
    await lidar.start()
    robot._adversary_detection_enable = True

@robot.sequence
async def test_stop_adversary_detection():
    robot._adversary_detection_enable = False
    await lidar.stop()

