import asyncio
from enum import Enum

# class syntax
class Slice(Enum):
    EMPTY = 1
    UNKNOWN = 2
    BROWN = 3
    YELLOW = 4
    PINK = 5


barillet = [[Slice.EMPTY, Slice.EMPTY, Slice.EMPTY], [Slice.EMPTY, Slice.EMPTY, Slice.EMPTY], [Slice.EMPTY, Slice.EMPTY, Slice.EMPTY]]

@robot.sequence
async def start_compressor_20():
    await pneumatic.start_compressor(20)

@robot.sequence
async def start_compressor():
    await pneumatic.start_compressor(30)

@robot.sequence
async def start_compressor_40():
    await pneumatic.start_compressor(36)
@robot.sequence
async def stop_compressor():
    await pneumatic.stop_compressor()

@robot.sequence
async def purge():
    await pneumatic.purge_compressor()
    await pneumatic.set_valves(0, 0, 0, 1)

@robot.sequence
async def test_valves():
    await pneumatic.set_valves(1, 1, 1, 1)
