from asyncio import sleep
import asyncio

import numpy as np
import math

from .herse import herse
from .pales import pales

class Side:
    Unknown = 0
    Blue = 1
    Yellow = 2

#values for 07 2021
robot_width = 0.255
robot_front_length =  0.1197
robot_back_length = 0.0837


bras_lat_gauche_sorti = 14500
bras_lat_gauche_rentre = 7300

bras_lat_droite_sorti = 4500
bras_lat_droite_rentre = 11500

fanion_ferme = 8000
fanion_ouvert = 11000

#
table_blue_port_green_x = 0.3
table_blue_port_green_x = 1.3


    
#actuators

#Pales exemple
#
#pales.move(gauche='ouvert', speed=0.5)
#pales.move(both='ferme', speed=0.1)



#herse
herse_haut = 2050
herse_bas_gobelet = 1000

#table:
#recifs bords x:1600
#recifs haut: y = +- 650

#port bas: 300mm du bord, y = +- 300

#zone depart: x [500, 1100] 400 en y
#zone n et s: 400 de part et d'autre depart
#zone d'exclusion port de 400 en y, attention, notre port est coté adverse et vice versa



def symetrie(pose):
    if isinstance(pose, np.ndarray):
        if pose.shape[0] == 2:
            return np.array([pose[0], -pose[1]])
    return (pose[0], -pose[1], -pose[2])

def on_segment(p1, p2, d):
    diff = p2 - p1
    midpoint = (p1 + p2) * 0.5
    diff = diff/np.linalg.norm(diff)
    nr = np.array([diff[1], -diff[0]])
    return midpoint + nr * d
    
#strategie homologation
#depart robot parallele au bord de latable
#avancée vers les fanions


class BluePoses(object):
    start_pose = (0.8, -1.5 + robot_width * 0.5 + 5e-3, 0)
    flags = (2 - (robot_width * 0.5 + 5e-3), -1.5 + robot_width * 0.5 + 5e-3, -90)
    flags_2 = (flags[0], -0.8, flags[2])
    flags_3 = (1.2, -0.8, flags[2])
    flags_4 = (1.1, -1.2, flags[2])
    flags_5 = (0.8, -1.3, flags[2])
    flags_5 = (0.8, -1.3, flags[2])
    zone_s = (1.2, -1.3, 90)
    zone_n = (0.4, -1.3, 90)

    p1 = (1.2, -0.8, 90)
    p2 = (0.4, -0.8, 90)

    phare = (0.15, -1.5 + 0.24, 90)
    
    hp_approche_phare = (0.4, -1, 180)
    hp_phare = (0.17, -1, 180)
    
    bouee_1 = np.array([0.51,-1.05])    
    bouee_2 = np.array([0.4,-1.2])
    bouee_3 = np.array([1.08,-1.05])
    bouee_4 = np.array([1.2,-1.2])
    
    pousse_bouees_1 = on_segment(bouee_1, bouee_2, -0.3)
    
    traj1 = [flags, flags_2, flags_3]
    
    servos_ma_bras_sorti = {'bras_lat_droite': bras_lat_droite_sorti}
    servos_ma_bras_rentre = {'bras_lat_droite': bras_lat_droite_rentre}

    servos_phare_bras_rentre = {'bras_lat_gauche': bras_lat_gauche_rentre}
    servos_phare_bras_sorti = {'bras_lat_gauche': 12000}
    servos_herse_phare = {'herse_slider': herse.h_droite}

class YellowPoses(object):
    start_pose = symetrie(BluePoses.start_pose)
    flags = symetrie(BluePoses.flags)
    flags_2 = symetrie(BluePoses.flags_2)
    flags_3 = symetrie(BluePoses.flags_3)
    flags_4 = symetrie(BluePoses.flags_4)
    flags_5 = symetrie(BluePoses.flags_5)
    zone_s = symetrie(BluePoses.zone_s)
    zone_n = symetrie(BluePoses.zone_n)

    p1 = symetrie(BluePoses.p1)
    p2 = symetrie(BluePoses.p2)

    phare = symetrie(BluePoses.phare)    
        
    hp_approche_phare = symetrie(BluePoses.hp_approche_phare)
    hp_phare = symetrie(BluePoses.hp_phare)

    servos_ma_bras_sorti = {'bras_lat_gauche': bras_lat_gauche_sorti}
    servos_ma_bras_rentre = {'bras_lat_gauche': bras_lat_gauche_rentre}

    servos_phare_bras_rentre = {'bras_lat_droite': bras_lat_droite_rentre}
    servos_phare_bras_sorti = {'bras_lat_droite': 6800 }
    servos_herse_phare = {'herse_slider': herse.h_gauche}
    #bras_lat_gauche_sorti = 14500
    #bras_lat_gauche_rentre = 7300

    #bras_lat_droite_sorti = 4500
    #bras_lat_droite_rentre = 11500

async def manches_a_air():
    speed = 0.7

    await propulsion.pointTo(poses.flags_2[0:2], 2)
    await servos.moveMultiple(poses.servos_ma_bras_sorti)
    await propulsion.moveTo(poses.flags_2[0:2], speed)
    await propulsion.pointTo(poses.flags_3[0:2], 2)
    await servos.moveMultiple(poses.servos_ma_bras_rentre)
    await robot.setScore(robot.score + 15)
    
async def moveToRetry(p, speed):
    await propulsion.moveToRetry(p, speed)
            
async def pointAndGoRetry(p, speed, yaw_rate):
    await propulsion.pointTo(p, yaw_rate)
    await moveToRetry(p, speed)
    
async def homologation_phare():
    #points phare
    await robot.setScore(2)
    speed = 0.7
    await propulsion.faceDirection(180, 2)
    await moveToRetry(poses.hp_approche_phare, speed)
    
    await declenchement_phare()
    
async def declenchement_phare():
    #depart a hp_approche_phare
    await propulsion.faceDirection(180, 0.5)
    
    await servos.moveMultiple({
            'herse_v': herse.v_depose})
    await servos.moveMultiple(poses.servos_herse_phare)
            
    await propulsion.moveTo(poses.hp_phare, 0.2)
    
    await robot.setScore(robot.score + 3)
    await robot.setScore(robot.score + 10)
    
    await propulsion.moveTo(poses.hp_approche_phare, 0.5)
    
    await servos.moveMultiple({
        'herse_slider': herse.h_centre})
    await servos.moveMultiple({
        'herse_v': herse.v_haut})
    
async def homologation():
    #points phare
    await robot.setScore(2)
    speed = 0.7
    await propulsion.pointTo(poses.flags, 2)
    await propulsion.moveToRetry(poses.flags[0:2], speed)
    await manches_a_air()

    await moveToRetry(poses.flags_3[0:2], speed)

    await pales_prise()

    girouette = await camera.captureGirouette()
    print('girouette', girouette)

    await propulsion.pointAndGo(poses.flags_4[0:2], 0.4, 2)

    #pousse les verres dans la zone de depart
    await pales_stockage()
    await propulsion.pointAndGo(poses.flags_5[0:2], speed, 2)
    await robot.setScore(robot.score + 2)

    #recule en laissant les verres
    await pales_droit()
    await propulsion.moveTo(poses.zone_s[0:2], speed)
    await pales_ferme()

    # va au phare
    await pointAndGoRetry(poses.p1[0:2], speed, 2)
    await pointAndGoRetry(poses.p2[0:2], speed, 2)
    
    #approche phare
    await pointAndGoRetry(poses.hp_approche_phare, speed, 2)

    # declenchement phare
    #await servos.moveMultiple(poses.servos_phare_bras_sorti)
    #await servos.moveMultiple(poses.servos_phare_bras_rentre)
    #await robot.setScore(robot.score + 3)
    #await robot.setScore(robot.score + 10)
    
    #declenchement nouveau phare
    await declenchement_phare()
    
    

    if girouette == 'south':
        await pointAndGoRetry(poses.p2[0:2], speed, 2)
        await pointAndGoRetry(poses.p1[0:2], speed, 2)
        await pointAndGoRetry(poses.zone_s[0:2], speed, 2)
        await robot.setScore(robot.score + 20)

    if girouette == 'north':
        await pointAndGoRetry(poses.p2[0:2], speed, 2)
        await pointAndGoRetry(poses.zone_n[0:2], speed, 2)
        await robot.setScore(robot.score + 20)

    if girouette == 'unknown':
        await pointAndGoRetry(poses.p2[0:2], speed, 2)
        await pointAndGoRetry(poses.zone_n[0:2], speed, 2)
        await robot.setScore(robot.score + 13)

@robot.sequence
async def test1():
    r = await camera.captureGirouette()
    print(r)
    return
    await robot.logMessage('I am in a sequence')
    await odrive.clearErrors()
    await propulsion.setAccelerationLimits(0.5,0.5,0.5,0.5)
    await propulsion.setPose([0,0], 0)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    await propulsion.setPose([0.5,0.1], 90)
    await propulsion.trajectorySpline([(0.5,0.1), (0.5,0.5), (1,0.5)], 0.5)
    return
    await propulsion.moveTo((1,0), 0.5)
    await propulsion.rotation(180, 0.5)
    await propulsion.moveTo((0.5,0), 0.5)
    await propulsion.pointTo((1,0), 0.5)
    await propulsion.faceDirection(90, 0.5)
    await propulsion.translation(0.1, 0.5)

    await propulsion.trajectorySpline([(0.5,0.1), (0.5,0.5), (1,0.5)], 0.5)

@robot.sequence
async def test_lifts():
    await servos.liftDoHoming(0)
    await servos.liftDoHoming(1)
    await sleep(1)
    await servos.liftSetEnable(0, True)
    await servos.setEnable('lift_left', True)
    
@robot.sequence
async def test_dynamixels():
    id_ = 8
    await commands.dynamixelsSetTorqueEnable(id_, True)
    await commands.dynamixelsSetSpeed(id_, 256)
    await commands.dynamixelsSetTorqueLimit(id_, 256)
    await commands.dynamixelsSetPosition(id_, 500)

@robot.sequence
async def test_servos():
    print('foo')
    #await servos.move('test_standard', 12000, 42)
    await servos.setEnable('pale_g', True)
    await servos.setEnable('pale_d', True)
    await servos.moveMultiple({'pale_g': 156, 'pale_d': 858})
    await servos.moveMultiple({'pale_g': 769, 'pale_d': 255})

@robot.sequence
async def test_herse():
    await herse.initialize()
    
@robot.sequence
async def test_recalage():
    #test recalage coin bleu
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.setAccelerationLimits(2,2,2,2)
    await propulsion.setPose([0.15, -1.35], 95)
    await propulsion.reposition(-0.1, 0.1)
    await propulsion.measureNormal(90, -1.5 + robot_back_length)
    await propulsion.translation(0.05, 0.5)
    await propulsion.faceDirection(0, 0.5)
    await propulsion.reposition(-0.1, 0.1)
    await propulsion.measureNormal(0, 0 + robot_back_length)
    await propulsion.translation(0.05, 0.5)
    
    
    
    
@robot.sequence
async def test_prises_herse():
    #await propulsion.translation(-0.05, 0.1)
    await pales_ferme()
    await propulsion.reposition(0.15, 0.1)
    await herse.prise()
    await pales_droit()
    await herse.depose()
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    await propulsion.clearError()
    await propulsion.translation(0.1, 0.1)
    await pales_stockage(0.5)


@robot.sequence
async def pales_ferme():
    await servos.moveMultiple({'pale_g': 156, 'pale_d': 858})
    
@robot.sequence
async def pales_stockage(speed=1):
    await servos.moveMultiple({'pale_g': 226, 'pale_d': 787}, speed)

@robot.sequence
async def pales_prise():
    await servos.moveMultiple({'pale_g': 567, 'pale_d': 461})
    
@robot.sequence
async def pales_ouvre():
    await servos.moveMultiple({'pale_g': 657, 'pale_d': 364})

@robot.sequence
async def pales_droit():
    await servos.moveMultiple({'pale_g': 409, 'pale_d': 614})

@robot.sequence
async def prematch():
    global poses
    await lidar.start()

    await robot.setScore(0)

    #servos
    await servos.setEnable('pale_g', True)
    await servos.setEnable('pale_d', True)
    await servos.moveMultiple({'pale_g': 156, 'pale_d': 858})

    await servos.setEnable('fanion', True)
    await servos.move('fanion', fanion_ferme)

    await servos.setEnable('bras_lat_gauche', True)
    await servos.move('bras_lat_gauche', bras_lat_gauche_rentre)

    await servos.setEnable('bras_lat_droite', True)
    await servos.move('bras_lat_droite', bras_lat_droite_rentre)

    await herse.initialize()

    await odrive.clearErrors()
    await propulsion.clearError()


    if robot.side == Side.Blue:
        poses = BluePoses
    if robot.side == Side.Yellow:
        poses = YellowPoses
    await propulsion.setPose(poses.start_pose[0:2], poses.start_pose[2])

    return True
    #robot._adversary_detection_enable = False

@robot.sequence
async def start_match():
    """
    Sequence called at the start of the match, before trying any action.
    This will typically be used to setup actuators and get out of the starting area.
    """
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    strategy.addTimerCallback(4, end_match)
    if robot.side == Side.Blue:
        await homologation()
    if robot.side == Side.Yellow:
        await homologation()
    strategy.actions['action1'].enabled = True

async def end_match():
    print('end match callback')
    await servos.move('fanion', fanion_ouvert)
    await sleep(2)
    await servos.move('fanion', fanion_ferme)
    await robot.setScore(robot.score + 10)

@robot.sequence
async def test_ferme_pavillon():
    await servos.setEnable('fanion', True)
    await servos.move('fanion', fanion_ferme)

@robot.sequence
async def test_ouvre_pavillon():
    await servos.setEnable('fanion', True)
    await servos.move('fanion', fanion_ouvert)
    await sleep(2)
    await servos.move('fanion', fanion_ferme)
@robot.sequence
async def test_enable_servos():
    await servos.setEnable('pale_g', True)
    await servos.setEnable('pale_d', True)
    await pales.move(gauche='ouvert', droite='droit')
    return
    print(robot.sensors['gache_g'])
    await herse.initialize()
    return
    #servos
    await servos.setEnable('pince_gauche', True)
    await servos.setEnable('pince_droite', True)
    await herse.pinces_attrape(gauche=True)
    return
    await servos.setEnable('pale_g', True)
    await servos.setEnable('pale_d', True)

    await servos.setEnable('fanion', True)

    await servos.setEnable('bras_lat_gauche', True)
    await servos.move('bras_lat_gauche', bras_lat_gauche_rentre)

    await servos.setEnable('bras_lat_droite', True)
    await servos.move('bras_lat_droite', bras_lat_droite_rentre)

    await herse.initialize()
    
@robot.sequence
async def test_emergency_stop():
    await propulsion.setAccelerationLimits(0.5,0.5,0.5,0.5)
    await propulsion.setPose([0,0], 0)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)

    await propulsion.reposition(0.2,0.1)

    task = asyncio.create_task(propulsion.translation(0.5, 0.1))
    await sleep(1)
    await propulsion.setTargetSpeed(0.3)
    await sleep(1)
    print('estop')
    await propulsion.emergencyStop()
    await task
