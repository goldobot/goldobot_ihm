import asyncio
#values for 07 2021
robot_width = 0.255
robot_front_length =  0.1197
robot_back_length = 0.0837
robot_rotation_distance= 0.2
robot_rotation_distance_figurine = 0.25

@robot.sequence
async def init_field():
    await field.init()

@robot.sequence
async def start_field():
    await field.start()

@robot.sequence
async def stop_field():
    await field.stop()

@robot.sequence
async def test_remove_cakes():
    await field.remove_cake(3)
    await asyncio.sleep(3)
    await field.remove_cake(7)
    await asyncio.sleep(2)
    await field.remove_cake(4)

@robot.sequence
async def test_add_cakes():
    await field.add_cake(20, 0.06, 0.5, 4)
    await asyncio.sleep(3)
    await field.add_cake(21, 0.18, 0.5, 4)
    await asyncio.sleep(3)
    await field.add_cake(22, 0.30, 0.5, 4)

@robot.sequence
async def test_print_cakes():
    for cake in field._table_state.cakes:
        print("====")
        print("Cake " + str(cake.id) + " : ")
        print("( " + str(cake.pose.x) + " ; " + str(cake.pose.y) + " )")
        print("Color : " + str(cake.color))
        if cake.here is True:
            print("Here")
        else:
            print("Not here")
        print("====")


@robot.sequence
async def test_clear_cakes():
    await field.clear()
