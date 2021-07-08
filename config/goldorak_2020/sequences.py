from asyncio import sleep
import asyncio

class Side:
    Unknown = 0
    Blue = 1
    Yellow = 2

#values for 07 2021
robot_width = 0.255
robot_front_length =  0.1197
robot_back_length = 0.0837

class BluePoses:
    start = (0.8, -1.5 + robot_width * 0.5 + 5e-3, 0)

bras_lat_gauche_sorti = 14500
bras_lat_gauche_rentre = 7300

bras_lat_droite_sorti = 4500
bras_lat_droite_rentre = 11500

fanion_ferme = 8000
fanion_ouvert = 11000

#actuators
class Herse(object):
    def __init__(self):
        self.v_haut = 2050
        self.v_approche = 1500
        self.v_prise = 1000
        self.v_rangement = 1800

        self.h_gauche = 190
        self.h_droite = 790
        self.h_centre = 490
        self.h_centre_gauche = 500
        self.h_centre_droit = 440

    async def initialize(self):
        await servos.setEnable('herse_v', True)
        await servos.setEnable('herse_slider', True)
        await servos.moveMultiple({'herse_slider': self.h_centre})
        await servos.moveMultiple({'herse_v': self.v_haut})

        return
        await servos.moveMultiple({'herse_v': self.v_prise})
        await servos.moveMultiple({'herse_slider': self.h_gauche})




herse = Herse()

#herse
herse_haut = 2050
herse_bas_gobelet = 1000

pos_depart_blue = [0.8, -1.4]
pos_blue = [[0.8, -0.7], [0.3, -0.7], [0.6, -1.2]]
pos_blue2 = [[1.5, -0.5], [1.0, -1.2]]

pos_depart_yellow = [0.8, 1.4]
pos_yellow = [[0.8, 0.7], [0.4, 0.7], [0.6, 1.2]]
pos_yellow2 = [[1.5, 0.5], [1.0, 1.2]]



def symetrie(pose):
    return (pose[0], -pose[1], -pose[2])


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

    servos_ma_bras_sorti = {'bras_lat_droite': bras_lat_droite_sorti}
    servos_ma_bras_rentre = {'bras_lat_droite': bras_lat_droite_rentre}

    servos_phare_bras_rentre = {'bras_lat_gauche': bras_lat_gauche_rentre}
    servos_phare_bras_sorti = {'bras_lat_gauche': 12000}

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

    servos_ma_bras_sorti = {'bras_lat_gauche': bras_lat_gauche_sorti}
    servos_ma_bras_rentre = {'bras_lat_gauche': bras_lat_gauche_rentre}

    servos_phare_bras_rentre = {'bras_lat_droite': bras_lat_droite_rentre}
    servos_phare_bras_sorti = {'bras_lat_droite': 6800 }
    
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
    cp = propulsion.pose
    cp = (cp.position.x, cp.position.y)
    while True:
        try:
            await propulsion.moveTo(p, speed)
            return
        except exceptions.PropulsionError as e:
            await propulsion.clearError()
            await propulsion.moveTo(cp, speed * 0.5)
            await sleep(2)
            
        

async def homologation():
    #points phare
    await robot.setScore(2)
    speed = 0.7
    await propulsion.moveTo(poses.flags[0:2], speed)
    await manches_a_air()

    await moveToRetry(poses.flags_3[0:2], speed)

    await pales_ouvre()

    girouette = await camera.captureGirouette()
    print('girouette', girouette)

    await propulsion.pointAndGo(poses.flags_4[0:2], speed, 2)

    #pousse les verres dans la zone de depart
    await pales_ferme()
    await propulsion.pointAndGo(poses.flags_5[0:2], speed, 2)
    await robot.setScore(robot.score + 2)

    #recule en laissant les verres
    await pales_droit()
    await propulsion.moveTo(poses.zone_s[0:2], speed)
    await pales_ferme()

    # va au phare
    await propulsion.pointAndGo(poses.p1[0:2], speed, 2)
    await propulsion.pointAndGo(poses.p2[0:2], speed, 2)
    await propulsion.pointAndGo(poses.phare[0:2], speed, 2)

    await propulsion.faceDirection(poses.phare[2], 2)

    # declenchement phare
    await servos.moveMultiple(poses.servos_phare_bras_sorti)
    await servos.moveMultiple(poses.servos_phare_bras_rentre)
    await robot.setScore(robot.score + 3)
    await robot.setScore(robot.score + 10)


    if girouette == 'south':
        await propulsion.pointAndGo(poses.p2[0:2], speed, 2)
        await propulsion.pointAndGo(poses.p1[0:2], speed, 2)
        await propulsion.pointAndGo(poses.zone_s[0:2], speed, 2)
        await robot.setScore(robot.score + 20)

    if girouette == 'north':
        await propulsion.pointAndGo(poses.p2[0:2], speed, 2)
        await propulsion.pointAndGo(poses.zone_n[0:2], speed, 2)
        await robot.setScore(robot.score + 20)

    if girouette == 'unknown':
        await propulsion.pointAndGo(poses.p2[0:2], speed, 2)
        await propulsion.pointAndGo(poses.zone_n[0:2], speed, 2)
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
async def pales_ferme():
    await servos.moveMultiple({'pale_g': 156, 'pale_d': 858})

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
