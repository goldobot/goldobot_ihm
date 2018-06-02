import struct
import math

class PropulsionTelemetry:
    def __init__(self, data):
        unpacked = struct.unpack('<hhhhhhhHHbbBB', data)
        self.x = unpacked[0] * 0.25e-3
        self.y = unpacked[1] * 0.25e-3
        self.yaw = unpacked[2] * math.pi / 32767
        self.speed = unpacked[3] * 1e-3
        self.yaw_rate = unpacked[4] * 1e-3
        self.acceleration = unpacked[5] * 1e-3
        self.angular_acceleration = unpacked[6] * 1e-3
        self.left_encoder = unpacked[7]
        self.right_encoder = unpacked[8]
        self.left_pwm = unpacked[9] *1e-2
        self.right_pwm = unpacked[10] * 1e-2
        self.state = unpacked[11]
        self.error = unpacked[12]

class PropulsionTelemetryEx:
    def __init__(self, data):
        unpacked = struct.unpack('<hhhhhhhii', data[:22])
        self.target_x = unpacked[0] * 0.25e-3
        self.target_y = unpacked[1] * 0.25e-3
        self.target_yaw = unpacked[2] * math.pi / 32767
        self.target_speed = unpacked[3] * 1e-3
        self.target_yaw_rate = unpacked[4] * 1e-3
        self.longitudinal_error = unpacked[5] * 0.25e-3
        self.lateral_error = unpacked[6] * 0.25e-3
        self.left_encoder_acc = unpacked[7]
        self.right_encoder_acc = unpacked[8]


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
    def __init__(self, data=None):
        if data is not None:
            unpacked = struct.unpack('<fffffffff', data[:36])
            self.period = unpacked[0]
            self.kp = unpacked[1]
            self.kd = unpacked[2]
            self.ki = unpacked[3]
            self.feed_forward = unpacked[4]
            self.lim_iterm = unpacked[5]
            self.lim_dterm = unpacked[6]
            self.min_output = unpacked[7]
            self.max_output = unpacked[8]

    def serialize(self):
        return struct.pack('<fffffffff',
            self.period,
            self.kp,
            self.kd,
            self.ki,
            self.feed_forward,
            self.lim_iterm,
            self.lim_dterm,
            self.min_output,
            self.max_output
            )

class PropulsionControllerConfig:
    def __init__(self, data = None):
        if data is not None:
            self.speed_pid_config = PIDConfig(data[0:36])
            self.yaw_rate_pid_config = PIDConfig(data[36:72])
            self.translation_pid_config = PIDConfig(data[72:108])
            self.translation_cruise_pid_config = PIDConfig(data[108:144])
            self.yaw_pid_config = PIDConfig(data[144:180])
            unpacked = struct.unpack('<fffff', data[180:])
            self.lookahead_distance = unpacked[0]
            self.lookahead_time = unpacked[1]
            self.static_pwm_limit = unpacked[2]
            self.moving_pwm_limit = unpacked[3]
            self.repositioning_pwm_limit = unpacked[4]
    def serialize(self):
        dat = struct.pack('<fffff',
            self.lookahead_distance,
            self.lookahead_time,
            self.static_pwm_limit,
            self.moving_pwm_limit,
            self.repositioning_pwm_limit)
        return b''.join(
            [self.speed_pid_config.serialize(),
            self.yaw_rate_pid_config.serialize(),
            self.translation_pid_config.serialize(),
            self.translation_cruise_pid_config.serialize(),
            self.yaw_pid_config.serialize(),
            dat])


