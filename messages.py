import struct
import math

class PropulsionTelemetry:
    def __init__(self, data):
        unpacked = struct.unpack('<hhhhhHHbb', data)
        self.x = unpacked[0] * 0.25e-3
        self.y = unpacked[1] * 0.25e-3
        self.yaw = unpacked[2] * math.pi / 32767
        self.speed = unpacked[3] * 1e-3
        self.yaw_rate = unpacked[4] * 1e-3
        self.left_encoder = unpacked[5]
        self.right_encoder = unpacked[6]
        self.left_pwm = unpacked[7] *1e-2
        self.right_pwm = unpacked[8] * 1e-2

class OdometryConfig:
    def __init__(self, data = None):
        if data is not None:
            unpacked = struct.unpack('<fffffHH', data)
            self.dist_per_count_left = unpacked[0]
            self.dist_per_count_right = unpacked[1]
            self.wheel_spacing = unpacked[2]
            self.update_period = unpacked[3]
            self.speed_filter_period = unpacked[4]
            self.encoder_period = unpacked[5]
        else:
            self.dist_per_count_left = 0
            self.dist_per_count_right = 0
            self.wheel_spacing = 1
            self.update_period = 1
            self.speed_filter_period = 1
            self.encoder_period = 0

    def serialize(self):
        pass

class PIDConfig:
    def __init__(self, data):
        print(len(data))
        unpacked = struct.unpack('<fffffH', data[:22])