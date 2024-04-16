import asyncio
from time import sleep

distrib_pose_lock = 10400
distrib_pose_lache = 5000
distrib_pose_neutral = 9500

@robot.sequence
async def distrib_enable():
    pass

@robot.sequence
async def distrib_neutral():
    pass

@robot.sequence
async def distrib_lock():
    pass

@robot.sequence
async def distrib_lache():
    pass
