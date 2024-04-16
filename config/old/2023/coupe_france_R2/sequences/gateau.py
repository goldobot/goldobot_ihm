import asyncio
from . import barillet
from . import pince

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
    # prise
    await barillet.barillet_niv1_gateau()
    await asyncio.sleep(1)
    if slot == 1:
        await barillet.valve1()
    elif slot == 3:
        await barillet.valve3()
    elif slot == 5:
        await barillet.valve5()
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
    await barillet.barillet_spin(cherry)
    await asyncio.sleep(0.3)
    await servos.setMaxTorque(['rotor'], 0.0)  
    await servos.setEnable(['rotor'], False)
    await barillet.barillet_niv3_cerise()
    await asyncio.sleep(0.4)
    await barillet.barillet_pose_haut()
    await asyncio.sleep(0.2)
    if sensors['sick_cerise_rotor'] is False:
        await barillet.barillet_niv3_cerise()
        await asyncio.sleep(0.4)
        await barillet.barillet_pose_haut()
    await servos.setMaxTorque(['rotor'], 1.0)
    await servos.setEnable(['rotor'], True)

@robot.sequence
async def cerise_4():
    await pose_cerise(4)

async def build_cake(brown, yellow, pink, cherry):
    await pince.pince_depose()
    await pince.chariot_close()
    await barillet.barillet_pose_haut()
    await barillet.barillet_spin(brown)
    await asyncio.sleep(0.2)
    await barillet.barillet_niv2_gateau()
    await asyncio.sleep(0.2)
    await barillet.pulse(brown)
    await asyncio.sleep(0.1)
    await barillet.barillet_pose_haut()
    await asyncio.sleep(0.1)
    await barillet.barillet_spin(yellow)
    await asyncio.sleep(0.2)
    await barillet.barillet_niv3_gateau()
    await asyncio.sleep(0.2)
    await barillet.pulse(yellow)
    await asyncio.sleep(0.1)
    await barillet.barillet_pose_haut()
    await asyncio.sleep(0.1)
    await barillet.barillet_spin(pink)
    await asyncio.sleep(0.2)
    await barillet.barillet_niv4_gateau()
    await asyncio.sleep(0.2)
    await barillet.pulse(pink)
    await asyncio.sleep(0.1)
    await barillet.barillet_pose_haut()
    await asyncio.sleep(0.1)
    await pince.recentre_cerise()
    await pince.chariot_close()
    await pose_cerise(cherry)
    await pince.pince_open()

@robot.sequence
async def build_last_cake():
    await pince.pince_depose()
    await barillet.barillet_pose_haut()
    await barillet.barillet_spin(1)
    await asyncio.sleep(0.1)
    await barillet.barillet_niv1_gateau()
    await asyncio.sleep(0.3)
    await pneumatic.set_valves(0, 1, 1, 0)
    await asyncio.sleep(0.4)
    await barillet.barillet_pose_haut()
    await barillet.barillet_spin(3)
    await asyncio.sleep(0.1)
    await barillet.barillet_niv2_gateau()
    await asyncio.sleep(0.2)
    await pneumatic.set_valves(0, 1, 0, 0)
    await asyncio.sleep(0.4)
    await barillet.barillet_pose_haut()
    await barillet.barillet_spin(5)
    await asyncio.sleep(0.3)
    await barillet.barillet_niv3_gateau()
    await asyncio.sleep(0.25)
    await pneumatic.set_valves(0, 0, 0, 0)
    await asyncio.sleep(0.4)
    await barillet.barillet_pose_haut()
    await pince.pince_take()
    await asyncio.sleep(0.1)
    await pince.pince_release()
    await asyncio.sleep(0.1)
    await pince.pince_take()
    await pince.chariot_close()
    await pose_cerise(6)
    await pince.pince_release()
    await pince.pince_open()

@robot.sequence
async def build_cake_test():
    await build_cake(1, 3, 5, 4)

@robot.sequence
async def build_cake_test2():
    await build_cake(1, 3, 5, 2)