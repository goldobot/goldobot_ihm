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
from .ecarteur import *
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
async def change_zone():
    global start_zone
    await propulsion.setAccelerationLimits(1,1,20,20)
    if start_zone == 1 or start_zone == 6:
        # trajectoire pour changer de zone
        await propulsion.pointTo(poses.traj_change_zone_coin, 5.0)
        await propulsion.moveToRetry(poses.traj_change_zone_coin, 0.8)
        await propulsion.pointTo(poses.traj_change_zone_milieu, 5.0)
        await propulsion.moveToRetry(poses.traj_change_zone_milieu, 0.8)
        await propulsion.pointTo(poses.traj_change_zone_bout, 5.0)
        await propulsion.moveToRetry(poses.traj_change_zone_bout, 0.8)
        await propulsion.pointTo(poses.traj_change_zone_milieu, 5.0)
        if start_zone == 1:
            await propulsion.pointTo(poses.zone6_start_pose, 5.0)
            await propulsion.moveToRetry(poses.zone6_start_pose, 0.8)
            await propulsion.faceDirection(180, 5.0)
            await recalage_zone_2()
            start_zone = 2
        else:
            await propulsion.pointTo(poses.zone1_start_pose, 5.0)
            await propulsion.moveToRetry(poses.zone1_start_pose, 0.8)
            await propulsion.faceDirection(180, 5.0)
            await recalage_zone_5()
            start_zone = 2

    elif start_zone == 5 or start_zone == 2:
        # trajectoire pour changer de zone
        await propulsion.pointTo(poses.traj_change_zone_milieu, 5.0)
        await propulsion.moveToRetry(poses.traj_change_zone_milieu, 0.8)
        await propulsion.pointTo(poses.traj_change_zone_coin, 5.0)
        await propulsion.moveToRetry(poses.traj_change_zone_coin, 0.8)
        if start_zone == 5:
            await propulsion.pointTo(poses.zone1_start_pose, 5.0)
            await propulsion.moveToRetry(poses.zone1_start_pose, 0.8)
            await propulsion.faceDirection(180, 5.0)
            await recalage_zone_1()
        else:
            await propulsion.pointTo(poses.zone6_start_pose, 5.0)
            await propulsion.moveToRetry(poses.zone6_start_pose, 0.8)
            await propulsion.faceDirection(180, 5.0)
            await recalage_zone_6()

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

    # Test ecarteur
    await ecarteur_autotest()

    # Check balayeurs
    await balayeur.test_balayeur()
    await asyncio.sleep(1)

    # Check tourne panneau
    await tourne_panneau.test()
    await asyncio.sleep(1)

@robot.sequence
async def prematch():

    # Latch start parameters
    global start_zone 
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
    await fourche_z_haut()
    await fourche_verticale()
    await asyncio.sleep(1)

    # Init balayeur
    await balayeur.balayeur_init()

    # Test ecarteur
    await ecarteur_autotest()

    # Init portes
    await asyncio.wait({porte_d_ouvre(), porte_g_ouvre()})

    await test_turbines()

    # Init
    await recalage(start_zone)
    await toboggan_rentre()

    # Lidar start
    # TODO : Re-enable lidar
    #await lidar.start()

    await slot_to_chg(1)

    await robot.gpioSet('keyboard_led', True)
    return True


@robot.sequence
async def start_match():
    panneau_done = False
    T0 = time.time()
    # TODO : Re enable detection
    robot._adversary_detection_enable = False

    await propulsion.setAccelerationLimits(1,1,20,20)
    await propulsion.moveToRetry(poses.debut_prise_1, 1.2)

    # Prend 12 plantes
    await prise_plantes_1()

    # Aligne les slots
    t1 = asyncio.create_task(slot_to_center(2))

    # Se dirige pour les pots
    await propulsion.pointTo(poses.pose_inter_depose1, 5.0)
    await propulsion.moveToRetry(poses.pose_inter_depose1, 0.8)
    if robot.side == Side.Blue:
        await propulsion.faceDirection(90, 2.0)
    else:
        await propulsion.faceDirection(-90, 2.0)

    # Prend 6 pots, les remplit, et les depose (recalage en Y au passage)
    await t1
    await chope_six_pots()
    await asyncio.sleep(0.1)
    if propulsion.pose.position.y < 0.0:
        await propulsion.setPose([propulsion.pose.position.x , -1.5 + rc.robot_back_length], 90)
    else:
        await propulsion.setPose([propulsion.pose.position.x , 1.5 - rc.robot_back_length], -90)

    await propulsion.setMotorsEnable(False)
    await propulsion.setEnable(False)
    await asyncio.sleep(0.1)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    await degage_depose_6_pots()
    await robot.setScore(robot.score + 30)

    # Monte les 2 plantes de devant
    t1 = asyncio.create_task(montee_en_roulant(1, 2))

    # Se dirige vers les autres pots
    await propulsion.pointTo(poses.prise_pots_2, 2.0)
    await propulsion.moveToRetry(poses.prise_pots_2, 1.0)
    await t1
    t1 = asyncio.create_task(slot_to_center(8))

    # Prend les pots
    if robot.side == Side.Blue:
        await propulsion.faceDirection(90, 5.0)
    else:
        await propulsion.faceDirection(-90, 5.0)

    await t1

    await chope_six_pots(1, False)

    # Va deposer en zone protegee
    await propulsion.pointTo(poses.depose_zone_protegee, 5.0)
    await propulsion.moveToRetry(poses.depose_zone_protegee, 1.0)
    await propulsion.faceDirection(0, 5.0)
    await depose_6_pots()
    #await propulsion.setPose([rc.robot_back_length , propulsion.pose.position.y], 0)
    await degage_depose_6_pots()

    await robot.setScore(robot.score + 20)
    

    # Va faire les panneaux solaires
    await propulsion.pointTo(poses.pose_depart_panneaux, 5.0)
    await propulsion.moveToRetry(poses.pose_depart_panneaux, 1.0)
    await propulsion.faceDirection(-90, 5.0)
    await tourne_panneau.tourne_panneau_out()
    await propulsion.moveToRetry(poses.pose_fin_panneaux, 0.8)
    await tourne_panneau.tourne_panneau_in()

    await robot.setScore(robot.score + 30)
    
    await propulsion.pointTo(poses.zone_fin, 5.0)
    await propulsion.moveToRetry(poses.zone_fin, 1.0)

    await robot.setScore(robot.score + 10)

    # Detection stop
    await lidar.stop()


# Fonction utilitaire pour call asynchrone dans la fonction suivante (prise_plantes_1)
async def prise_en_roulant_1():
    await slot_to_chd(5)
    while propulsion.pose.position.x > poses.fin_prise_1[0]:
        await asyncio.sleep(0.01)
    await asyncio.wait({turbine_d_suck(), balayeur.balayeur_g_hold(), porte_g_ferme()})
    await asyncio.sleep(0.5)
    await slot_to_chg(6)
    await asyncio.sleep(0.2)
    await asyncio.wait({porte_g_ouvre(),turbine_d_hold(), turbine_g_suck(), balayeur.balayeur_init()})
    await asyncio.sleep(0.5)
    await turbine_g_hold()
    await slot_to_chg(7)
    await asyncio.wait({turbine_g_hold(), turbine_d_hold()})
    return

# Sequence de prise de 12 plantes en partant de la zone a cote des panneaux solaires
# Part de la position debut_prise_1 = (1.7, +/-0.5, 180)
async def prise_plantes_1(my_speed_prise = 0.8, my_slow_speed_prise = 0.15):
    # demarre les turbines et s'oriente
    await asyncio.wait({turbine_g_hold(), turbine_d_hold()})
    await propulsion.pointTo(poses.fin_prise_1, 8.0)

    # avance et aspire
    await propulsion.moveToRetry(poses.inter_prise_1, my_speed_prise)
    await asyncio.wait({turbine_g_suck(), turbine_d_suck()})

    # attend la montee
    await asyncio.sleep(0.5)

    # ralentit les turbines
    await asyncio.wait({turbine_g_hold(), turbine_d_hold()})

    # 1 et 3 sont pleins, on se prepare a remplir 2 et 4
    await slot_to_chg(2)

    # avance et aspire
    await propulsion.moveToRetry(poses.inter2_prise_1, my_speed_prise)
    await asyncio.wait({turbine_g_suck(), turbine_d_suck()})

    # attend la montee
    await asyncio.sleep(0.5)

    # ralentit les turbines
    await asyncio.wait({turbine_g_hold(), turbine_d_hold()})

    # 2 et 4 sont pleins on remplit 5 et 6 en roulant
    t1 = asyncio.create_task(prise_en_roulant_1())
    await propulsion.moveToRetry(poses.debut_prise_2, my_slow_speed_prise)
    await t1

    # 5 et 6 sont pleins on remplit 7 et 9
    await turbine_g_suck()
    await turbine_d_suck()
    await asyncio.sleep(0.5)
    await turbine_g_hold()
    await turbine_d_hold()
    t1 = asyncio.create_task(slot_to_chg(8))

    # 7 et 9 sont pleins on remplit 8 et 10
    await propulsion.moveToRetry(poses.inter_prise_2, my_speed_prise)
    await t1
    await turbine_g_suck()
    await turbine_d_suck()
    await asyncio.sleep(0.5)
    await turbine_g_hold()
    await turbine_d_hold()

    # Carousel plein, on prend 2 plantes devant, pincees entre les balayeurs et les portes
    await propulsion.moveToRetry(poses.fin_prise_2, my_slow_speed_prise)
    await asyncio.wait({balayeur.balayeur_d_hold(), balayeur.balayeur_g_hold()})
    await asyncio.wait({porte_d_ferme(), porte_g_ferme()})

async def montee_en_roulant(slot_g, slot_d):
    # aligne le slot G
    await slot_to_chg(slot_g)

    # ouvre porte G
    await porte_g_ouvre()
    # aspire G
    await turbine_g_suck()
    await asyncio.sleep(0.5)
    await turbine_g_hold()

    # aligne le slot D
    await slot_to_chd(slot_d)

    # ouvre porte D
    await porte_d_ouvre()

    # aspire D
    await turbine_d_suck()
    await asyncio.sleep(0.5)
    await turbine_d_hold()

    # range balayeur
    await balayeur.balayeur_init()
    return

@robot.sequence
async def chope_six_pots(slot_2 = 5, depose = True):
    timeout_l = 0.2

    # 1) ouvrir toboggan
    await toboggan_ouvre()
    await asyncio.sleep(timeout_l)

    # 1') prepare ecarteur
    await ecarteur_pointy()
    await asyncio.sleep(timeout_l)

    # 2) fourche a l'horiz et a hauteur
    await asyncio.wait({fourche_horizontale(), fourche_z_depile_six()})
    await asyncio.sleep(timeout_l)

    # 4) recul
    await propulsion.reposition(-0.105, 0.3)
    await asyncio.sleep(timeout_l)

    # 4') active l'ecarteur
    t1 = asyncio.create_task(ecarteur_spread())

    # 5) fourche en position haute
    await fourche_z_haut()
    await asyncio.sleep(timeout_l)

    # 6) fourche pitch depile
    await fourche_pitch_depile_six_slow()
    await asyncio.sleep(timeout_l)

    await t1

    # 7) avance
    await propulsion.translation(0.18, 0.3)
    await asyncio.sleep(timeout_l)

    # 7') referme l'ecarteur
    t1 = asyncio.create_task(ecarteur_idle())

    # 8) fourche en position basse
    await fourche_z_depose_bas()
    await asyncio.sleep(timeout_l)

    await t1

    # 9) fourche a l'horiz..
    await fourche_horizontale()
    await asyncio.sleep(timeout_l)

    # 10) recul
    await propulsion.translation(-0.18, 0.3)
    await asyncio.sleep(timeout_l)

    # 11) fourche pitch fill rank2
    await fourche_pitch_fill_rank2()
    await asyncio.sleep(timeout_l)

    # 12) toboggan_deplacement
    await toboggan_deplacement()
    await asyncio.sleep(timeout_l)

    # 13) ejection de 3 plantes
    try:
        await asyncio.wait({eject_left(), eject_center(), eject_right()})
    except:
        print ("Exception: Overload ejecteur??")
    finally:
        await eject_safe()
    await asyncio.sleep(timeout_l)

    # 14) ouvrir toboggan
    await toboggan_ouvre()
    await asyncio.sleep(timeout_l)

    # 16) fourche a hauteur .. corecte et pitch fill rank1 (?)
    await asyncio.wait({fourche_z_depose_rank1(),fourche_pitch_fill_rank1_slow()})
    await asyncio.sleep(timeout_l)

    # 17) prepare les 3 plantes suivantes
    await slot_to_center(slot_2)

    # 18) fourche pitch dessus bordure
    await fourche_pitch_dessus_bordure_slow()
    await asyncio.sleep(timeout_l)

    # 20) fourche haut
    await fourche_z_haut()
    await asyncio.sleep(timeout_l)

    # 21) ejection de 3 dernieres plantes
    try:
        await asyncio.wait({eject_left(), eject_center(), eject_right()})
    except:
        print ("Exception: Overload ejecteur??")
    finally:
        await eject_safe()
    await asyncio.sleep(timeout_l)

    # 21) Depose ou mode deplacement
    if depose:
        await depose_6_pots()


async def depose_6_pots():
    timeout_l = 0.2
    # 1) Ouverture toboggan
    await toboggan_ouvre()

    # 2) fourche pitch dessus bordure
    await fourche_pitch_dessus_bordure_slow()
    await asyncio.sleep(timeout_l)

    # 3) fourche haut
    await fourche_z_haut()
    await asyncio.sleep(timeout_l)

    # 4) reposition pour depose
    await propulsion.reposition(-0.3, 0.3)
    await asyncio.sleep(timeout_l)

    # 5) fourche pitch horizontal
    await fourche_z_depose_six()
    await fourche_horizontale_slow()
    await asyncio.sleep(timeout_l)


async def degage_depose_6_pots():
    timeout_l = 0.2
    # 1) avance 16 cm
    await propulsion.translation(0.16, 0.3)
    await asyncio.sleep(timeout_l)

    # 1) range les actionneurs et s'en va..
    await fourche_verticale()
    await asyncio.sleep(timeout_l)
    await fourche_z_haut()
    await toboggan_rentre()
    await asyncio.sleep(timeout_l)
