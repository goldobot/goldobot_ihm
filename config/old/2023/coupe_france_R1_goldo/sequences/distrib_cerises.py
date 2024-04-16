import asyncio
from time import sleep

distrib_pose_lock = 10400
distrib_pose_lache = 5000
distrib_pose_neutral = 9500

ascenseur_pose_neutral = 9500
ascenseur_pose_niveau1 = 7600
ascenseur_pose_niveau2 = 10000
ascenseur_pose_niveau3 = 12400
ascenseur_pose_haut = 12750

@robot.sequence
async def distrib_enable():
    await servos.setEnable(['distrib_cerises'], True)
    await servos.moveMultiple({'distrib_cerises': distrib_pose_neutral}, 1)
    await servos.setEnable(['ascenseur_cerises'], True)

@robot.sequence
async def distrib_neutral():
    await servos.moveMultiple({'distrib_cerises': distrib_pose_neutral}, 1)

@robot.sequence
async def distrib_lock():
    await servos.moveMultiple({'distrib_cerises': distrib_pose_lock}, 1)

@robot.sequence
async def distrib_lache():
    await servos.moveMultiple({'distrib_cerises': distrib_pose_lache}, 1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple({'distrib_cerises': distrib_pose_neutral}, 1)


@robot.sequence
async def distrib_niveau1():
    await servos.moveMultiple({'ascenseur_cerises': ascenseur_pose_niveau1}, 1)

@robot.sequence
async def distrib_niveau2():
    await servos.moveMultiple({'ascenseur_cerises': ascenseur_pose_niveau2}, 1)

@robot.sequence
async def distrib_niveau3():
    await servos.moveMultiple({'ascenseur_cerises': ascenseur_pose_niveau3}, 1)

@robot.sequence
async def distrib_haut():
    await servos.moveMultiple({'ascenseur_cerises': ascenseur_pose_haut}, 1)

@robot.sequence
async def distrib_pose_cerise():
    if(sensors['sick_niveau3'] is True):
        await distrib_niveau3()
    elif(sensors['sick_niveau2'] is True):
        await distrib_niveau2()
    elif(sensors['baumer_niveau1'] is True):
        await distrib_niveau1()
    else:
        return
    await asyncio.sleep(0.2)
    await distrib_lache()
    await asyncio.sleep(0.2)
    await distrib_haut()

@robot.sequence
async def get_layers():
    if sensors['sick_niveau4'] is False and sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        return 4
    elif sensors['sick_niveau3'] is True and sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        return 3
    elif sensors['sick_niveau2'] is True and sensors['baumer_niveau1'] is True:
        return 2
    elif sensors['baumer_niveau1'] is True:
        return 1
    else:
        return 0
