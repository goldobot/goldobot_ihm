import asyncio
from asyncio import sleep

class Herse(object):
    def __init__(self):
        self.v_haut = 2050
        self.v_approche = 1500
        self.v_prise_approche = 1020
        self.v_prise = 950
        self.v_depose = 900
        self.v_rangement = 1800
        self.v_declenche_phare = 900

        self.h_gauche = 190
        self.h_droite = 790
        self.h_centre = 490
        self.h_centre_gauche = 500
        self.h_centre_droit = 440
        
        self.pg_positions = {
            'ouvert': 6800,
            'prise': 14200,
            'maintient': 14000
            }
            
        self.pd_positions = {
            'ouvert': 11000,
            'prise': 5200,
            'maintient': 5400
            }
            
        self.pd_ouvert = 11000
        self.pd_ferme = 5300
        
        self.pg_ouvert = 6800
        self.pg_ferme = 12000
        
    async def pinces(self, gauche=None, droite=None, both=None, speed=1):
        if both is not None:
            gauche = both
            droite = both        
        cmd = {}
        if gauche is not None:
            cmd['pince_gauche'] = self.pg_positions[gauche]
        if droite is not None:
            cmd['pince_droite'] = self.pd_positions[droite]
        if len(cmd) == 0:
            return        
        await servos.moveMultiple(cmd, speed)  
        
    async def pinces_attrape(self, gauche=False, droite=False):
        if gauche:
            pg = ['prise', 'maintient']
        else:
            pg = [None, None]            
        if droite:
            pd = ['prise', 'maintient']
        else:
            pd = [None, None]
        await self.pinces(pg[0], pd[0])
        await sleep(0.5)
        await self.pinces(pg[1], pd[1], speed=0.1)
        
        

    async def prise(self):
        await servos.moveMultiple({
            'herse_v': self.v_prise_approche})
        await servos.moveMultiple({
            'herse_v': self.v_prise,
            'pince_droite': self.pd_ferme,
            'pince_gauche': self.pg_ferme})
        await sleep(1)
            
        await servos.moveMultiple({
            'herse_v': self.v_approche})
        await servos.moveMultiple({
            'herse_slider': self.h_centre})
            
    async def depose(self):
        await servos.moveMultiple({
            'herse_v': self.v_depose})
        await servos.moveMultiple({
            'pince_droite': self.pd_ouvert,
            'pince_gauche': self.pg_ouvert})
        await servos.moveMultiple({
            'herse_v': self.v_rangement})
        
    async def initialize(self):
        await servos.setEnable('herse_v', True)
        await servos.setEnable('herse_slider', True)
        #await servos.setEnable('pince_droite', True)
        #await servos.setEnable('pince_gauche', True)
        await servos.moveMultiple({'herse_slider': self.h_centre})
        await sleep(1)
        await servos.moveMultiple({'herse_v': self.v_haut})
        #await self.pinces(both='ouvert')

        return
        await servos.moveMultiple({'herse_v': self.v_prise})
        await servos.moveMultiple({'herse_slider': self.h_gauche})




herse = Herse()