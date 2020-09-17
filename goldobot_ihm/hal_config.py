import struct

gpio_port_nums = {
   'PA': 0,
   'PB': 1,
   'PC': 2,
   'PD': 3,
   'PE': 4,
   'PF': 5
   }
   
periph_names = [
    'GPIO',
    'TIM1',
	'TIM2',
	'TIM3',
	'TIM4',
	'TIM6',
	'TIM7',
	'TIM8',
	'TIM15',
	'TIM16',
	'TIM17',
    'TIM20',
	'CAN',
	'I2C1',
	'I2C2',
	'I2C3',
	'SPI1',
	'SPI2',
	'SPI3',
	'USART1',
	'USART2',
	'USART3',
	'UART4',
	'UART5'
    ]
    
periph_num = {}
i = 1

for pn in periph_names:
    periph_num[pn] = i
    i += 1
    
class DeviceType:
   Gpio = 1
   Timer = 2
   Pwm = 3
   
    
def align_buffer(buff):
    k = len(buff) % 8
    if k == 0:
        return buff
    else:
        return buff + b'\0' * (8-k)
        
class PinConfig:
    def __init__(self, pin_name = None):
        if pin_name is not None:
            self.port = gpio_port_nums[pin_name[0:2]]
            self.pin = int(pin_name[2:])
        else:
            self.port = 0xff
            self.pin = 0xff
        
    def compile(self):
        return struct.pack('<BB', self.port, self.pin)
        
class DeviceConfig:
    def __init__(self, config_dict):
        self.device_id = periph_num[config_dict['name']]
        
class GpioConfig(DeviceConfig):
    def __init__(self, config_dict = None):        
        self.id = config_dict['id']
        self.pin = PinConfig(config_dict['pin'])
        self.dir = {'IN': 0, 'OUT_PP': 1, 'OUT_OD': 2}[config_dict['mode']]
        
    def compile(self):
        buff = struct.pack('<BB', DeviceType.Gpio, periph_num['GPIO'])
        buff += struct.pack('<BB', self.id, self.dir) + self.pin.compile()
        buff = struct.pack('<H', len(buff) + 2) + buff
        return buff

class TimerConfig(DeviceConfig):
    def __init__(self, config_dict):
        super().__init__(config_dict)
        self.prescaler = config_dict.get('prescaler', 1)
        self.period = config_dict['period']
        
    def compile(self):
        buff = struct.pack('<BB', DeviceType.Timer, self.device_id)
        buff += struct.pack('<II', self.prescaler, self.period)
        buff = struct.pack('<H', len(buff) + 2) + buff
        return buff
        
class PwmConfig(DeviceConfig):
    def __init__(self, config_dict):
        self.id = config_dict['id']
        self.device_id = periph_num[config_dict['timer']]
        self.channel = {'CH1': 1, 'CH2': 2, 'CH3': 3, 'CH4': 4}[config_dict['channel']]
        self.pin = PinConfig(config_dict['pin'])
        self.n_pin = PinConfig(config_dict.get('n_pin'))
        self.dir_pin = PinConfig(config_dict.get('dir_pin'))
        
    def compile(self):
        buff = struct.pack('<BB', DeviceType.Pwm, self.device_id)
        buff += struct.pack('<BB', self.id, self.channel) + self.pin.compile() + self.n_pin.compile() + self.dir_pin.compile()
        buff = struct.pack('<H', len(buff) + 2) + buff
        return buff
        
class EncoderConfig(DeviceConfig):
    def __init__(self, config_dict):
        super().__init__(config_dict)       
        self.period = config_dict['period']
        
    def compile(self):
        buff = struct.pack('<BB', 7, self.device_id)
        buff += struct.pack('<HH', self.prescaler, self.period)
        buff = struct.pack('<H', len(buff) + 2) + buff
        return buff
        
class UsartConfig(DeviceConfig):
    def __init__(self, config_dict):
        super().__init__(config_dict)
        self.fd = config_dict['fd']
        self.baudrate = config_dict['baudrate']
        self.rx_buffer_size = config_dict['rx_buffer_size']
        self.tx_buffer_size = config_dict['tx_buffer_size']
        self.rx_pin = PinConfig(config_dict['rx_pin'])
        self.tx_pin = PinConfig(config_dict['tx_pin'])
        
    def compile(self):
        buff = struct.pack('<BB', 1, self.device_id)
        buff += struct.pack('<BBHHH', self.fd, 0, self.rx_buffer_size, self.tx_buffer_size, 0)
        buff += self.rx_pin.compile() + self.tx_pin.compile() + struct.pack('<I', self.baudrate)
        buff = struct.pack('<H', len(buff) + 2) + buff
        return buff
        
class I2cConfig(DeviceConfig):
    def __init__(self, config_dict):
        super().__init__(config_dict)
        self.prescaler = config_dict['prescaler']
        self.period = config_dict['period']
        
    def compile(self):
        buff = struct.pack('<BB', 7, self.device_id)
        buff += struct.pack('<HH', self.prescaler, self.period)
        buff = struct.pack('<H', len(buff) + 2) + buff
        return buff
        
class SpiConfig(DeviceConfig):
    def __init__(self, config_dict):
        super().__init__(config_dict)
        self.prescaler = config_dict['prescaler']
        self.period = config_dict['period']
        
    def compile(self):
        buff = struct.pack('<BB', 7, self.device_id)
        buff += struct.pack('<HH', self.prescaler, self.period)
        buff = struct.pack('<H', len(buff) + 2) + buff
        return buff
        
class CanConfig(DeviceConfig):
    def __init__(self, config_dict):
        super().__init__(config_dict)
        self.prescaler = config_dict['prescaler']
        self.period = config_dict['period']
        
    def compile(self):
        buff = struct.pack('<BB', 7, self.device_id)
        buff += struct.pack('<HH', self.prescaler, self.period)
        buff = struct.pack('<H', len(buff) + 2) + buff
        return buff

class HALConfig:
    def __init__(self, config_dict):
        self.gpio = [GpioConfig(v) for v in config_dict.get('gpio', [])]
        self.timer = [TimerConfig(v) for v in config_dict.get('timer', [])]
        self.pwm = [PwmConfig(v) for v in config_dict.get('pwm', [])]
        #self.encoder = [EncoderConfig(v) for v in config_dict.get('encoder', [])]
        self.usart = [UsartConfig(v) for v in config_dict.get('usart', [])]        
        #self.i2c = [I2cConfig(v) for v in config_dict.get('i2c', [])]
        #self.spi = [SpiConfig(v) for v in config_dict.get('spi', [])]
        #self.can = [CanConfig(v) for v in config_dict.get('can', [])]
        
        
    def compile(self):
        config_buffers = []
        config_buffer_offsets = []
        offset = 0
        
        for p in self.gpio:
            buffer = align_buffer(p.compile())
            config_buffers.append(buffer)
            config_buffer_offsets.append(offset)
            offset += len(buffer)
            
        for p in self.timer:
            buffer = align_buffer(p.compile())
            config_buffers.append(buffer)
            config_buffer_offsets.append(offset)
            offset += len(buffer)
            
        for p in self.pwm:
            buffer = align_buffer(p.compile())
            config_buffers.append(buffer)
            config_buffer_offsets.append(offset)
            offset += len(buffer)
            
        for p in self.usart:
            buffer = align_buffer(p.compile())
            config_buffers.append(buffer)
            config_buffer_offsets.append(offset)
            offset += len(buffer)
            
        # compute 8 bytes aligned start offset
        start_offset = 2 + 2 * len(config_buffers)
        if start_offset % 8:
            start_offset += 8 - (start_offset % 8)
        buff = struct.pack('<H', len(config_buffers))
        for cbo in config_buffer_offsets:
            buff += struct.pack('<H',start_offset + cbo)
        buff += b'\0' * (start_offset - len(buff))
        for cb in config_buffers:
            buff += cb
        return buff
       
            