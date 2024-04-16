import asyncio
from time import sleep

canon_pose_lock = 8200  # ou 8550 pour mieux bloquer
canon_pose_shoot = 11850
canon_pose_neutral = 9500

@robot.sequence
async def canon_enable():
    pass

@robot.sequence
async def canon_neutral():
    pass

@robot.sequence
async def canon_lock():
    pass

@robot.sequence
async def canon_shoot():
    pass

@robot.sequence
async def canon_initialize():
    pass

