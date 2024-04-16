import asyncio
from time import sleep

canon_pose_lock = 8800  # ou 8550 pour mieux bloquer
canon_pose_shoot = 11800
canon_pose_neutral = 9500

@robot.sequence
async def canon_enable():
    await servos.setEnable(['canon_cerises'], True)
    await servos.moveMultiple({'canon_cerises': canon_pose_neutral}, 1)

@robot.sequence
async def canon_neutral():
    await servos.moveMultiple({'canon_cerises': canon_pose_neutral}, 1)

@robot.sequence
async def canon_lock():
    await servos.moveMultiple({'canon_cerises': canon_pose_lock}, 1)

@robot.sequence
async def canon_shoot():
    await servos.moveMultiple({'canon_cerises': canon_pose_shoot}, 1)
    await asyncio.sleep(0.1)
    await servos.moveMultiple({'canon_cerises': canon_pose_neutral}, 1)

@robot.sequence
async def canon_initialize():
    await canon_enable()
    while sensors['switch_canon'] is False:
        await asyncio.sleep(0.02)
    await asyncio.sleep(3)
    await servos.moveMultiple({'canon_cerises': canon_pose_lock}, 1)
