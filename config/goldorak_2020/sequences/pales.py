import asyncio
from asyncio import sleep

class Pales(object):
    def __init__(self):
        self.positions_g = {
            'ferme': 156,
            'stockage': 226,
            'prise': 567,
            'ouvert': 657,
            'droit': 409}
        self.positions_d = {
            'ferme': 858,
            'stockage': 787,
            'prise': 461,
            'ouvert': 364,
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