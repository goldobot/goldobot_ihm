import asyncio
from . import barillet
from . import pince
from . import utils

async def prend_gateau(slot):
    # Placement en haut pour permettre la rotation
    await barillet.barillet_pose_haut()
    # Choix du slot
    if slot == 1:
        await barillet.barillet_pose_1()
    elif slot == 3:
        await barillet.barillet_pose_3()
    elif slot == 5:
        await barillet.barillet_pose_5()
    else:
        return
    # Recentrage
    await pince.recentre_tempaxe()
    await asyncio.sleep(0.5)
    if await utils.get_cake_layers() < 3:
        await pince.pince_open()
        await asyncio.sleep(0.1)
        await propulsion.translation(0.02, 0.5)
        await pince.recentre_tempaxe()

    # prise
    await barillet.reduce_torque_ascenseur()
    await barillet.disable_torque_rotor()
    await barillet.barillet_niv1_gateau()
    await asyncio.sleep(1.5)
    if slot == 1:
        await barillet.valve1()
    elif slot == 3:
        await barillet.valve3()
    elif slot == 5:
        await barillet.valve5()
    await barillet.full_torque_ascenseur()
    await barillet.full_torque_rotor()
    # Placement en haut pour permettre la rotation
    await barillet.barillet_pose_haut()

@robot.sequence
async def prend_gateau1():
    await prend_gateau(1)

@robot.sequence
async def prend_gateau3():
    await prend_gateau(3)

@robot.sequence
async def prend_gateau5():
    await prend_gateau(5)

@robot.sequence
async def pose_cerise(cherry):
    height = 0
    # Choix cerise
    await barillet.barillet_spin(cherry)
    await asyncio.sleep(0.5)

    # Desactivation torque
    await servos.setMaxTorque(['rotor'], 0.0)
    await servos.setEnable(['rotor'], False)

    # Descente
    height = await utils.get_cake_layers()
    if height == 3:
        await barillet.barillet_niv3_cerise()
    elif height == 2:
        await barillet.barillet_niv2_cerise()
    elif height == 1:
        await barillet.barillet_niv1_cerise()
    else:
        await barillet.barillet_pose_haut()
        print("Wrong cake height")

    # Remontee
    await asyncio.sleep(0.3)
    await barillet.barillet_pose_haut()
    await asyncio.sleep(0.2)

    # Check cerise
    if await utils.get_cake_layers() != height + 1:
        if height == 3:
            await barillet.barillet_niv3_cerise()
        elif height == 2:
            await barillet.barillet_niv2_cerise()
        elif height == 1:
            await barillet.barillet_niv1_cerise()
        else:
            await barillet.barillet_pose_haut()
        await asyncio.sleep(0.3)
        await barillet.barillet_pose_haut()
        await asyncio.sleep(0.2)

    # Reactivation couple
    await servos.setMaxTorque(['rotor'], 1.0)
    await servos.setEnable(['rotor'], True)

@robot.sequence
async def cerise_2():
    await pince.recentre_cerise()
    await pince.chariot_close()
    await pose_cerise(2)

@robot.sequence
async def cerise_4():
    await pince.recentre_cerise()
    await pince.chariot_close()
    await pose_cerise(4)

@robot.sequence
async def cerise_6():
    await pince.recentre_cerise()
    await pince.chariot_close()
    await pose_cerise(6)

async def build_cake(brown, yellow, pink, cherry):
    await pince.pince_depose()
    await pince.chariot_close()
    await barillet.barillet_pose_haut()
    await barillet.barillet_spin(brown)
    await asyncio.sleep(0.2)
    await barillet.barillet_niv2_gateau()
    await asyncio.sleep(0.2)
    await barillet.valve(brown)
    await asyncio.sleep(0.08)
    await barillet.valve(brown)
    await asyncio.sleep(0.1)
    await barillet.barillet_pose_haut()
    await asyncio.sleep(0.3)
    await barillet.barillet_spin(yellow)
    await asyncio.sleep(0.2)
    await barillet.barillet_niv3_gateau()
    await asyncio.sleep(0.2)
    await barillet.valve(yellow)
    await asyncio.sleep(0.08)
    await barillet.valve(yellow)
    await asyncio.sleep(0.1)
    await barillet.barillet_pose_haut()
    await asyncio.sleep(0.3)
    await barillet.barillet_spin(pink)
    await asyncio.sleep(0.2)
    await barillet.barillet_niv4_gateau()
    await asyncio.sleep(0.2)
    await barillet.valve(pink)
    await asyncio.sleep(0.08)
    await barillet.valve(pink)
    await asyncio.sleep(0.1)
    await barillet.barillet_pose_haut()
    await asyncio.sleep(0.1)

@robot.sequence
async def build_cake_1():
    await pince.pince_depose()
    await pince.chariot_close()
    await barillet.barillet_pose_haut()
    await barillet.barillet_spin(1)
    await asyncio.sleep(0.2)
    await barillet.barillet_niv2_gateau()
    await asyncio.sleep(0.2)
    await barillet.valve1()
    await asyncio.sleep(0.15)
    await barillet.valve1()
    await asyncio.sleep(0.1)
    await barillet.barillet_pose_haut()
    await asyncio.sleep(0.3)
    await barillet.barillet_spin(3)
    await asyncio.sleep(0.2)
    await barillet.barillet_niv3_gateau()
    await asyncio.sleep(0.2)
    await barillet.valve3()
    await asyncio.sleep(0.15)
    await barillet.valve3()
    await asyncio.sleep(0.1)
    await barillet.barillet_pose_haut()
    await asyncio.sleep(0.3)
    await barillet.barillet_spin(5)
    await asyncio.sleep(0.2)
    await barillet.barillet_niv4_gateau()
    await asyncio.sleep(0.2)
    await barillet.valve5()
    await asyncio.sleep(0.15)
    await barillet.valve5()
    await asyncio.sleep(0.1)
    await barillet.barillet_pose_haut()
    await asyncio.sleep(0.1)


@robot.sequence
async def build_last_cake():
    await pince.pince_depose()
    await pince.chariot_close()
    await barillet.barillet_pose_haut()
    await barillet.barillet_spin(1)
    await asyncio.sleep(0.5)
    await pneumatic.set_valves(0, 1, 1, 0)
    await asyncio.sleep(0.2)
    await barillet.barillet_spin(3)
    await asyncio.sleep(0.5)
    await pneumatic.set_valves(0, 1, 0, 0)
    await asyncio.sleep(0.2)
    await barillet.barillet_spin(5)
    await asyncio.sleep(0.5)
    await pneumatic.set_valves(0, 0, 0, 0)
    await asyncio.sleep(0.2)

@robot.sequence
async def build_cake_test():
    await build_cake(1, 3, 5, 4)

@robot.sequence
async def build_cake_test2():
    await build_cake(1, 3, 5, 2)