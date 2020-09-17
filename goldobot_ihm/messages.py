import struct


class HalGpioSet:
    def __init__(self, gpio_id, value):
        self.gpio_id = gpio_id
        self.value = value
        
    def serialize(self):
        return struct.pack('<BB', self.gpio_id, self.value)
        
class HalSetPwm:
    def __init__(self):
        self.pwm_id = 0
        self.value = 0
        
    def serialize(self):
        return struct.pack('<Bf', self.gpio_id, self.value)