import asyncio
from time import sleep

distrib_pose_lock = 10400
distrib_pose_lache = 5000
distrib_pose_neutral = 9500

@robot.sequence
async def distrib_enable():
    await servos.setEnable(['distrib_cerises'], True)
    await servos.moveMultiple({'distrib_cerises': distrib_pose_neutral}, 1)

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
