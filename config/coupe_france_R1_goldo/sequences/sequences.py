# import base modules
import asyncio
import numpy as np

# import modules from sequence directory
from . import positions as pos
from . import recalages
from . import canon_cerises
from . import distrib_cerises
from . import actuators
from . import robot_config as rc

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
end_action = None
cherry_in_dispenser = 6
cherry_in_gun = 1

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
            assiette_3 = False
        if lidar.objectInDisk(poses.rose_1, 0.20):
            rose_1 = False
        if lidar.objectInDisk(poses.rose_2, 0.20):
            rose_2 = False
        if lidar.objectInDisk(poses.jaune_1, 0.20):
            jaune_1 = False
        if lidar.objectInDisk(poses.jaune_2, 0.20):
            jaune_2 = False
        await asyncio.sleep(0.2)


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
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,2,2)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    
    # Lidar
    robot._adversary_detection_enable = False
    await lidar.start()

    # Actionneurs
    await distrib_cerises.distrib_enable()
    await distrib_cerises.distrib_neutral()
    await canon_cerises.canon_initialize()
    await distrib_cerises.distrib_haut()
    await actuators.arms_initialize()

    # Placement
    await recalages.recalage()

    # Score +5 pour presence panier
    await robot.setScore(5)
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print ("$ Score +5 pour presence panier")
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    await robot.gpioSet('keyboard_led', True)

    return True


@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """
    traj_depart = [
        poses.plat_start_pose,
        poses.plat_inter_pose,
        poses.prise_marron
    ]

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
    global end_action
    global cherry_in_dispenser
    global cherry_in_gun

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
    end_action = None
    cherry_in_dispenser = 6
    cherry_in_gun = 1

    await propulsion.setAccelerationLimits(1,1,20,20)
    # FIXME : DEBUG ++
    strategy.addTimerCallback(1, end_match)
    strategy.addTimerCallback(2, robot_in_zone)
    strategy.addTimerCallback(11, need_end_match)

    end_action = strategy.create_action('return_home')
    end_action.opponent_radius = 0.3
    end_action.sequence_prepare = 'arms_close'
    end_action.sequence = 'end_match'
    end_action.enabled = True
    end_action.priority = 0
    end_action.begin_pose = poses.zone_fin
    # FIXME : DEBUG --

    taskarms = asyncio.create_task(actuators.arms_collect())

    # await propulsion.pointTo(poses.prise_marron, 1.5)
    robot._adversary_detection_enable = True
    try:
        tasklidar = asyncio.create_task(check_areas())
    except:
        print("Tasklidar failed")

    print('*********************')
    print('Rush initial         ')
    print('*********************')
    if robot.start_zone == 1 or robot.start_zone == 10: 
        try:
            await propulsion.trajectorySpline(traj_depart, speed=0.5)
        except:
            print('!!!!!!!!!!!!!!!!!!!!!')
            print(' EXCEPTION           ')
            print('!!!!!!!!!!!!!!!!!!!!!')
            await asyncio.sleep(10.0)
            print('Clear error')
            await propulsion.clearError()
            await propulsion.translation(-0.15, 0.5)
            await propulsion.pointTo(poses.prise_marron, 1.0)
            await propulsion.moveToRetry(poses.prise_marron, 0.5)
    elif robot.start_zone == 2 or robot.start_zone == 9:
        print("alt start zone")
        await propulsion.moveToRetry(poses.prise_marron_alt, 1.0)
        assiette_1 = False
    else:
        await propulsion.pointTo(poses.prise_marron, 1.0)
        await propulsion.moveToRetry(poses.prise_marron, 0.5)
    await taskarms
    
    # Prise avec les bras
    print('*********************')
    print('Prise avec les bras  ')
    print('*********************')
    await actuators.arms_centering()

    # Depose marron
    print('*********************')
    print('Depose marron        ')
    print('*********************')
    await propulsion.pointTo(poses.pose_construction, 1.5)
    await propulsion.moveToRetry(poses.pose_construction, 1.0)
    await propulsion.pointTo(poses.depose_marron, 1.5)
    await propulsion.moveToRetry(poses.depose_marron, 0.5)

    # Depose avec les bras
    print('*********************')
    print('Depose avec les bras ')
    print('*********************')
    await actuators.arms_collect()
    await asyncio.sleep(0.2)

    # Pose construction
    print('*********************')
    print('Pose construction    ')
    print('*********************')
    await propulsion.moveToRetry(poses.pose_construction, 1.0)
    await propulsion.faceDirection(180, 1.5)


    #print('******************')
    #print('******************')
    #print(' STOOOOP!!!!      ')
    #print('******************')
    #print('******************')
    #return

    test = 0 # pour voir si on a pose la cerise

    # Construction gateau 1
    print('*********************')
    print('Construction gateau 1')
    print('*********************')
    await distrib_cerises.distrib_niveau1()
    if robot.side == pos.Side.Green:
        await actuators.construction_gateau_haut_vert()
    else:
        await actuators.construction_gateau_haut_bleu()
    await distrib_cerises.distrib_haut()
    await actuators.goldo_lifts_move(200, 80)
    await propulsion.moveToRetry(poses.pose_gateau_1, 1.0)
    #await actuators.arms_take()
    await actuators.arms_centering()
    
    if sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        test = 3
    elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        test = 2
    elif sensors['baumer_niveau1'] is True:
        test = 1

    await distrib_cerises.distrib_pose_cerise()
    cherry_in_dispenser = cherry_in_dispenser-1
    await asyncio.sleep(0.2)
    #await actuators.arms_open()
    await actuators.arms_collect()

    if sensors['baumer_niveau4'] is True and sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        await robot.setScore(robot.score + 10)
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print ("$ Score +10 pour 'baumer_niveau4..' (gateau1)")
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    elif sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        if test == 3:
            await robot.setScore(robot.score + 6)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +6 pour 'test == 3' (gateau1)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        else:
            await robot.setScore(robot.score + 7)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +7 pour 'test != 3' (gateau1)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        if test == 2:
            await robot.setScore(robot.score + 2)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +2 pour 'test == 2' (gateau1)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        else:
            await robot.setScore(robot.score + 4)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +4 pour 'test != 2' (gateau1)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    elif sensors['baumer_niveau1'] is True:
        await robot.setScore(robot.score + 1)
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print ("$ Score +1 pour 'baumer_niveau1..' (gateau1)")
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    test = 0

    # Construction gateau 2
    print('*********************')
    print('Construction gateau 2')
    print('*********************')
    await distrib_cerises.distrib_haut()
    await propulsion.moveToRetry(poses.pose_construction, 1.0)
    await propulsion.faceDirection(180, 1.5)
    await distrib_cerises.distrib_niveau1()
    if robot.side == pos.Side.Green:
        await actuators.construction_gateau_milieu_vert()
    else:
        await actuators.construction_gateau_milieu_bleu()
    await distrib_cerises.distrib_haut()
    await actuators.goldo_lifts_move(200, 80)
    await propulsion.moveToRetry(poses.pose_gateau_2, 1.0)
    #await actuators.arms_take()
    await actuators.arms_centering()

    if sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        test = 3
    elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        test = 2
    elif sensors['baumer_niveau1'] is True:
        test = 1
    
    await distrib_cerises.distrib_pose_cerise()
    cherry_in_dispenser = cherry_in_dispenser-1
    await asyncio.sleep(0.2)
    #await actuators.arms_open()
    await actuators.arms_collect()

    if sensors['baumer_niveau4'] is True and sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        await robot.setScore(robot.score + 10)
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print ("$ Score +10 pour 'baumer_niveau4..' (gateau2)")
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    elif sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        if test == 3:
            await robot.setScore(robot.score + 6)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +6 pour 'test == 3' (gateau2)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        else:
            await robot.setScore(robot.score + 7)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +7 pour 'test != 3' (gateau2)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        if test == 2:
            await robot.setScore(robot.score + 2)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +2 pour 'test == 2' (gateau2)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        else:
            await robot.setScore(robot.score + 4)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +4 pour 'test != 2' (gateau2)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    elif sensors['baumer_niveau1'] is True:
        await robot.setScore(robot.score + 1)
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print ("$ Score +1 pour 'baumer_niveau1..' (gateau2)")
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    test = 0

    # Construction gateau 3
    print('*********************')
    print('Construction gateau 3')
    print('*********************')
    await distrib_cerises.distrib_haut()
    await propulsion.moveToRetry(poses.pose_construction, 1.0)
    await propulsion.faceDirection(180, 1.5)
    await distrib_cerises.distrib_niveau1()
    if robot.side == pos.Side.Green:
        await actuators.construction_gateau_bas_vert()
    else:
        await actuators.construction_gateau_bas_bleu()
    await distrib_cerises.distrib_haut()
    await actuators.goldo_lifts_move(200, 80)
    await propulsion.moveToRetry(poses.pose_gateau_3, 1.0)
    #await actuators.arms_take()
    await actuators.arms_centering()

    if sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        test = 3
    elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        test = 2
    elif sensors['baumer_niveau1'] is True:
        test = 1
    
    await distrib_cerises.distrib_pose_cerise()
    cherry_in_dispenser = cherry_in_dispenser-1
    await asyncio.sleep(0.2)
    #await actuators.arms_open()
    await actuators.arms_collect()

    if sensors['baumer_niveau4'] is True and sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        await robot.setScore(robot.score + 10)
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print ("$ Score +10 pour 'baumer_niveau4..' (gateau3)")
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    elif sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        if test == 3:
            await robot.setScore(robot.score + 6)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +6 pour 'test == 3' (gateau3)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        else:
            await robot.setScore(robot.score + 7)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +7 pour 'test != 3' (gateau3)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        if test == 2:
            await robot.setScore(robot.score + 2)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +2 pour 'test == 2' (gateau3)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        else:
            await robot.setScore(robot.score + 4)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +4 pour 'test != 2' (gateau3)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    elif sensors['baumer_niveau1'] is True:
        await robot.setScore(robot.score + 1)
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print ("$ Score +1 pour 'baumer_niveau1..' (gateau3)")
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    test = 0
        
    # Recul
    print('******************')
    print('      Recul       ')
    print('******************')
    await propulsion.translation(-0.15, 1.0)
    await asyncio.sleep(0.2)


    #print('******************')
    #print('******************')
    #print(' STOOOOP!!!!      ')
    #print('******************')
    #print('******************')
    #return


    # Shoot
    await actuators.arms_close()
    await propulsion.pointTo(poses.tir_cerises, 5.0)
    await propulsion.moveToRetry(poses.tir_cerises, 1.0)
    await asyncio.sleep(0.2)
    await propulsion.faceDirection(90, 5.0)

    # FIXME : DEBUG
    await canon_cerises.canon_shoot()
    await propulsion.faceDirection(0, 5.0)
    await propulsion.translation(0.2, 1.0)
    cherry_score = 5 + cherry_in_gun
    await robot.setScore(robot.score + cherry_score)
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print ("$ Score +{} pour 'canon_cerises.canon_shoot()'".format(cherry_score))
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    #await actuators.arms_open()
    await actuators.arms_collect()

    print("MJR1 : " + str(assiette_1) + "," + str(jaune_1) + "," + str(rose_1))
    print("MJR2 : " + str(assiette_2) + "," + str(jaune_2) + "," + str(rose_2))
    print("five_secs_limit : " + str(five_secs_limit))

    # FIXME : DEBUG
    #assiette_1 = False
    # Prise marron
    await distrib_cerises.distrib_haut()
    if assiette_1 == True and five_secs_limit == False and (cherry_in_dispenser>0):
        print('******************')
        print('******************')
        print('    assiette_1    ')
        print('******************')
        print('******************')
        await propulsion.pointTo(poses.marron_assiette_1, 5.0)
        #taskarms = asyncio.create_task(actuators.arms_open())
        taskarms = asyncio.create_task(actuators.arms_collect())
        await propulsion.moveToRetry(poses.marron_assiette_1, 1.0)
        await taskarms
        await actuators.arms_centering()
        await propulsion.pointTo(poses.assiette_1, 5.0)
        await propulsion.moveToRetry(poses.assiette_1, 1.0)

        if sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            test = 3
        elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            test = 2
        elif sensors['baumer_niveau1'] is True:
            test = 1

        await distrib_cerises.distrib_pose_cerise()
        cherry_in_dispenser = cherry_in_dispenser-1
        #await actuators.arms_open()
        await actuators.arms_collect()

        if sensors['baumer_niveau4'] is True and sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            await robot.setScore(robot.score + 6)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +6 pour 'baumer_niveau4..' (assiette_1)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        elif sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            if test == 3:
                await robot.setScore(robot.score + 3)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +3 pour 'test == 3' (assiette_1)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            else:
                await robot.setScore(robot.score + 5)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +5 pour 'test != 3' (assiette_1)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            if test == 2:
                await robot.setScore(robot.score + 2)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +2 pour 'test == 2' (assiette_1)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            else:
                await robot.setScore(robot.score + 4)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +4 pour 'test != 2' (assiette_1)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        elif sensors['baumer_niveau1'] is True:
            await robot.setScore(robot.score + 1)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +1 pour 'baumer_niveau1..' (assiette_1)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        try:
            await propulsion.translation(-0.30, 0.5)
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print("Cannot retreat!!.. (assiette_1)")
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        test = 0

    # FIXME : DEBUG
    #jaune_1 = False
    await distrib_cerises.distrib_haut()
    if jaune_1 == True and five_secs_limit == False and (cherry_in_dispenser>0):
        print('******************')
        print('******************')
        print('     jaune_1      ')
        print('******************')
        print('******************')
        await propulsion.pointTo(poses.prise_j1, 5.0)
        await propulsion.moveToRetry(poses.prise_j1, 1.0)
        await actuators.arms_centering()
        await asyncio.sleep(0.2)
        try:
            await propulsion.translation(-0.30, 0.5)
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print("Cannot retreat!!.. (jaune_1)")
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        await propulsion.pointTo(poses.depose_j_1, 5.0)
        await propulsion.moveToRetry(poses.depose_j_1, 1.0)

        if sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            test = 3
        elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            test = 2
        elif sensors['baumer_niveau1'] is True:
            test = 1
        
        await distrib_cerises.distrib_pose_cerise()
        cherry_in_dispenser = cherry_in_dispenser-1
        #await actuators.arms_open()
        await actuators.arms_collect()

        if sensors['baumer_niveau4'] is True and sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            await robot.setScore(robot.score + 6)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +6 pour 'baumer_niveau4..' (jaune_1)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        elif sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            if test == 3:
                await robot.setScore(robot.score + 3)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +3 pour 'test == 3' (jaune_1)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            else:
                await robot.setScore(robot.score + 5)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +5 pour 'test != 3' (jaune_1)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            if test == 2:
                await robot.setScore(robot.score + 2)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +2 pour 'test == 2' (jaune_1)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            else:
                await robot.setScore(robot.score + 4)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +4 pour 'test != 2' (jaune_1)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        elif sensors['baumer_niveau1'] is True:
            await robot.setScore(robot.score + 1)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +1 pour 'baumer_niveau1..' (jaune_1)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        test = 0

        await propulsion.translation(-0.20, 1.0)
        if(robot.side == pos.Side.Blue):
            await propulsion.faceDirection(90, 5.0)
        else:
            await propulsion.faceDirection(-90, 5.0)
        await propulsion.translation(-0.20, 1.0)
        if rose_1 == False:
            if(robot.side == pos.Side.Blue):
                await propulsion.faceDirection(-90, 5.0)
            else:
                await propulsion.faceDirection(90, 5.0)
            await propulsion.translation(0.30, 1.0)


    #print('******************')
    #print('******************')
    #print(' STOOOOP!!!!      ')
    #print('******************')
    #print('******************')
    #return


    # FIXME : DEBUG
    #assiette_2 = False
    await distrib_cerises.distrib_haut()
    if assiette_2 == True and five_secs_limit == False and (cherry_in_dispenser>0):
        print('******************')
        print('******************')
        print('    assiette_2    ')
        print('******************')
        print('******************')
        await propulsion.pointTo(poses.marron_assiette_2, 5.0)
        #taskarms = asyncio.create_task(actuators.arms_open())
        taskarms = asyncio.create_task(actuators.arms_collect())
        await propulsion.moveToRetry(poses.marron_assiette_2, 1.0)
        await taskarms
        await actuators.arms_centering()
        await propulsion.pointTo(poses.assiette_2, 5.0)
        await propulsion.moveToRetry(poses.assiette_2, 1.0)

        if sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            test = 3
        elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            test = 2
        elif sensors['baumer_niveau1'] is True:
            test = 1

        await distrib_cerises.distrib_pose_cerise()
        cherry_in_dispenser = cherry_in_dispenser-1
        #await actuators.arms_open()
        await actuators.arms_collect()

        if sensors['baumer_niveau4'] is True and sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            await robot.setScore(robot.score + 6)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +6 pour 'baumer_niveau4..' (assiette_2)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        elif sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            if test == 3:
                await robot.setScore(robot.score + 3)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +3 pour 'test == 3' (assiette_2)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            else:
                await robot.setScore(robot.score + 5)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +5 pour 'test != 3' (assiette_2)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            if test == 2:
                await robot.setScore(robot.score + 2)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +2 pour 'test == 2' (assiette_2)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            else:
                await robot.setScore(robot.score + 4)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +4 pour 'test != 2' (assiette_2)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        elif sensors['baumer_niveau1'] is True:
            await robot.setScore(robot.score + 1)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +1 pour 'baumer_niveau1..' (assiette_2)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        test = 0

        await asyncio.sleep(0.2)
        await propulsion.translation(-0.15, 1.0)

    # FIXME : DEBUG
    #assiette_3 = False
    await distrib_cerises.distrib_haut()
    if assiette_3 == True and five_secs_limit == False and (cherry_in_dispenser>0):
        print('******************')
        print('******************')
        print('    assiette_3    ')
        print('******************')
        print('******************')
        await propulsion.pointTo(poses.marron_assiette_3, 5.0)
        #taskarms = asyncio.create_task(actuators.arms_open())
        taskarms = asyncio.create_task(actuators.arms_collect())
        await propulsion.moveToRetry(poses.marron_assiette_3, 1.0)
        await taskarms
        await actuators.arms_centering()
        await propulsion.pointTo(poses.assiette_3, 5.0)
        await propulsion.moveToRetry(poses.assiette_3, 1.0)

        if sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            test = 3
        elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            test = 2
        elif sensors['baumer_niveau1'] is True:
            test = 1

        await distrib_cerises.distrib_pose_cerise()
        cherry_in_dispenser = cherry_in_dispenser-1
        #await actuators.arms_open()
        await actuators.arms_collect()

        if sensors['baumer_niveau4'] is True and sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            await robot.setScore(robot.score + 6)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +6 pour 'baumer_niveau4..' (assiette_3)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        elif sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            if test == 3:
                await robot.setScore(robot.score + 3)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +3 pour 'test == 3' (assiette_3)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            else:
                await robot.setScore(robot.score + 5)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +5 pour 'test != 3' (assiette_3)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
            if test == 2:
                await robot.setScore(robot.score + 2)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +2 pour 'test == 2' (assiette_3)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            else:
                await robot.setScore(robot.score + 4)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print ("$ Score +4 pour 'test != 2' (assiette_3)")
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        elif sensors['baumer_niveau1'] is True:
            await robot.setScore(robot.score + 1)
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print ("$ Score +1 pour 'baumer_niveau1..' (assiette_3)")
            print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        test = 0

        await asyncio.sleep(0.2)
        await propulsion.translation(-0.15, 1.0)

    """    
    if jaune_2 and rose_2:
        await propulsion.pointTo(0.3, poses.rose_2[1], 5.0)
        await propulsion.pointTo(poses.jr_1[1], 5.0)
        await propulsion.moveToRetry(poses.jr_1[1], 1.0)
        await actuators.arms_centering()
        await asyncio.sleep(0.1)
        await distrib_cerises.distrib_lache()
        await actuators.arms_collect()
        await asyncio.sleep(0.1)
        await propulsion.translation(-0.3, 1.0)
        await actuators.arms_centering()
        await robot.setScore(robot.score + 10)
    """    

    check_areas_b = False

    # retour en zone
    await goto_final_pose()
    end_action.enabled = False

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

@robot.sequence
async def goto_final_pose():
    global in_zone
    print('******************')
    print('******************')
    print('  retour en zone  ')
    print('******************')
    print('******************')
    await propulsion.pointTo(poses.zone_presque_fin, 5.0)
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
        await propulsion.moveToRetry(poses.zone_fin, 0.2)
        in_zone = True
        await propulsion.faceDirection(0, 5.0)
    else:
        await propulsion.pointTo(poses.zone_fin_au_fond, 5.0)
        await propulsion.moveToRetry(poses.zone_fin_au_fond, 0.2)
        in_zone = True

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
    """
    if robot.side == pos.Side.Green:
        if lidar.objectInRectangle([2.60, 0.40], [2.999, 0.0]):
            if in_zone is True:
                robot.setScore(robot.score + 15)
    else:
        if lidar.objectInRectangle([2.60, -0.40], [2.999, 0.0]):
            if in_zone is True:
                robot.setScore(robot.score + 15)
    """
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


async def arms_safe():
    await actuators.arms_close()

@robot.sequence
async def init_test():
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,20,20)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setPose([0.1, 0.5], 0)

@robot.sequence
async def test_translation_pos():
    await propulsion.translation(0.50, 0.5)

@robot.sequence
async def test_translation_neg():
    await propulsion.translation(-0.50, 0.5)

@robot.sequence
async def test_move_to():
    await propulsion.moveTo((0.7,0.5), 0.5)

