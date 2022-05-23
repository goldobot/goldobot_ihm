import asyncio

class PinceRavisseuse(object):
    def __init__(self):
        self.mors_d_closed = 12
        self.mors_d_opened = 1023
        self.mors_g_closed = 4
        self.mors_g_opened = 1023

        self.chariot_g_mid = 512
        self.chariot_d_mid = 512
        self.chariot_g_closed = 0
        self.chariot_d_closed = 0

        self.lift_up = 3379

        #replica
        self.lift_wait_replica = 805
        self.mors_d_wait_replica = 761
        self.chariot_d_wait_replica = 371
        self.mors_g_wait_replica = 760
        self.chariot_g_wait_replica = 372

        self.lift_take_replica = 482
        self.mors_d_take_replica = 721
        self.chariot_d_take_replica = 340
        self.mors_g_take_replica = 722
        self.chariot_g_take_replica = 353

        self.mors_opened = {
            'mors_g': mors_g_opened,
            'mors_d': mors_d_opened
        }

        self.mors_closed = {
            'mors_g': mors_g_closed,
            'mors_d': mors_d_closed
        }

        self.chariot_opened = {
            'chariot_g': chariot_g_mid,
            'chariot_d': chariot_d_mid
        }

        self.chariot_closed = {
            'chariot_g': chariot_g_closed,
            'chariot_d': chariot_d_closed
        }


    @robot.sequence
    async def test_pince(self):
        await servos.setMaxTorque(['chariot_g', 'chariot_d', 'mors_g', 'mors_d'], 0.50)    
        await servos.setEnable(['chariot_g', 'chariot_d'], False)
        await servos.setEnable(['mors_g', 'mors_d'], True)
        await servos.moveMultiple(mors_opened, 0.8)
        await servos.setMaxTorque(['chariot_g', 'chariot_d', 'mors_g', 'mors_d'], 1.0)    
        await servos.moveMultiple(mors_closed, 1.0)
        await servos.setEnable(['chariot_g', 'chariot_d'], True)
        await servos.moveMultiple(chariot_opened, 1.0)
        await asyncio.sleep(0.3)
        await servos.moveMultiple(chariot_closed, 1.0)
        await asyncio.sleep(1)
        await servos.setEnable(['chariot_g', 'chariot_d', 'mors_g', 'mors_d'], False)

    @robot.sequence
    async def take_replica_right(self):
        await servos.setMaxTorque(['chariot_g', 'chariot_d', 'mors_g', 'mors_d', 'lift_pince'], 0.80)    
        await servos.setEnable(['chariot_g', 'chariot_d'], True)
        await servos.setEnable(['mors_g', 'mors_d','lift_pince'], True)

        await servos.moveMultiple({'lift_pince': self.lift_wait_replica}, 0.8)
        await servos.moveMultiple({'chariot_d': self.chariot_d_wait_replica}, 0.8)
        await servos.moveMultiple({'mors_d': self.mors_d_wait_replica}, 0.8)

        while sensors['sick_lat_d'] == True:
            await asyncio.sleep(0.1)
            
        await asyncio.sleep(5)
        await servos.moveMultiple({'lift_pince': self.lift_take_replica}, 0.8)
        await servos.moveMultiple({'chariot_d': self.chariot_d_take_replica}, 0.8)
        await servos.moveMultiple({'mors_d': self.mors_d_take_replica}, 0.8)

        await asyncio.sleep(1)

    @robot.sequence
    async def take_replica_left(self):
        await servos.setMaxTorque(['chariot_g', 'mors_g', 'lift_pince'], 0.80)    
        await servos.setEnable(['chariot_g'], True)
        await servos.setEnable(['mors_g', 'lift_pince'], True)

        await servos.moveMultiple({'lift_pince': self.lift_wait_replica}, 0.8)
        await servos.moveMultiple({'chariot_g': self.chariot_g_wait_replica}, 0.8)
        await servos.moveMultiple({'mors_g': self.mors_g_wait_replica}, 0.8)

        while sensors['sick_lat_g'] == True:
            await asyncio.sleep(0.1)
            
        await asyncio.sleep(5)
        await servos.moveMultiple({'lift_pince': self.lift_take_replica}, 0.8)
        await servos.moveMultiple({'chariot_g': self.chariot_d_take_replica}, 0.8)
        await servos.moveMultiple({'mors_g': self.mors_d_take_replica}, 0.8)

        await asyncio.sleep(1)