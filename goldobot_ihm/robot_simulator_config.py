import struct

class RobotSimulatorConfig:
    def __init__(self, config_dict):
        self.speed_coeff = config_dict.get('speed_coeff', 0)
        self.wheels_spacing = config_dict.get('wheels_spacing', 0)
        self.encoders_spacing = config_dict.get('encoders_spacing', 0)
        self.encoders_counts_per_m = config_dict.get('encoders_counts_per_m', 0)
        self.encoders_period = config_dict.get('encoders_period', 0)

    def compile(self):
        return struct.pack('<ffffH',
            self.speed_coeff,
            self.wheels_spacing,
            self.encoders_spacing,
            self.encoders_counts_per_m,
            self.encoders_period)