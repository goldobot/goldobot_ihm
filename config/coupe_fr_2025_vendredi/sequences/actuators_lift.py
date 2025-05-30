@robot.sequence
async def lift_homing():
    await robot.fpgaRegWrite(0x80008500, 0x50000000)

@robot.sequence
async def lift_asserv_disable():
    await robot.fpgaRegWrite(0x80008500, 0x10000000)

@robot.sequence
async def lift_asserv_enable():
    await robot.fpgaRegWrite(0x80008500, 0x10000001)

@robot.sequence
async def lift_move(target_pos,speed,block_trig=0x80):
    new_val = 0x90000000 | (0x0fff0000 & (block_trig<<16)) | (0x0000ffff & speed)
    await robot.fpgaRegWrite(0x80008500, new_val)
    new_val = 0x70000000 | (0x0fffffff & target_pos)
    await robot.fpgaRegWrite(0x80008500, new_val)

@robot.sequence
async def lift_print_pos():
    lift_pos = await robot.fpgaRegRead(0x80008508)
    print ("lift_pos = {}".format(lift_pos))

