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
        unpacked = struct.unpack('<hhhhhhhhhhii', data)
        self.target_x = unpacked[0] * 0.25e-3
        self.target_y = unpacked[1] * 0.25e-3
        self.target_yaw = unpacked[2] * math.pi / 32767
        self.target_speed = unpacked[3] * 1e-3
        self.target_yaw_rate = unpacked[4] * 1e-3
        self.longitudinal_error = unpacked[5] * 0.25e-3
        self.lateral_error = unpacked[6] * 0.25e-3
        self.left_encoder_acc = unpacked[10]
        self.right_encoder_acc = unpacked[11]

class RplidarRobotDetection:
    def __init__(self, data):
        unpacked = struct.unpack('<iihhhhhh', data)
        self.timestamp = unpacked[0]
        self.id = unpacked[1]
        self.x = unpacked[2] * 0.25e-3
        self.y = unpacked[3] * 0.25e-3
        self.vx = unpacked[4] * 1.0e-3
        self.vy = unpacked[5] * 1.0e-3
        self.ax = unpacked[6] * 1.0e-3
        self.ay = unpacked[7] * 1.0e-3


class OdometryConfig:
    def __init__(self, data = None):
        if data is not None:
            self.dist_per_count_left = data['dist_per_count_left']
            self.dist_per_count_right = data['dist_per_count_right']
            self.wheel_spacing = data['wheels_spacing']
            self.update_period = data['update_period']
            self.speed_filter_period = data['speed_filter_period']
            self.encoder_period = data['encoder_period']
        else:
            self.dist_per_count_left = 0
            self.dist_per_count_right = 0
            self.wheel_spacing = 1
            self.update_period = 1
            self.speed_filter_period = 1
            self.encoder_period = 0

    def serialize(self):
        return struct.pack('<fffffHH',
            self.dist_per_count_left,
            self.dist_per_count_right,
            self.wheel_spacing,
            self.update_period,
            self.speed_filter_period,
            int(self.encoder_period),
            0
            )

class PIDConfig:
    def __init__(self, data=None):
        if data is not None:
            #print (data)
            self.period = data['period']
            self.kp = data['kp']
            self.kd = data['kd']
            self.ki = data['ki']
            self.feed_forward = data['feed_forward']
            self.lim_iterm = data['lim_iterm']
            self.lim_dterm = data['lim_dterm']
            self.min_output = data['min_out']
            self.max_output = data['max_out']

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
class PropulsionControllerLowLevelConfig:
    def __init__(self, data=None):
        if data is not None:
            #print (data)
            self.speed_pid_config = PIDConfig(data['speed'])        
            self.translation_pid_config = PIDConfig(data['longi'])
            self.yaw_rate_pid_config = PIDConfig(data['yaw_rate'])
            self.yaw_pid_config = PIDConfig(data['yaw'])
        
    def serialize(self):
        return b''.join([
            self.speed_pid_config.serialize(),
            self.translation_pid_config.serialize(),
            self.yaw_rate_pid_config.serialize(),
            self.yaw_pid_config.serialize()
            ])
        
class PropulsionControllerConfig:
    def __init__(self, data = None):
        if data is not None:
            #print (data)
            self.config_static = PropulsionControllerLowLevelConfig(data['pid_static'])
            self.config_cruise = PropulsionControllerLowLevelConfig(data['pid_cruise'])
            self.config_rotate = PropulsionControllerLowLevelConfig(data['pid_rotate'])
            
            self.lookahead_distance = data['lookahead_distance']
            self.lookahead_time = data['lookahead_time']
            self.static_pwm_limit = data['static_pwm_limit']
            self.moving_pwm_limit = data['moving_pwm_limit']
            self.repositioning_pwm_limit = data['reposition_pwm_limit']
            
    def serialize(self):
        dat = struct.pack('<fffff',
            self.lookahead_distance,
            self.lookahead_time,
            self.static_pwm_limit,
            self.moving_pwm_limit,
            self.repositioning_pwm_limit)
        return b''.join(
            [self.config_static.serialize(),
            self.config_cruise.serialize(),
            self.config_rotate.serialize(),
            dat])


