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
    t=int(target_pos)
    s=int(speed)
    blt=int(block_trig)
    print ("t={}, s={}, blt={}".format(t,s,blt))
    new_val = 0x90000000 | (0x0fff0000 & (blt<<16)) | (0x0000ffff & s)
    await robot.fpgaRegWrite(0x80008500, new_val)
    await robot.fpgaRegWrite(0x80008500, new_val)
    new_val = 0x70000000 | (0x0fffffff & t)
    await robot.fpgaRegWrite(0x80008500, new_val)
    await robot.fpgaRegWrite(0x80008500, new_val)

#@robot.sequence
#async def lift_move2(*args):
#    target_pos=int(args[0],16)
#    speed=int(args[1],16)
#    print ("target={], speed={}".format(target_pos,speed))
#    #new_val = 0x90800000 | (0x0000ffff & speed)
#    #await robot.fpgaRegWrite(0x80008500, new_val)
#    #new_val = 0x70000000 | (0x0fffffff & target_pos)
#    #await robot.fpgaRegWrite(0x80008500, new_val)

@robot.sequence
async def lift_print_pos():
    lift_pos = await robot.fpgaRegRead(0x80008508)
    print ("DEBUG : lift_pos = {}".format(lift_pos))

@robot.sequence
async def lift_move2(*args):
    #print ("DEBUG : LIFT TEST")
    #for arg in args:
    #    print ("{}".format(arg))
    target=int(args[0],16)
    speed=int(args[1],16)
    print ("target={}, speed={}".format(target,speed))
    new_val = 0x90800000 | (0x0000ffff & speed)
    print ("new_val={:x}".format(new_val))
    await robot.fpgaRegWrite(0x80008500, new_val)
    new_val = 0x70000000 | (0x0fffffff & target)
    print ("new_val={:x}".format(new_val))
    await robot.fpgaRegWrite(0x80008500, new_val)
