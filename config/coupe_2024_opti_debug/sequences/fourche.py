import asyncio
from enum import Enum

fourche_z_haut_var = 789
fourche_z_depose_haut_var = 1376
#fourche_z_depose_rank1_var = 1548
#fourche_z_depose_rank1_var = 1750
fourche_z_depose_rank1_var = 1840
fourche_z_depile_six_var = 1880
fourche_z_depose_six_var = 1850
fourche_z_depile_var = 1885
fourche_z_bas_var = 2494
fourche_z_depose_bas_var = 2450

fourche_pitch_incline_bas_var = 404
fourche_pitch_horizontal_var = 434
fourche_pitch_depile_six_var = 550
fourche_pitch_dessus_bordure_var = 558
fourche_pitch_depose_bas_var = 559
fourche_pitch_fill_rank1_var = 650
fourche_pitch_depose_haut_var = 701
fourche_pitch_transport_var = 715
fourche_pitch_fill_rank2_var = 720
fourche_pitch_vertical_var = 733

class SlotFourche(Enum):
    EMPTY = 0
    POT = 1
    PLANT = 2

class Fourche:
    slots = [SlotFourche.EMPTY for _ in range(10)]

    def __init__(self):
        self.slots = [SlotFourche.EMPTY for _ in range(10)]

    def reset(self):
        self.slots = [SlotFourche.EMPTY for _ in range(10)]

@robot.sequence
async def fourche_z_haut():
    await servos.setMaxTorque(['fourche_z'], 0.80)
    await servos.setEnable(['fourche_z'], True)
    await servos.moveMultiple({'fourche_z': fourche_z_haut_var}, 1)

@robot.sequence
async def fourche_z_bas():
    await servos.setMaxTorque(['fourche_z'], 0.80)
    await servos.setEnable(['fourche_z'], True)
    await servos.moveMultiple({'fourche_z': fourche_z_bas_var}, 1)

@robot.sequence
async def fourche_z_depose_bas():
    await servos.setMaxTorque(['fourche_z'], 0.80)
    await servos.setEnable(['fourche_z'], True)
    await servos.moveMultiple({'fourche_z': fourche_z_depose_bas_var}, 1)

@robot.sequence
async def fourche_z_depose_haut():
    await servos.setMaxTorque(['fourche_z'], 0.80)
    await servos.setEnable(['fourche_z'], True)
    await servos.moveMultiple({'fourche_z': fourche_z_depose_haut_var}, 1)

@robot.sequence
async def fourche_z_depose_rank1():
    await servos.setMaxTorque(['fourche_z'], 0.80)
    await servos.setEnable(['fourche_z'], True)
    await servos.moveMultiple({'fourche_z': fourche_z_depose_rank1_var}, 1)

@robot.sequence
async def fourche_z_depile_six():
    await servos.setMaxTorque(['fourche_z'], 0.80)
    await servos.setEnable(['fourche_z'], True)
    await servos.moveMultiple({'fourche_z': fourche_z_depile_six_var}, 1)

@robot.sequence
async def fourche_z_depose_six():
    await servos.setMaxTorque(['fourche_z'], 0.80)
    await servos.setEnable(['fourche_z'], True)
    await servos.moveMultiple({'fourche_z': fourche_z_depose_six_var}, 1)

@robot.sequence
async def fourche_depile():
    await servos.setMaxTorque(['fourche_z'], 0.80)
    await servos.setEnable(['fourche_z'], True)
    await servos.moveMultiple({'fourche_z': fourche_z_depile_var}, 1)

@robot.sequence
async def fourche_horizontale():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_horizontal_var}, 1)

@robot.sequence
async def fourche_horizontale_slow():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_horizontal_var}, 0.3)

@robot.sequence
async def fourche_verticale():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_vertical_var}, 1)

@robot.sequence
async def fourche_transport():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_transport_var}, 1)

@robot.sequence
async def fourche_pitch_dessus_bordure():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_dessus_bordure_var}, 1)

@robot.sequence
async def fourche_pitch_dessus_bordure_slow():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_dessus_bordure_var}, 0.3)

@robot.sequence
async def fourche_pitch_depile_six():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_depile_six_var}, 1)

@robot.sequence
async def fourche_pitch_fill_rank1():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_fill_rank1_var}, 1)

@robot.sequence
async def fourche_pitch_fill_rank1_slow():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_fill_rank1_var}, 0.3)

@robot.sequence
async def fourche_pitch_fill_rank2():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_fill_rank2_var}, 1)

@robot.sequence
async def fourche_depose():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_depose_haut_var, 'fourche_z': fourche_z_depose_haut_var}, 0.6)

