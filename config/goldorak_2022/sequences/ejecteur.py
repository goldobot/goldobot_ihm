import asyncio

class Ejecteur(object):

    def __init__(self):
        self.ejecteur_neutral = 8000

    @robot.sequence
    async def ejecteur_initialize(self):
        await servos.setEnable(['ejecteur'], True)
        await servos.moveMultiple({'ejecteur': self.ejecteur_neutral}, 1)