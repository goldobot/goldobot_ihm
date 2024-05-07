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
solar_panels = False
solar_panels_score = 0

#Task pour verifier si un robot prend .. certains objets ..
async def check_areas():
    global check_areas_b
    global solar_panels
    global solar_panels_score
    while check_areas_b:
        if lidar.objectInRectangle([2.0, -0.5], [1.5, 0.5]):
            print("SOLAR PANELS DETECTION")
            solar_panels_score = 0
            solar_panels = False
        await asyncio.sleep(0.2)


@robot.sequence
async def prematch():

    global poses

    await robot.setScore(0)

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

    if robot.side == pos.Side.Blue:
        await propulsion.faceDirection(140, 1.5)
    else:
        await propulsion.faceDirection(-140, 1.5)

    await propulsion.moveTo(poses.start_pose, 0.2)

    if robot.side == pos.Side.Blue:
        await propulsion.faceDirection(90, 1.5)
        await asyncio.sleep(0.5)
    else:
        await propulsion.faceDirection(-90, 1.5)
        await asyncio.sleep(0.5)

    await propulsion.translation(-0.05, 0.5)

    if robot.side == pos.Side.Blue:
        await propulsion.faceDirection(90, 1.5)
        await asyncio.sleep(0.5)
    else:
        await propulsion.faceDirection(-90, 1.5)
        await asyncio.sleep(0.5)

    await actuators.lift_right_solar_panel()
    await actuators.lift_left_solar_panel()
    await asyncio.sleep(0.5)
    await actuators.arms_down()

    await robot.gpioSet('keyboard_led', True)

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
    global solar_panels
    global solar_panels_score

    check_areas_b = True
    five_secs_limit = False
    in_zone = False
    end_action = None
    solar_panels_score = 0

    await propulsion.setAccelerationLimits(1,1,20,20)
    strategy.addTimerCallback(1, end_match)
    #strategy.addTimerCallback(15, need_end_match)

    # end_action = strategy.create_action('return_home')
    # end_action.opponent_radius = 0.3
    # end_action.sequence_prepare = 'arms_close'
    # end_action.sequence = 'end_match'
    # end_action.enabled = True
    # end_action.priority = 0
    # end_action.begin_pose = poses.zone_fin

    robot._adversary_detection_enable = True
    try:
        tasklidar = asyncio.create_task(check_areas())
    except:
        print("Tasklidar failed")

    # Premier panneau
    if robot.side == pos.Side.Blue:
        await actuators.lift_right_solar_panel()
        await actuators.prepare_solar_panel_right()
        await actuators.lift_right_solar_panel()
        await asyncio.sleep(1.0)
        await actuators.hit_solar_panel_right()
    else:
        await actuators.lift_left_solar_panel()
        await actuators.prepare_solar_panel_left()
        await actuators.lift_left_solar_panel()
        await asyncio.sleep(1.0)
        await actuators.hit_solar_panel_left()
    await robot.setScore(robot.score + 5)

    # 2eme panneau
    await propulsion.moveToRetry(poses.panneau_2, 0.6)
    if robot.side == pos.Side.Blue:
        await propulsion.faceDirection(90, 1.5)
        
        await actuators.hit_solar_panel_right()
    else:
        await propulsion.faceDirection(-90, 1.5)
        await actuators.hit_solar_panel_left()
    await robot.setScore(robot.score + 5)

    # 3eme panneau
    await propulsion.moveToRetry(poses.panneau_3, 0.6)
    if robot.side == pos.Side.Blue:
        await propulsion.faceDirection(90, 1.5)
        await actuators.hit_solar_panel_right()
    else:
        await propulsion.faceDirection(-90, 1.5)
        await actuators.hit_solar_panel_left()
    await robot.setScore(robot.score + 5)

    # Check panneaux milieu
    try:
        if not lidar.objectInRectangle([2.0, -0.5], [1.5, 0.5]):
            await propulsion.moveToRetry(poses.panneau_4, 0.6)
            if robot.side == pos.Side.Blue:
                await propulsion.faceDirection(90, 3.0)
                await actuators.hit_solar_panel_right()
            else:
                await propulsion.faceDirection(-90, 3.0)
                await actuators.hit_solar_panel_left()
            solar_panels_score = solar_panels_score + 5
        else:
            raise Exception("apapossib")
        
        if not lidar.objectInRectangle([2.0, -0.5], [1.5, 0.5]):
            await propulsion.moveToRetry(poses.panneau_5, 0.6)
            if robot.side == pos.Side.Blue:
                await propulsion.faceDirection(90, 3.0)
                await actuators.hit_solar_panel_right()
            else:
                await propulsion.faceDirection(-90, 3.0)
                await actuators.hit_solar_panel_left()
            solar_panels_score = solar_panels_score + 5
        else:
            raise Exception("apapossib")

        if not lidar.objectInRectangle([2.0, -0.5], [1.5, 0.5]):
            await propulsion.moveToRetry(poses.panneau_6, 0.6)
            if robot.side == pos.Side.Blue:
                await propulsion.faceDirection(90, 3.0)
                await actuators.hit_solar_panel_right()
            else:
                await propulsion.faceDirection(-90, 3.0)
                await actuators.hit_solar_panel_left()
            solar_panels_score = solar_panels_score + 5
            solar_panels = True
        else:
            raise Exception("apapossib")
    except:
        print("Problem doing central panels")
        await propulsion.translation(-0.15, 0.5)
        await propulsion.pointTo(poses.backup_1, 8.0)
        await propulsion.moveToRetry(poses.backup_1, 0.6)
    else:
        await propulsion.translation(-0.15, 0.5)
    finally:
        await actuators.arms_safe()

    await propulsion.pointTo(poses.prise_plantes_1, 8.0)
    await actuators.arms_down()

    await propulsion.moveToRetry(poses.prise_plantes_1, 0.6)
    await actuators.arms_collect()
    await propulsion.pointTo(poses.depose_plantes_1, 8.0)
    await propulsion.moveToRetry(poses.depose_plantes_1, 0.4)
    await robot.setScore(robot.score + 6)
    try:
        await propulsion.translation(-0.3, 0.4)
    except:
        await propulsion.translation(0.15, 0.4)
        await propulsion.translation(-0.15, 0.4)
    finally:
        await actuators.arms_safe()

    await propulsion.pointTo(poses.prise_plantes_2, 8.0)
    await propulsion.moveToRetry(poses.prise_plantes_2, 0.6)
    await actuators.arms_collect()
    await propulsion.pointTo(poses.retour_plantes_3, 8.0)
    await propulsion.moveToRetry(poses.retour_plantes_3, speed=0.4)
    await robot.setScore(robot.score + 3)
    try:
        await propulsion.translation(-0.3, 0.4)
    except:
        await propulsion.translation(0.15, 0.4)
        await propulsion.translation(-0.15, 0.4)
    finally:
        await actuators.arms_safe()

    await asyncio.sleep(0.5)

    if not lidar.objectInRectangle(poses.zone_1, poses.zone_2):
        if not lidar.objectInDisk(poses.zone_3, 0.3):
            await propulsion.pointTo(poses.prise_plantes_3, 5.0)
            await propulsion.moveToRetry(poses.prise_plantes_3, 0.6)
            if not lidar.objectInRectangle(poses.zone_1, poses.zone_2):
                if not lidar.objectInDisk(poses.zone_3, 0.2):
                    await propulsion.pointTo(poses.depose_plantes_3, 5.0)
                    await actuators.arms_collect()
                    await propulsion.moveToRetry(poses.depose_plantes_3, 0.4)
                    await robot.setScore(robot.score + 3)
                    try:
                        await propulsion.translation(-0.3, 0.4)
                    except:
                        await propulsion.translation(0.15, 0.4)
                        await propulsion.translation(-0.15, 0.4)
                    finally:
                        await actuators.arms_safe()        

    Ttest = time.time()
    time_val = 70-(Ttest-T0)
    if time_val > 0:
        await asyncio.sleep(70-(Ttest-T0))
    
    T1 = time.time()
    # Retry panneaux
    try:
        if not solar_panels:
            if T1 - T0 < 90:
                if not lidar.objectInRectangle([2.0, -0.5], [1.5, 0.5]):
                    await propulsion.translation(-0.3, 0.4)
                    await asyncio.sleep(0.5)
                    await propulsion.pointTo(poses.panneau_4, 8.0)
                    await actuators.arms_safe()
                    await propulsion.moveToRetry(poses.panneau_4, 1.0)

                    if robot.side == pos.Side.Blue:
                        await propulsion.faceDirection(90, 3.0)
                        await asyncio.sleep(0.5)
                    else:
                        await propulsion.faceDirection(-90, 3.0)
                        await asyncio.sleep(0.5)

                    if robot.side == pos.Side.Blue:
                        await actuators.lift_right_solar_panel()
                        await actuators.prepare_solar_panel_right()
                        await actuators.lift_right_solar_panel()
                        await asyncio.sleep(1.0)
                        await actuators.hit_solar_panel_right()
                    else:
                        await actuators.lift_left_solar_panel()
                        await actuators.prepare_solar_panel_left()
                        await actuators.lift_left_solar_panel()
                        await asyncio.sleep(1.0)
                        await actuators.hit_solar_panel_left()
                    solar_panels_score = solar_panels_score + 5
                    solar_panels = True

                    T2 = time.time()
                    if T2 - T0 < 80:
                        if not lidar.objectInRectangle([2.0, -0.5], [1.5, 0.5]):
                            await propulsion.moveToRetry(poses.panneau_5, 0.6)
                            if robot.side == pos.Side.Blue:
                                await propulsion.faceDirection(90, 1.5)
                                await actuators.hit_solar_panel_right()
                            else:
                                await propulsion.faceDirection(-90, 1.5)
                                await actuators.hit_solar_panel_left()
                        else:
                            raise Exception("apapossib")
                    solar_panels_score = solar_panels_score + 5

                    T3 = time.time()
                    if T3 - T0 < 80:
                        if not lidar.objectInRectangle([2.0, -0.5], [1.5, 0.5]):
                            await propulsion.moveToRetry(poses.panneau_6, 0.6)
                            if robot.side == pos.Side.Blue:
                                await propulsion.faceDirection(90, 1.5)
                                await actuators.hit_solar_panel_right()
                            else:
                                await propulsion.faceDirection(-90, 1.5)
                                await actuators.hit_solar_panel_left()
                        else:
                            raise Exception("apapossib")
                    solar_panels_score = solar_panels_score + 5
    except:
        await propulsion.translation(-0.15, 0.5)
    else:
        await propulsion.translation(-0.15, 0.5)
    finally:
        await actuators.arms_safe()


    await goto_final_pose()

    if solar_panels:
        print("SOLAR_PANELS_SCORE")
        print(solar_panels_score)
        print("SOLAR_PANELS_SCORE")
        await robot.setScore(robot.score + solar_panels_score)

    end_action.enabled = False

def get_robot_actual_zone():
    my_x = propulsion.pose.position.x
    my_y = propulsion.pose.position.y

    return get_point_zone(my_x,my_y)

@robot.sequence
async def goto_final_pose():
    global in_zone
    global check_areas_b
    print('******************')
    print('******************')
    print('  retour en zone  ')
    print('******************')
    print('******************')
    await propulsion.pointTo(poses.end_pose, 5.0)
    await propulsion.moveToRetry(poses.end_pose, 0.5)
    await robot.setScore(robot.score + 10)


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
    global solar_panels_score
    global solar_panels
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
