import struct

class RobotConfig:
    def __init__(self, config_dict):
        self.front_length = config_dict['geometry']['front_length']
        self.back_length = config_dict['geometry']['back_length']
        self.propulsion_interface = {'PWM_OUT': 0, 'ODRIVE_UART': 1}[config_dict['propulsion']['interface']]
        self.use_simulator = config_dict['propulsion']['use_simulator']
        

    def compile(self):
        buff = struct.pack('<ffBB',
            self.front_length,
            self.back_length,
            self.propulsion_interface, self.use_simulator)#todo add proper reading of option
        return buff
