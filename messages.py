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
    def __init__(self, data = None, yaml = None):
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
        if yaml:
            self.dist_per_count_left = yaml['dist_per_count_left']
            self.dist_per_count_right = yaml['dist_per_count_right']
            self.wheel_spacing = yaml['wheels_spacing']
            self.update_period = yaml['update_period']
            self.speed_filter_period = yaml['speed_filter_period']
            self.encoder_period = yaml['encoder_period']

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
    def __init__(self, data=None, yaml=None):
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
        if yaml is not None:
            self.period = yaml['period']
            self.kp = yaml['kp']
            self.kd = yaml['ki']
            self.ki = yaml['kd']
            self.feed_forward = yaml['feed_forward']
            self.lim_iterm = yaml['lim_iterm']
            self.lim_dterm = yaml['lim_dterm']
            self.min_output = yaml['min_out']
            self.max_output = yaml['max_out']

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
    def __init__(self, data=None, yaml=None):
        if data is not None:
            self.speed_pid_config = PIDConfig(data[0:36])        
            self.translation_pid_config = PIDConfig(data[36:72])
            self.yaw_rate_pid_config = PIDConfig(data[72:108])
            self.yaw_pid_config = PIDConfig(data[108:144])
        if yaml is not None:
            self.speed_pid_config = PIDConfig(yaml = yaml['speed'])        
            self.translation_pid_config = PIDConfig(yaml = yaml['longi'])
            self.yaw_rate_pid_config = PIDConfig(yaml = yaml['yaw_rate'])
            self.yaw_pid_config = PIDConfig(yaml = yaml['yaw'])
        
    def serialize(self):
        return b''.join([
            self.speed_pid_config.serialize(),
            self.translation_pid_config.serialize(),
            self.yaw_rate_pid_config.serialize(),
            self.yaw_pid_config.serialize()
            ])
        
class PropulsionControllerConfig:
    def __init__(self, data = None, yaml = None):
        if data is not None:
            self.config_static = PropulsionControllerLowLevelConfig(data[0:144])
            self.config_cruise = PropulsionControllerLowLevelConfig(data[144:288])
            self.config_rotate = PropulsionControllerLowLevelConfig(data[288:432])
            
            unpacked = struct.unpack('<fffff', data[432:])
            self.lookahead_distance = unpacked[0]
            self.lookahead_time = unpacked[1]
            self.static_pwm_limit = unpacked[2]
            self.moving_pwm_limit = unpacked[3]
            self.repositioning_pwm_limit = unpacked[4]
        if yaml is not None:
            self.config_static = PropulsionControllerLowLevelConfig(yaml = yaml['pid_static'])
            self.config_cruise = PropulsionControllerLowLevelConfig(yaml = yaml['pid_static'])
            self.config_rotate = PropulsionControllerLowLevelConfig(yaml = yaml['pid_static'])
            self.lookahead_distance = yaml['lookahead_distance']
            self.lookahead_time = yaml['lookahead_time']
            self.static_pwm_limit = yaml['static_pwm_limit']
            self.moving_pwm_limit = yaml['moving_pwm_limit']
            self.repositioning_pwm_limit = yaml['reposition_pwm_limit']
            
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
            
class ServoConfig:
    def __init__(self, yaml):
        self.id = yaml['id']
        self.type = yaml['type']
