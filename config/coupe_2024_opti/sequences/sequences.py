# import base modules
import asyncio
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

carousel = Carousel()
fourche = Fourche()
start_zone = 0
start_side = Side.Unknown
poses = YellowPoses

@robot.sequence
async def print_sensors():
    print(sensors)

@robot.sequence
async def check_up_actionneurs():
    # Check turbines
    await test_turbines()
    await asyncio.sleep(2)

    # Check carrousel + ejecteurs
    await slot_cheminee_droite(get_slot_cheminee_droite+1)
    await eject_center()
    await eject_left()
    await eject_right()
    await asyncio.sleep(2)
    await eject_safe()
    await asyncio.sleep(2)
    await slot_cheminee_droite(get_slot_cheminee_droite-1)

    # Check portes
    await portes_test()
    await asyncio.sleep(1)

    # Check balayeurs
    await balayeur.test_balayeur()
    await asyncio.sleep(1)

    # Check tourne panneau
    await tourne_panneau.test()
    await asyncio.sleep(1)

@robot.sequence
async def demo_sponsors():
    await toboggan_ouvre()
    await carousel_demo_sponsors()
    await toboggan_rentre()

@robot.sequence
async def prematch():

    # Latch start parameters
    start_zone = robot.start_zone
    global poses
    start_side = robot.side
    if start_side == Side.Blue:
        poses = BluePoses
    elif start_side == Side.Yellow:
        poses = YellowPoses
    else:
        raise RuntimeError('Side not set')
    
    # Init score
    await robot.setScore(0)
    
    # Detection stop
    await lidar.stop()
    robot._adversary_detection_enable = False

    # Propulsion
    await odrive.clearErrors()
    await propulsion.clearError()
    await propulsion.setAccelerationLimits(1,1,20,20)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    await eject_safe()
    # Init turbines
    await init_turbines()

    # Init carousel
    carousel.reset()
    await init_carousel()

    # Init tourne panneau
    await tourne_panneau.tourne_panneau_in()

    # Init fourche and toboggan
    await toboggan_ouvre()
    await asyncio.sleep(1)
    await fourche_haut()
    await fourche_verticale()
    await asyncio.sleep(1)

    # Init balayeur
    await balayeur.balayeur_init()

    await test_turbines()

    # Init
    await recalage(start_zone)
    await toboggan_rentre()
    await propulsion.faceDirection(-90, 5.0)

    # Lidar start
    await lidar.start()

    await slot_to_chd(1)

    await robot.gpioSet('keyboard_led', True)
    return True


@robot.sequence
async def start_match():
    panneau_done = False
    T0 = time.time()
    robot._adversary_detection_enable = True

    my_rot_speed = 4.0
    my_lon_speed = 0.3
    my_lon_speed_prise = 0.3

    await propulsion.setAccelerationLimits(1,1,20,20)
    await tourne_panneau.tourne_panneau_out()
    await asyncio.sleep(0.5)
    await propulsion.moveToRetry(poses.pose_inter_panneaux, 0.4)
    await robot.setScore(robot.score + 15)

    if not lidar.objectInRectangle([2.0, -0.5], [1.5, 0.5]):
        await propulsion.moveToRetry(poses.pose_fin_panneaux, 0.4)
        await robot.setScore(robot.score + 15)
        panneau_done = True

        await tourne_panneau.tourne_panneau_in()

        await propulsion.pointTo(poses.pose_retour_panneaux, 5.0)
        await propulsion.moveToRetry(poses.pose_retour_panneaux, 1.0)
        await propulsion.pointTo(poses.pose_retour_panneaux2, 5.0)
        await propulsion.moveToRetry(poses.pose_retour_panneaux2, 0.6)
        await propulsion.moveToRetry(poses.pose_retour_panneaux3, 0.6)
        await robot.setScore(robot.score + 3)
    else:
        await tourne_panneau.tourne_panneau_in()
        await propulsion.pointTo(poses.pose_no_panneaux, 5.0)
        await propulsion.moveToRetry(poses.pose_no_panneaux, 1.0)
        

    await propulsion.moveToRetry(poses.debut_prise_1, 1.0)
    await propulsion.pointTo(poses.fin_prise_1, 5.0)

    await turbine_g_enable()
    await turbine_d_enable()

    await propulsion.moveToRetry(poses.inter_prise_1, my_lon_speed_prise)
    await turbine_g_suck()
    await turbine_d_suck()

    await asyncio.sleep(0.8)

    await turbine_g_enable()
    await turbine_d_enable()

    await slot_to_chd(2)
    
    await propulsion.moveToRetry(poses.inter2_prise_1, my_lon_speed_prise)
    await turbine_g_suck()
    await turbine_d_suck()

    await asyncio.sleep(0.8)

    await turbine_g_enable()
    await turbine_d_enable()

    await slot_to_chd(5)
    await propulsion.moveToRetry(poses.fin_prise_1, my_lon_speed_prise)
    await turbine_g_suck()
    await turbine_d_suck()
    await asyncio.sleep(0.8)
    await turbine_g_enable()
    await turbine_d_enable()

    await slot_to_chd(6)
    await propulsion.moveToRetry(poses.debut_prise_2, my_lon_speed_prise)
    await turbine_g_suck()
    await turbine_d_suck()
    await asyncio.sleep(0.8)
    await turbine_g_enable()
    await turbine_d_enable()

    try:
        await propulsion.translation()
    except:
        if robot.side == Side.Blue:
            await propulsion.faceDirection(90, 5.0)
        else:
            await propulsion.faceDirection(-90, 5.0)

    await slot_to_right(5)
    await slot_to_right(3)
    await slot_to_right(4)

    await propulsion.moveToRetry(poses.pose_inter_depose1, 1.2)
    if robot.side == Side.Blue:
        await propulsion.faceDirection(90, 5.0)
    else:
        await propulsion.faceDirection(-90, 5.0)

    await toboggan_ouvre()
    await fourche_bas()
    await fourche_horizontale()
    await asyncio.sleep(0.5)
    await propulsion.reposition(-0.1, my_lon_speed)
    await asyncio.sleep(0.2)
    await fourche_depose()
    await fourche_haut()
    await asyncio.sleep(0.5)
    await toboggan_depose()

    await propulsion.pointTo(poses.depose1, 5.0)
    await propulsion.moveToRetry(poses.depose1, 1.2)
    await propulsion.faceDirection(0, 5.0)
    await propulsion.reposition(-0.4, 0.3)

    await fourche_depose()
    await fourche_horizontale()
    await asyncio.sleep(0.5)
    await toboggan_depose()
    await asyncio.sleep(0.2)

    t1 = asyncio.create_task(eject_left())
    t2 = asyncio.create_task(eject_center())
    t3 = asyncio.create_task(eject_right())
    try:
        await t1
        await t2
        await t3
    except:
        print ("Exception: Overload ejecteur??")
    finally:
        await eject_safe()
    """
    await eject_center()
    await toboggan_depose2()
    t1 = asyncio.create_task(eject_left())
    t2 = asyncio.create_task(eject_center())
    t3 = asyncio.create_task(eject_right())
    try:
        await t1
        await t2
        await t3
    except:
        print ("Exception: Overload ejecteur??")
    """

    await toboggan_ouvre()
    await asyncio.sleep(0.5)

    await propulsion.translation(0.2, 0.4)
    await fourche_bas()
    await fourche_horizontale()
    await toboggan_rentre()

    await robot.setScore(robot.score + 14)

    await propulsion.pointTo(poses.depose2, 6.0)
    await propulsion.moveToRetry(poses.depose2, 1.0)
    await slot_to_right(10)
    await slot_to_right(2)
    await slot_to_right(1)
    if robot.side == Side.Blue:
        await propulsion.faceDirection(90, 6.0)
    else:
        await propulsion.faceDirection(-90, 6.0)

    await propulsion.reposition(-0.1, my_lon_speed)

    await toboggan_ouvre()
    await fourche_depose()
    await toboggan_depose()
    await asyncio.sleep(0.5)

    t1 = asyncio.create_task(eject_left())
    t2 = asyncio.create_task(eject_center())
    t3 = asyncio.create_task(eject_right())
    try:
        await t1
        await t2
        await t3
    except:
        print ("Exception: Overload ejecteur??")
    finally:
        await eject_safe()

    await asyncio.sleep(0.5)
    await toboggan_ouvre()
    await fourche_haut()
    await asyncio.sleep(0.5)
    await propulsion.reposition(-0.4, 0.4)

    await fourche_depose()
    await fourche_horizontale()
    
    await asyncio.sleep(0.5)
    await propulsion.translation(0.3, 1.0)
    await fourche_verticale()
    await fourche_haut()
    await asyncio.sleep(0.5)
    await toboggan_rentre()

    await robot.setScore(robot.score + 15)

    if panneau_done == False:
        await propulsion.pointTo(poses.pose_inter_panneaux, 5.0)
        await propulsion.moveToRetry(poses.pose_inter_panneaux, 1.2)
        await propulsion.faceDirection(-90, 5.0)
        await tourne_panneau.tourne_panneau_out()
        await propulsion.moveToRetry(poses.pose_fin_panneaux, 1.2)
        await tourne_panneau.tourne_panneau_in()

    await propulsion.pointTo(poses.depose_fin, 5.0)
    await propulsion.moveToRetry(poses.depose_fin, 1.2)
    await propulsion.faceDirection(0, 6.0)
    
    await robot.setScore(robot.score + 10)

    T1 = time.time()
    time_left = 90 - (T1 - T0)
    time_release = (time_left - 6) / 2
    await slot_to_chg(9)
    await turbine_g_stop()
    if time_release > 0:
        await asyncio.sleep(time_release)
    else:
        await asyncio.sleep(0)
    await slot_to_chd(10)
    await turbine_d_stop()
    if time_release > 0:
        await asyncio.sleep(time_release)
    else:
        await asyncio.sleep(0)
    await propulsion.reposition(-0.2, 0.6)

    await robot.setScore(robot.score + 1)

    # Detection stop
    await lidar.stop()

@robot.sequence
async def test_slot_chg1():
    await slot_to_chg(1)

@robot.sequence
async def test_slot_chg2():
    await slot_to_chg(2)

@robot.sequence
async def test_slot_chg5():
    await slot_to_chg(5)

@robot.sequence
async def test_slot_chd6():
    await slot_to_chd(6)

@robot.sequence
async def test_slot_center2():
    await slot_to_center(2)

@robot.sequence
async def test_slot_center4():
    await slot_to_center(4)

async def slot_to_chd(slot):
    exit_flag = False
    while(not exit_flag):
        try:
            print("try1 before")
            await slot_cheminee_droite(slot)
            print("try1 after")
            return
        except:
            exit_flag = False
        try:
            print("try2 before")
            await debloque_cheminees()
            await slot_cheminee_droite((slot -1)%10)
            await slot_cheminee_droite((slot +1)%10)
            await slot_cheminee_droite(slot)
            print("try2 after")
            return
        except:
            exit_flag = False
        try:
            print("try3 before")
            await asyncio.sleep(1)
            await slot_cheminee_droite((slot -1)%10)
            await slot_cheminee_droite((slot +1)%10)
            await slot_cheminee_droite(slot)
            print("try3 after")
            return
        except:
            print("Dammit I'm stuck !!!")
            return
        
async def slot_to_chg(slot):
    exit_flag = False
    while(not exit_flag):
        try:
            print("try1 before")
            await slot_cheminee_gauche(slot)
            print("try1 after")
            return
        except:
            exit_flag = False
        try:
            print("try2 before")
            await debloque_cheminees()
            await slot_cheminee_gauche((slot -1)%10)
            await slot_cheminee_gauche((slot +1)%10)
            await slot_cheminee_gauche(slot)
            print("try2 after")
            return
        except:
            exit_flag = False
        try:
            print("try3 before")
            await asyncio.sleep(1)
            await slot_cheminee_gauche((slot -1)%10)
            await slot_cheminee_gauche((slot +1)%10)
            await slot_cheminee_gauche(slot)
            print("try3 after")
            return
        except:
            print("Dammit I'm stuck !!!")
            return
        
async def slot_to_right(slot):
    exit_flag = False
    while(not exit_flag):
        try:
            print("try1 before")
            await slot_ejecteur_droit(slot)
            print("try1 after")
            return
        except:
            exit_flag = False
        try:
            print("try2 before")
            await slot_ejecteur_droit((slot -1)%10)
            await slot_ejecteur_droit((slot +1)%10)
            await slot_ejecteur_droit(slot)
            print("try2 after")
            return
        except:
            exit_flag = False
        try:
            print("try3 before")
            await asyncio.sleep(1)
            await slot_ejecteur_droit((slot -1)%10)
            await slot_ejecteur_droit((slot +1)%10)
            await slot_ejecteur_droit(slot)
            print("try3 after")
            return
        except:
            print("Dammit I'm stuck !!!")
            return

async def slot_to_center(slot):
    exit_flag = False
    while(not exit_flag):
        try:
            print("try1 before")
            await slot_ejecteur_centre(slot)
            print("try1 after")
            return
        except:
            exit_flag = False
        try:
            print("try2 before")
            await slot_ejecteur_centre((slot -1)%10)
            await slot_ejecteur_centre((slot +1)%10)
            await slot_ejecteur_centre(slot)
            print("try2 after")
            return
        except:
            exit_flag = False
        try:
            print("try3 before")
            await asyncio.sleep(1)
            await slot_ejecteur_centre((slot -1)%10)
            await slot_ejecteur_centre((slot +1)%10)
            await slot_ejecteur_centre(slot)
            print("try3 after")
            return
        except:
            print("Dammit I'm stuck !!!")
            return
        
@robot.sequence
async def check_plante_couchee():
    if sensors['bas_cheminee_droite'] == True:
        if sensors['milieu_cheminee_droite'] != True:
            await balayeur.push_right()
            await asyncio.sleep(0.1)
        if sensors['milieu_cheminee_droite'] != True:
            await balayeur.balayeur_d_degage()

    if sensors['bas_cheminee_gauche'] == False:
        if sensors['milieu_cheminee_gauche'] != False:
            await balayeur.push_left()
            await asyncio.sleep(0.1)
        if sensors['milieu_cheminee_gauche'] != False:
            await balayeur.balayeur_g_degage()
            
@robot.sequence
async def prise_auto():
    await turbine_d_enable()
    await turbine_g_enable()

    while True:
        carousel_full = True
        for slot in carousel.slots:
            if slot == Slot.EMPTY:
                carousel_full = False
        if carousel_full:
            return

        if sensors['bas_cheminee_droite'] == True:
            if sensors['milieu_cheminee_droite'] != True:
                await balayeur.push_right()
            if sensors['milieu_cheminee_droite'] != True:
                await balayeur.balayeur_d_degage()
            else:
                await turbine_d_suck()

        if sensors['bas_cheminee_gauche'] == False:
            if sensors['milieu_cheminee_gauche'] != False:
                await balayeur.push_left()
            if sensors['milieu_cheminee_gauche'] != False:
                await balayeur.balayeur_g_degage()
            else:
                await turbine_g_suck()

        if sensors['haut_cheminee_gauche'] == False and sensors['haut_cheminee_droite'] == False:
            return True
