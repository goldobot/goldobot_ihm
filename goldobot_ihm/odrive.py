
ODRIVE_JSON_CRC = 0x7411

CRC16_INIT = 0x1337
CRC16_DEFAULT = 0x3d65
PROTOCOL_VERSION = 1

ODRIVE_TYPES = {
    'bool': (1, '?', bool),
    'uint8': (1, 'B', int),
    'uint16': (2, 'H', int),
    'uint32': (4, 'I', int),
    'uint64': (8, 'Q', int),
    'int8': (1, 'b', int),
    'int16': (2, 'h', int),
    'int32': (4, 'i', int),
    'int64': (8, 'q', int),
    'float': (4, '<f', float)
   }

def calc_crc(remainder, value, polynomial, bitwidth):
    topbit = (1 << (bitwidth - 1))

    # Bring the next byte into the remainder.
    remainder ^= (value << (bitwidth - 8))
    for bitnumber in range(0,8):
        if (remainder & topbit):
            remainder = (remainder << 1) ^ polynomial
        else:
            remainder = (remainder << 1)

    return remainder & ((1 << bitwidth) - 1)

def calc_crc16(remainder, value):
    if isinstance(value, bytearray) or isinstance(value, bytes) or isinstance(value, list):
        for byte in value:
            if not isinstance(byte, int):
                byte = ord(byte)
            remainder = calc_crc(remainder, byte, CRC16_DEFAULT, 16)
    else:
        remainder = calc_crc(remainder, value, CRC16_DEFAULT, 16)
    return remainder

def calc_json_crc(json_bytes):
    return calc_crc16(PROTOCOL_VERSION, json_bytes)
    
def parse_item(js, prefix, endpoints, functions):
    if js['type'] == 'object':
        for m in js['members']:
            parse_item(m, prefix + js['name'] + '.', endpoints, functions)
        return
    if js['type'] == 'function':
        functions[prefix + js['name']] = js
        return
    if js['id'] == 0:
        return
    endpoints[prefix + js['name']] = (js['id'], js['type'], js['access'])