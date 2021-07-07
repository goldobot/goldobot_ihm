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
fanion_ouvert = 10000

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
blue_start_pose = (0.8, -1.5 + robot_width * 0.5 + 5e-3, 0)
blue_flags = (2 - (robot_width * 0.5 + 5e-3), -1.5 + robot_width * 0.5 + 5e-3, -90)
blue_flags_2 = (blue_flags[0], -0.8, blue_flags[2])
blue_flags_3 = (1.2, -0.8, blue_flags[2])
blue_flags_4 = (1.1, -1.3, blue_flags[2])
blue_flags_5 = (0.8, -1.3, blue_flags[2])

class BluePoses(object):
    start_pose = (0.8, -1.5 + robot_width * 0.5 + 5e-3, 0)
    flags = (2 - (robot_width * 0.5 + 5e-3), -1.5 + robot_width * 0.5 + 5e-3, -90)
    flags_2 = (blue_flags[0], -0.8, flags[2])
    flags_3 = (1.2, -0.8, flags[2])
    flags_4 = (1.1, -1.3, flags[2])
    flags_5 = (0.8, -1.3, flags[2])
    
class YellowPoses(object):
    start_pose = symetrie(BluePoses.start_pose)
    flags = symetrie(BluePoses.flags)
    flags_2 = symetrie(BluePoses.flags_2)
    flags_3 = symetrie(BluePoses.flags_3)
    flags_4 = symetrie(BluePoses.flags_4)
    flags_5 = symetrie(BluePoses.flags_5)
    
async def homologation_blue():
    await propulsion.moveTo(poses.flags[0:2], 1)
    await propulsion.pointTo(poses.flags_2[0:2], 2)
    
    await servos.moveMultiple({'bras_lat_droite': bras_lat_droite_sorti})
    
    await propulsion.moveTo(poses.flags_2[0:2], 1)
    await servos.moveMultiple({'bras_lat_droite': bras_lat_droite_rentre})
    
    await propulsion.pointAndGo(poses.flags_3[0:2], 1, 2)
    
    await pales_ouvre()
    
    await propulsion.pointAndGo(poses.flags_4[0:2], 1, 2)
    await propulsion.pointAndGo(poses.flags_5[0:2], 1, 2)
    
async def homologation_yellow():
    await propulsion.moveTo(poses.flags[0:2], 1)
    await propulsion.pointTo(poses.flags_2[0:2], 2)
    
    await servos.moveMultiple({'bras_lat_gauche': bras_lat_gauche_sorti})
    
    await propulsion.moveTo(poses.flags_2[0:2], 1)
    await servos.moveMultiple({'bras_lat_gauche': bras_lat_gauche_rentre})
    
    await propulsion.pointAndGo(poses.flags_3[0:2], 1, 2)
    
    await pales_ouvre()
    
    await propulsion.pointAndGo(poses.flags_4[0:2], 1, 2)
    await propulsion.pointAndGo(poses.flags_5[0:2], 1, 2)

    
@robot.sequence
async def test1():
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
async def pales_ferme():
    pass
    
@robot.sequence
async def pales_ouvre():
    await servos.moveMultiple({'pale_g': 657, 'pale_d': 364})
    
@robot.sequence
async def prematch():
    global poses
    await lidar.start()
    
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
    
    await odrive.clearErrors()
    await propulsion.clearError()
    #await commands.motorsSetEnable(True)
    #await commands.propulsionSetEnable(True)
    #await commands.propulsionSetAccelerationLimits(1.0, 1.0, 1.0, 1.0) 
    

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
        await homologation_blue()
    if robot.side == Side.Yellow:
        await homologation_yellow()
    strategy.actions['action1'].enabled = True


async def end_match():
    await servos.move('fanion', fanion_ouvert)
    await sleep(2)
    await servos.move('fanion', fanion_ferme)
 
@robot.sequence
async def match():    
    await commands.scoreSet(15)
    
    if robot.side == Side.Blue:
        traj = pos_blue
        await commands.servoMove('bras_lat_droite', bras_lat_droite_sorti)
        for p in pos_blue:
            await commands.propulsionPointTo(p, 1)
            await commands.propulsionMoveTo(p, 0.6)
            
    if robot.side == Side.Yellow:
        traj = pos_yellow
        await commands.servoMove('bras_lat_gauche', bras_lat_gauche_sorti)
        for p in pos_yellow:
            await commands.propulsionPointTo(p, 1)
            await commands.propulsionMoveTo(p, 0.6)
    await commands.propulsionTranslation(-0.5,0.6)
    if robot.side == Side.Blue:
        for p in pos_blue2:
            await commands.propulsionPointTo(p, 1)
            await commands.propulsionMoveTo(p, 0.6)
    if robot.side == Side.Yellow:
        for p in pos_yellow2:
            await commands.propulsionPointTo(p, 1)
            await commands.propulsionMoveTo(p, 0.6)
    await sleep(5)

    return
    await commands.propulsionWaitForStop()
    await commands.waitForMatchTimer(5)
    await commands.servoMove('fanion', fanion_ouvert)
    await sleep(3)
    await commands.servoMove('fanion', fanion_ferme)
        
    


async def matcha():
    await sleep(20)
    await commands.scoreSet(10)
    robot.snapGirouette()
    if robot.girouette == 'n':
        await commands.scoreSet(50)
        
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
