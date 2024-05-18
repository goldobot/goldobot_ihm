import asyncio
from enum import Enum

fourche_z_haut = 789
fourche_z_bas = 2494
fourche_z_depose_bas = 2452
fourche_z_depose_haut = 1376
fourche_z_depile = 1885
fourche_z_depose = 1548

fourche_pitch_horizontal = 434
fourche_pitch_vertical = 733
fourche_pitch_transport = 715
fourche_pitch_dessus_bordure = 558
fourche_pitch_depose_bas = 559
# FIXME : DEBUG : GOLDO
#fourche_pitch_depose_haut = 701
fourche_pitch_depose_haut = 550
fourche_pitch_incline_bas = 404

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
async def fourche_haut():
    await servos.setMaxTorque(['fourche_z'], 0.80)
    await servos.setEnable(['fourche_z'], True)
    await servos.moveMultiple({'fourche_z': fourche_z_haut}, 1)

@robot.sequence
async def fourche_bas():
    await servos.setMaxTorque(['fourche_z'], 0.80)
    await servos.setEnable(['fourche_z'], True)
    await servos.moveMultiple({'fourche_z': fourche_z_bas}, 1)

@robot.sequence
async def fourche_depose():
    await servos.setMaxTorque(['fourche_z'], 0.80)
    await servos.setEnable(['fourche_z'], True)
    await servos.moveMultiple({'fourche_z': fourche_z_depose}, 1)

@robot.sequence
async def fourche_depile():
    await servos.setMaxTorque(['fourche_z'], 0.80)
    await servos.setEnable(['fourche_z'], True)
    await servos.moveMultiple({'fourche_z': fourche_z_depile}, 1)

@robot.sequence
async def fourche_horizontale():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_horizontal}, 1)

@robot.sequence
async def fourche_verticale():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_vertical}, 1)

@robot.sequence
async def fourche_transport():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_transport}, 1)

@robot.sequence
async def fourche_bordure():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_bordure}, 1)

@robot.sequence
async def fourche_depose():
    await servos.setMaxTorque(['fourche_pitch'], 0.80)
    await servos.setEnable(['fourche_pitch'], True)
    await servos.moveMultiple({'fourche_pitch': fourche_pitch_depose_haut, 'fourche_z': fourche_z_depose_haut}, 0.6)

