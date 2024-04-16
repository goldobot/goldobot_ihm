# import base modules
import asyncio
import numpy as np

# import modules from sequence directory
from . import pince
from . import positions as pos
from . import recalages
from . import robot_config as rc
from . import barillet
from . import gateau
from . import utils

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

check_areas_b = True
assiette_1 = True
assiette_2 = True
assiette_3 = True
jaune_1 = True
rose_1 = True
jaune_2 = True
rose_2 = True
five_secs_limit = False
in_zone = False
antivol = False

#Task pour verifier si un robot prend les gateaux marrons
async def check_areas():
    global assiette_1
    global rose_1
    global jaune_1
    global assiette_2
    global assiette_3
    global rose_2
    global jaune_2
    global check_areas_b
    while check_areas_b:
        if lidar.objectInDisk(poses.marron_assiette_1, 0.20):
            assiette_1 = False
        if lidar.objectInDisk(poses.marron_assiette_2, 0.20):
            assiette_2 = False
        if lidar.objectInDisk(poses.marron_assiette_3, 0.20):
            assiette_2 = False
        if lidar.objectInDisk(poses.rose_1, 0.20):
            rose_1 = False
        if lidar.objectInDisk(poses.rose_2, 0.20):
            rose_2 = False
        if lidar.objectInDisk(poses.jaune_1, 0.20):
            jaune_1 = False
        if lidar.objectInDisk(poses.jaune_2, 0.20):
            jaune_2 = False
        await asyncio.sleep(0.3)


@robot.sequence
async def prematch():

    global poses

    if robot.side == pos.Side.Blue:
        poses = pos.BluePoses
    elif robot.side == pos.Side.Green:
        poses = pos.GreenPoses
    else:
        raise RuntimeError('Side not set')

    # Propulsion
    await lidar.stop()
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    await pneumatic.lcd_off()
    await pneumatic.led_on()
    await barillet.reset_valves()
    await barillet.start_compressor()
    await barillet.barillet_init()
    await asyncio.sleep(2)
    await pince.pince_init()
    await pince.pince_take()
    await pince.chariot_close()
    await barillet.barillet_pose_2()
    
    # Lidar
    robot._adversary_detection_enable = False

    # Placement
    await recalages.recalage()
    if robot.start_zone == 4 or robot.start_zone == 7:
        await propulsion.pointTo(poses.waypoint_rush_initial, 1.0)

    await robot.setScore(0)
    await robot.gpioSet('keyboard_led', True)
    await lidar.start()

    end_action = strategy.create_action('return_home')
    end_action.sequence_prepare = ''
    end_action.sequence = 'end_match'
    end_action.enabled = True
    end_action.priority = 0
    end_action.begin_pose = poses.zone_fin

    return True


@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """

    end_action = strategy.create_action('return_home')
    end_action.opponent_radius = 0.3
    end_action.sequence_prepare = 'pince_take'
    end_action.sequence = 'end_match'
    end_action.enabled = True
    end_action.priority = 0
    end_action.begin_pose = poses.zone_fin

    global assiette_1
    global rose_1
    global jaune_1
    global assiette_2
    global assiette_3
    global rose_2
    global jaune_2
    global check_areas_b
    global five_secs_limit
    global in_zone
    global antivol

    five_secs_limit = False
    in_zone = False
    antivol = False

    await propulsion.setAccelerationLimits(1,1,20,20)
    strategy.addTimerCallback(1, the_end)
    strategy.addTimerCallback(2, robot_in_zone)
    strategy.addTimerCallback(15, disable_antivol)

    robot._adversary_detection_enable = True
    #tasklidar = asyncio.create_task(check_areas())

    # Collecte gateaux
    if robot.start_zone == 4 or robot.start_zone == 7:
        await pince.pince_open()
        await propulsion.trajectorySpline(traj_depart, 1.2)
    
        await gateau.prend_gateau1()

        await propulsion.pointTo(poses.pose_gateau_1, 5.0)
        await propulsion.trajectorySpline(traj_retour, 1.2)
        await propulsion.pointTo(poses.prise_rose, 5.0)
        await pince.pince_open()
        await asyncio.sleep(0.2)
        await propulsion.moveToRetry(poses.prise_rose, 1.0)
        
        await gateau.prend_gateau5()

        await pince.pince_open()
        await asyncio.sleep(0.2)
        await propulsion.moveToRetry(poses.prise_jaune, 1.0)

        await gateau.prend_gateau3()
    elif robot.start_zone == 3 or robot.start_zone == 8:
        await pince.pince_open()
        await propulsion.moveToRetry(poses.prise_marron_alt, 1.2)
        await asyncio.sleep(0.2)

        await gateau.prend_gateau1()

        await pince.pince_open()
        await propulsion.pointTo(poses.prise_inter_alt, 5.0)
        await propulsion.moveToRetry(poses.prise_inter_alt, 1.0)
        await propulsion.pointTo(poses.prise_jaune_alt, 5.0)
        await propulsion.moveToRetry(poses.prise_jaune_alt, 1.0)

        await gateau.prend_gateau3()

        await pince.pince_open()
        await propulsion.pointTo(poses.prise_rose_alt, 5.0)
        await propulsion.moveToRetry(poses.prise_rose_alt, 1.2)

        await gateau.prend_gateau5()

        await propulsion.translation(-0.3, 1.2)
    else:
        return

    # Construction gateaux
    #await propulsion.pointTo(poses.pose_aruco, 5.0)
    #await propulsion.moveToRetry(poses.pose_aruco, 0.5)
    await propulsion.pointTo(poses.pose_gateau_1, 5.0)
    await propulsion.moveToRetry(poses.pose_gateau_1, 1.0)

    if robot.side == pos.Side.Blue:
        await propulsion.faceDirection(-90, 5.0)
    elif robot.side == pos.Side.Green:
        await propulsion.faceDirection(90, 5.0)

    await gateau.build_cake_1()
    test = await utils.get_cake_layers()
    await pince.recentre_cerise()
    await pince.chariot_close()
    await gateau.pose_cerise(2)
    await pince.pince_open()

    if (await utils.get_cake_layers() == test + 1):
        if test == 3:
            await robot.setScore(robot.score + 10)
        else:
            await robot.setScore(robot.score + test + 3)
    else:
        await robot.setScore(robot.score + test)
    
    await propulsion.translation(-0.15, 1.2)

    await gateau.build_cake_1()
    test = await utils.get_cake_layers()
    await pince.recentre_cerise()
    await pince.chariot_close()
    await gateau.pose_cerise(4)
    
    if (await utils.get_cake_layers() == test + 1):
        if test == 3:
            await robot.setScore(robot.score + 10)
        else:
            await robot.setScore(robot.score + test + 3)
    else:
        await robot.setScore(robot.score + test)

    if robot.side == pos.Side.Blue:
        await propulsion.faceDirection(-45, 2.0)
    elif robot.side == pos.Side.Green:
        await propulsion.faceDirection(45, 2.0)
    await pince.chariot_open()
    await pince.pince_open()
    await asyncio.sleep(0.4)
    await pince.chariot_close()
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(0, 2.0)
    await propulsion.translation(-0.15, 1.2)

    await gateau.build_last_cake()
    test = await utils.get_cake_layers()
    await pince.recentre_cerise()
    await pince.chariot_close()
    await gateau.pose_cerise(6)

    if (await utils.get_cake_layers() == test + 1):
        if test == 3:
            await robot.setScore(robot.score + 10)
        else:
            await robot.setScore(robot.score + test + 3)
    else:
        await robot.setScore(robot.score + test)

    if robot.side == pos.Side.Blue:
        await propulsion.faceDirection(-135, 2.0)
    elif robot.side == pos.Side.Green:
        await propulsion.faceDirection(135, 2.0)
    await pince.chariot_open()
    await pince.pince_open()
    await asyncio.sleep(0.4)
    await pince.chariot_close()
    await asyncio.sleep(0.2)
    await pince.pince_take()
    await propulsion.faceDirection(0, 2.0)
    await propulsion.translation(0.20, 1.2)

    await barillet.reset_valves()

    antivol = True

    while antivol is True:
        asyncio.sleep(0.2)
    # retour en zone
    await goto_final_pose()
    end_action.enabled = False

@robot.sequence
async def goto_final_pose():
    global in_zone
    print('******************')
    print('******************')
    print('  retour en zone  ')
    print('******************')
    print('******************')
    await propulsion.pointTo(poses.zone_presque_fin, 5.0)
    await pince.pince_take()
    final_speed = 1.0
    final_zone = get_point_zone(poses.zone_fin[0],poses.zone_fin[1])
    print ("final_zone = {}".format(final_zone))
    for i in range(1,3):
        try:
            await propulsion.moveTo(poses.zone_presque_fin, final_speed)
            break
        except:
            print('!!!!!!!!!!!!!!!!!!!!!')
            print(' EXCEPTION           ')
            print('!!!!!!!!!!!!!!!!!!!!!')
            print(" robot_pose = ({}, {})".format(propulsion.pose.position.x, propulsion.pose.position.y))
            await asyncio.sleep(1.0)
            print('Clear error')
            await propulsion.clearError()
            final_speed = 0.4
            my_x = propulsion.pose.position.x
            my_y = propulsion.pose.position.y
            zpf_x = poses.zone_presque_fin[0]
            zpf_y = poses.zone_presque_fin[1]
            dx = zpf_x - my_x
            dy = zpf_y - my_y
            if ((dx*dx+dy*dy)<(0.15*0.15)):
                print('Disable adversary detection')
                robot._adversary_detection_enable = False
                await asyncio.sleep(0.5)
                break
    robot._adversary_detection_enable = False
    robot_actual_zone = get_robot_actual_zone()
    print ("robot_actual_zone = {}".format(robot_actual_zone))
    if robot_actual_zone == final_zone:
        return
    buddy_actual_zone = get_buddy_actual_zone()
    if (final_zone == buddy_actual_zone):
        await propulsion.pointTo(poses.zone_fin, 5.0)
        #await propulsion.moveToRetry(poses.zone_fin, 0.2)
        await propulsion.moveToRetry(poses.zone_fin, 0.2, -0.01, 10, True)
        #try :
        #    await propulsion.moveTo(poses.zone_fin, 0.2)
        #except:
        #    print ("EXCEPTION (mais on s'en fout!..)")
        #in_zone = True
        await propulsion.faceDirection(0, 5.0)
    else:
        await propulsion.pointTo(poses.zone_fin_au_fond, 5.0)
        #await propulsion.moveToRetry(poses.zone_fin_au_fond, 0.2)
        await propulsion.moveToRetry(poses.zone_fin_au_fond, 0.2, -0.01, 10, True)
        #try :
        #    await propulsion.moveToRetry(poses.zone_fin_au_fond, 0.2)
        #except:
        #    print ("EXCEPTION (mais on s'en fout!..)")
        in_zone = True

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
    buddy_final_zone = get_buddy_actual_zone()
    print(" buddy_final_zone = {}".format(buddy_final_zone))

    if my_final_zone > 0:
        print("Robot in zone")
        if buddy_final_zone == my_final_zone:
            print("Other robot in zone")
            await robot.setScore(robot.score + 15)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +15 pour 'robots in zone'")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


def get_point_zone(x,y):
    my_x = x
    my_y = y

    if (my_x>0.0)   and (my_x<0.5)   and (my_y>0.4)   and (my_y<1.0)   and (robot.side == pos.Side.Green):
        return 1
    if (my_x>0.85)  and (my_x<1.4)   and (my_y>0.4)   and (my_y<1.0)   and (robot.side == pos.Side.Blue):
        return 2
    if (my_x>1.6)   and (my_x<2.15)  and (my_y>0.4)   and (my_y<1.0)   and (robot.side == pos.Side.Green):
        return 3
    if (my_x>2.5)   and (my_x<3.0)   and (my_y>0.4)   and (my_y<1.0)   and (robot.side == pos.Side.Blue):
        return 4
    if (my_x>2.4)   and (my_x<3.0)   and (my_y>0.0)   and (my_y<0.55)  and (robot.side == pos.Side.Green):
        return 5
    if (my_x>2.4)   and (my_x<3.0)   and (my_y<0.0)   and (my_y>-0.55) and (robot.side == pos.Side.Blue):
        return 6
    if (my_x>2.5)   and (my_x<3.0)   and (my_y<-0.4)  and (my_y>-1.0)  and (robot.side == pos.Side.Green):
        return 7
    if (my_x>1.6)   and (my_x<2.15)  and (my_y<-0.4)  and (my_y>-1.0)  and (robot.side == pos.Side.Blue):
        return 8
    if (my_x>0.85)  and (my_x<1.4)   and (my_y<-0.4)  and (my_y>-1.0)  and (robot.side == pos.Side.Green):
        return 9
    if (my_x>0.0)   and (my_x<0.5)   and (my_y<-0.4)  and (my_y>-1.0)  and (robot.side == pos.Side.Blue):
        return 10

    return 0


def get_robot_actual_zone():
    my_x = propulsion.pose.position.x
    my_y = propulsion.pose.position.y

    return get_point_zone(my_x,my_y)


def get_buddy_actual_zone():
    if lidar.objectInRectangle([0.0, 0.5], [0.5, 1.0])  and (robot.side == pos.Side.Green):
        return 1
    if lidar.objectInRectangle([0.85, 0.5], [1.4, 1.0]) and (robot.side == pos.Side.Blue):
        return 2
    if lidar.objectInRectangle([1.6, 0.5], [2.15, 1.0]) and (robot.side == pos.Side.Green):
        return 3
    if lidar.objectInRectangle([2.5, 0.5], [3.0, 1.0])  and (robot.side == pos.Side.Blue):
        return 4
    if lidar.objectInRectangle([2.5, 0.0], [3.0, 0.55]) and (robot.side == pos.Side.Green):
        return 5
    if lidar.objectInRectangle([2.5, 0.0], [3.0,-0.55]) and (robot.side == pos.Side.Blue):
        return 6
    if lidar.objectInRectangle([2.5,-0.5], [3.0,-1.0])  and (robot.side == pos.Side.Green):
        return 7
    if lidar.objectInRectangle([1.6,-0.5], [2.15,-1.0]) and (robot.side == pos.Side.Blue):
        return 8
    if lidar.objectInRectangle([0.85,-0.5], [1.4,-1.0]) and (robot.side == pos.Side.Green):
        return 9
    if lidar.objectInRectangle([0.0,-0.5], [0.5,-1.0])  and (robot.side == pos.Side.Blue):
        return 10

    return 0


async def need_end_match():
    global five_secs_limit
    print('5 sec limit reached')
    five_secs_limit = True


async def the_end():
    await barillet.reset_valves()
    await pneumatic.lcd_on()
    await robot.setScore(robot.score + 5)
    await robot.gpioSet('keyboard_led', False)
    await lidar.stop()
    await servos.setMaxTorque(['ascenseur', 'rotor'], 0.0)    
    await servos.setEnable(['ascenseur', 'rotor'], False)

async def disable_antivol():
    global antivol
    antivol = False

async def end_match():
    print('end match callback')
    strategy.current_action.enabled = False
