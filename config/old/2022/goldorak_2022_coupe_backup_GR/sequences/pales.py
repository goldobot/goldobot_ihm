import asyncio
from asyncio import sleep

class Pales(object):
    def __init__(self):
        self.positions_g = {
            'ferme': 156,
            'stockage': 226,
            'prise': 567,
            'ouvert': 657,
            'deflecteur': 480,
            'droit': 409}
        self.positions_d = {
            'ferme': 858,
            'stockage': 787,
            'prise': 461,
            'ouvert': 364,
            'deflecteur': 540,
            'droit': 614}

    async def move(self, *,gauche=None, droite=None, both=None, speed=1):
        cmd = {}
        if both is not None:
            gauche = both
            droite = both
        if gauche is not None:
            cmd['pale_g'] = self.positions_g[gauche]
        if droite is not None:
            cmd['pale_d'] = self.positions_d[droite]
        if len(cmd) == 0:
            return
        await servos.moveMultiple(cmd, speed)            

pales = Pales()

@robot.sequence
async def pales_ferme():
    await pales.move(both='ferme')
    
@robot.sequence
async def pales_stockage(speed=1):
    await pales.move(both='stockage')

@robot.sequence
async def pales_stockage_soft(speed=0.5):
    await pales.move(both='stockage', speed=speed)

@robot.sequence
async def pales_prise():
    await pales.move(both='prise')

@robot.sequence
async def pales_ouvre():
    await pales.move(both='ouvert')

@robot.sequence
async def pales_droit():
    await pales.move(both='droit')
    
@robot.sequence
async def pales_deflecteur():
    await pales.move(both='deflecteur')
    