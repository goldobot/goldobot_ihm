# Sequences de la Coupe de France 2023 - gardees pour test & debug

# import base modules
import asyncio
import numpy as np

import time

# import modules from sequence directory
from . import positions as pos
from . import recalages
from . import actuators
from . import robot_config as rc

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

check_areas_b = True
five_secs_limit = False
in_zone = False
robot_in_zone_done = False
end_action = None

#Task pour verifier si un robot prend .. certains objets ..
async def check_areas():
    global check_areas_b
    while check_areas_b:
        # FIXME : TODO
        #if lidar.objectInDisk(poses.marron_assiette_1, 0.20):
        #    assiette_1 = False
        #    available_stacks = available_stacks - 1
        await asyncio.sleep(0.2)


@robot.sequence
async def prematch():

    global poses

    if robot.side == pos.Side.Blue:
        poses = pos.BluePoses
    elif robot.side == pos.Side.Yellow:
        poses = pos.YellowPoses
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
    await lidar.start()

    # Actionneurs
    await actuators.arms_initialize()

    # Placement
    await recalages.recalage()

    return True


@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """

    T0 = time.time()

    global check_areas_b
    global five_secs_limit
    global in_zone
    global robot_in_zone_done
    global end_action

    check_areas_b = True
    available_stacks = 7
    minicake_done = False
    assiette_1 = True
    assiette_2 = True
    assiette_3 = True
    jaune_1 = True
    rose_1 = True
    jaune_2 = True
    rose_2 = True
    five_secs_limit = False
    in_zone = False
    robot_in_zone_done = False
    end_action = None

    await propulsion.setAccelerationLimits(1,1,20,20)
    strategy.addTimerCallback(1, end_match)
    strategy.addTimerCallback(2, robot_in_zone)
    strategy.addTimerCallback(15, need_end_match)

    end_action = strategy.create_action('return_home')
    end_action.opponent_radius = 0.3
    end_action.sequence_prepare = 'arms_close'
    end_action.sequence = 'end_match'
    end_action.enabled = True
    end_action.priority = 0
    end_action.begin_pose = poses.zone_fin

    robot._adversary_detection_enable = True
    try:
        tasklidar = asyncio.create_task(check_areas())
    except:
        print("Tasklidar failed")

    T1 = time.time()
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    print ("T match_timer = {}".format(T1-T0))
    print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    print('*********************')
    print('Rush initial         ')
    print('*********************')
    if robot.start_zone == 1 or robot.start_zone == 6:
        pass
    else:
        pass
    
    await actuators.goldo_lifts_move(520, 80)

    check_areas_b = False

    # retour en zone
    await goto_final_pose()
    end_action.enabled = False

def get_point_zone(x,y):
    my_x = x
    my_y = y

    if (my_x>1.550)   and (my_x<2.000)   and (my_y>-1.500)   and (my_y<-1.050)   and (robot.side == pos.Side.Blue):
        return 1
    if (my_x>0.775)   and (my_x<1.225)   and (my_y>-1.500)   and (my_y<-1.050)   and (robot.side == pos.Side.Yellow):
        return 2
    if (my_x>0.000)   and (my_x<0.450)   and (my_y>-1.500)   and (my_y<-1.050)   and (robot.side == pos.Side.Blue):
        return 3
    if (my_x>0.000)   and (my_x<0.450)   and (my_y> 1.050)   and (my_y< 1.500)   and (robot.side == pos.Side.Yellow):
        return 4
    if (my_x>0.775)   and (my_x<1.225)   and (my_y> 1.050)   and (my_y< 1.500)   and (robot.side == pos.Side.Blue):
        return 5
    if (my_x>1.550)   and (my_x<2.000)   and (my_y< 1.050)   and (my_y> 1.500)   and (robot.side == pos.Side.Yellow):
        return 6

    return 0

def get_robot_actual_zone():
    my_x = propulsion.pose.position.x
    my_y = propulsion.pose.position.y

    return get_point_zone(my_x,my_y)

@robot.sequence
async def goto_final_pose():
    global in_zone
    print('******************')
    print('******************')
    print('  retour en zone  ')
    print('******************')
    print('******************')
    await propulsion.pointTo(poses.zone_fin, 5.0)
    #await actuators.arms_close()
    final_speed = 1.0
    final_zone = get_point_zone(poses.zone_fin[0],poses.zone_fin[1])
    print ("final_zone = {}".format(final_zone))
    for i in range(1,3):
        try:
            await propulsion.moveTo(poses.zone_fin, final_speed)
            break
        except:
            print('!!!!!!!!!!!!!!!!!!!!!')
            print(' EXCEPTION           ')
            print('!!!!!!!!!!!!!!!!!!!!!')
            print(" robot_pose = ({}, {})".format(propulsion.pose.position.x, propulsion.pose.position.y))
            await asyncio.sleep(1.0)
            print('Clear error')
            await propulsion.clearError()
            await propulsion.setMotorsEnable(True)
            await propulsion.setEnable(True)
            final_speed = 0.4
    robot._adversary_detection_enable = False
    robot_actual_zone = get_robot_actual_zone()
    print ("robot_actual_zone = {}".format(robot_actual_zone))

async def need_end_match():
    global five_secs_limit
    print('10 sec limit reached')
    five_secs_limit = True

async def the_end():
    global in_zone
    in_zone = True

@robot.sequence
async def end_match():
    global in_zone
    global end_action
    print('******************')
    print('******************')
    print('end match callback')
    print('******************')
    print('******************')
    end_action.enabled = False

    pass

    await robot.gpioSet("keyboard_led", False)
    print()
    print()
    print('******************')
    print('******************')
    print('    stop lidar    ')
    print('******************')
    print('******************')
    await lidar.stop()
    await asyncio.sleep(1.0)


@robot.sequence
async def robot_in_zone():
    global robot_in_zone_done

    if (robot_in_zone_done):
        print ("Warning : robot_in_zone() scheduled multiple times!..")
        return
    robot_in_zone_done = True
    robot._adversary_detection_enable = False

    print('******************')
    print('******************')
    print(' robot_in_zone()  ')
    print('******************')
    print('******************')
    await asyncio.sleep(1.0)
    print(" robot_pose = ({}, {})".format(propulsion.pose.position.x, propulsion.pose.position.y))

    my_final_zone = get_robot_actual_zone()
    print(" my_final_zone = {}".format(my_final_zone))

    if my_final_zone > 0:
        print("Robot in zone")
        await robot.setScore(robot.score + 15)
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print ("$ Score +15 pour 'robots in zone'")
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

async def arms_safe():
    await actuators.arms_close()

