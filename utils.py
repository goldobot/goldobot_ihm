


def compute_crc(buffer):
    crc = 0
    for b in buffer:
        x = crc >> 8 ^ b;
        x ^= x >> 4;
        crc = ((crc << 8) ^ (x << 12) ^ (x << 5) ^ x) & 0xffff;
    return crc