from asyncio import sleep

class Side:
    Unknown = 0
    Blue = 1
    Yellow = 2

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

@robot.sequence
async def test1():
    print('I am in a sequence')
    await propulsion.setPose([0,0], 0)
    await propulsion.setMotorsEnable(True)
    await propulsion.setEnable(True)
    
    await propulsion.moveTo((1,0), 1)
    cmd = await propulsion.pointTo((1,1), 1)
    await propulsion.moveTo((1,1), 1)
    await cmd.begin
    #await propulsion.clearCommandQueue()
    #await propulsion.setMotorsEnable(False)
    await cmd.end
    
@robot.sequence
async def test_dynamixels():
    await commands.dynamixelsSetTorqueEnable(1, True)
    for i in range(4):
        await commands.dynamixelsSetSpeed(1, 256)
        await commands.dynamixelsSetPosition(1, 512)
        await sleep(1)
        await commands.dynamixelsSetSpeed(1, 1023)
        await commands.dynamixelsSetPosition(1, 200)
        await sleep(1)
    
@robot.sequence
async def _prematch():
    await commands.propulsionSetEnable(True)
    await commands.propulsionPointTo([1,2], 3)
    
@robot.sequence
async def prematch():
    await sleep(1)
    await commands.lidarStart()
    await commands.servoMove('bras_lat_gauche', bras_lat_gauche_rentre)
    await commands.servoMove('bras_lat_droite', bras_lat_droite_rentre)
    await commands.motorsSetEnable(True)
    await commands.propulsionSetEnable(False)
    await commands.propulsionSetEnable(True)
    await commands.propulsionSetAccelerationLimits(1.0, 1.0, 1.0, 1.0)    
    if robot.side == Side.Blue:
        await commands.propulsionSetPose(pos_depart_blue, 90)
    if robot.side == Side.Yellow:
        await commands.propulsionSetPose(pos_depart_yellow, -90)
    await sleep(2)
    await commands.servoMove('fanion', fanion_ferme)
    #robot._adversary_detection_enable = False
    
    
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
        
    
@robot.sequence
async def prematch3():
    print('start moves')
    await commands.propulsionSetEnable(False)
    await commands.propulsionSetEnable(True)
    await commands.motorsSetEnable(True)
    await commands.propulsionSetPose([0,0], 0)
    await commands.propulsionMoveTo([0.5, 0], 1)
    print(1)
    await commands.propulsionPointTo([1,1], 1)
    print(1)
    await commands.propulsionMoveTo([1, 1], 1)
    print(1)
    await commands.propulsionFaceDirection(-90, 1)
    print(1)
    await commands.propulsionTrajectory([[1,1], [1,0.5], [1.5,0]], 1)
    print(1)
    await commands.propulsionWaitForStop()
    print('end moves')
    await sleep(1)
    await commands.servoMove('bras_lat_gauche', 12000)
    
@robot.sequence
async def prematch2():
    print('prematch started, side: {}'.format(robot.side))
    await commands.lidarStart()
    print('start moves')
    await commands.propulsionSetEnable(True)
    await commands.propulsionSetPose([0,0], 0)
    await commands.propulsionTranslation(0.5, 1)
    
    await commands.propulsionRotation(90, 1)
    await commands.propulsionTranslation(0.5, 1)
    await commands.propulsionWaitForStop()
    print('end moves')
    await sleep(1)
    await commands.lidarStop()
    print('foo')
    await commands.servoMove('bras_lat_gauche', 12000)
    
@robot.sequence
async def matcha():
    await sleep(20)
    await commands.scoreSet(10)
    robot.snapGirouette()
    if robot.girouette == 'n':
        await commands.scoreSet(50)