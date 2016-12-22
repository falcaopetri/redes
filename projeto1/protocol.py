from bitarray import bitarray
import logging
import binascii

def crc16(data):
    # Source: https://gist.github.com/oysstu/68072c44c02879a2abf94ef350d1c7c6
    poly = 0x8408
    crc = 0xFFFF
    for byte in data:
        curr_byte = 0xFF & byte
        for i in range(8):
            if (crc & 0x0001) ^ (curr_byte & 0x0001):
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1

            curr_byte >>= 1

    crc = (~crc & 0xFFFF)
    crc = (crc << 8) | ((crc >> 8) & 0xFF)
    crc = 0x0000FFFF & crc
    return crc


def binstr_to_bools(string):
    arr = []

    for c in string:
        if c not in ['0', '1']:
            raise Exception('Invalid boolean string. %s should contain only 0s and 1s' % string)
        
        arr.append( c == '1' )
 
    return arr


def str_from_bits(bits):
    # Source: http://stackoverflow.com/a/10238140
    chars = []
    n_bytes = len(bits) // 8
    for b in range(n_bytes):
        idx = b*8
        byte = bits[idx:idx+8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def cmd_to_bin(cmd):
    m = {
            'ps': '00000001',
            'df': '00000010',
            'finger': '00000100',
            'uptime': '00001000'
    }

    return m[cmd] if cmd in m else '00000000'

def IP2Bin(ip):
    if ip is None:
        return "".zfill(32)

    o = list()
    for i in ip.split('.'):
        o.append(i)    
    res = (256**3 * int(o[0])) + (256**2 * int(o[1])) + (256**1 * int(o[2])) + (256**0 * int(o[3]))
    res = bin(res)[2:].zfill(32)
    return res


def Bin2IP(ipnum):
    ipnum = int(ipnum, 2)
    o1 = int(ipnum / 16777216) % 256
    o2 = int(ipnum / 65536) % 256
    o3 = int(ipnum / 256) % 256
    o4 = int(ipnum) % 256
    return '%(o1)s.%(o2)s.%(o3)s.%(o4)s' % locals()

def encode_request(cmd, param, src, dest):
    return encode_bin(cmd, param, src, dest, '000')

def encode_response(cmd, param, src, dest):
    return encode_bin(cmd, param, src, dest, '111')


def encode_bin(cmd, param, src, dest, flag):
    version = '0010'
    ihl = '0101'
    tos = '00000000'
    ident = '0000000000000000'
    flags = flag
    fargoff = '0000000000000'
    ttl = '01010101'
    if (flags == '111'):
	# TODO prev_ttl deveria ser passado como parametro, e ttl deveria ser ttl=prev_ttl-1
        ttl = int(ttl, 2) - 1
        ttl = bin(ttl)[2:].zfill(8)

    protocol = cmd_to_bin(cmd)    

    crc = '0000000000000000' #TODO
    srcadd = IP2Bin(src) 
    destadd = IP2Bin(dest) 

    options = ''
    for c in param.encode():
        options += bin(c)[2:].zfill(8)

    size = len(options)

    total_length_value = bin(32 * 5 + size)[2:]
    tlfinal = total_length_value.zfill(16)

    to_append = [version, ihl, tos, tlfinal, ident, flags, fargoff, ttl, protocol, crc, srcadd, destadd, options]

    b = bitarray()
    for string in to_append:
        b.extend(binstr_to_bools(string))

    checksum = crc16(b.tobytes())
    logging.debug("calculated checksum: %s" % str(checksum))
    checksum = bin(checksum)[2:].zfill(16)
    logging.debug("calculated checksum: %s" % str(checksum))
    logging.debug("hex msg %s" % binascii.hexlify(b.tobytes()).decode())
    to_append = [version, ihl, tos, tlfinal, ident, flags, fargoff, ttl, protocol, checksum, srcadd, destadd, options]
    
    b = bitarray()
    for string in to_append:
        b.extend(binstr_to_bools(string))

    #logging.debug("hex msg %s" %binascii.hexlify(b.tobytes()).decode())


    return b.tobytes()


def check_checksum(stringbits):
    checksum_recv = stringbits[80:96]
    logging.debug("x1: %s" % checksum_recv)
    logging.debug("x2: %s" % str(checksum_recv))
    stringbits = stringbits.replace(checksum_recv, '0'*len(checksum_recv))

    bits = bitarray()
    bits.extend(binstr_to_bools(stringbits))
    checksum = crc16(bits.tobytes())
    logging.debug("x3: %s" % str(checksum))
    logging.debug("x3: %s" % str(int(checksum_recv, 2)))

    return int(checksum_recv, 2) == checksum


def decode(b):
    logging.debug("<decoding>")
    bits = bitarray()
    bits.frombytes(b)

    stringbits = bits.to01()
    if not check_checksum(stringbits):
        raise AssertionError("checksum errado")

    version = stringbits[0:4]
    ihl = int(stringbits[4:8], 2)
    tos = stringbits[8:16]
    tlfinal = int(stringbits[16:32], 2)
    ident = stringbits[32:48]
    flags = stringbits[48:51]
    fragoff = stringbits[51:64]
    ttl = stringbits[64:72]
    protocol = stringbits[72:80]

    if (protocol == '00000001'):
        cmd = 'ps'
    elif (protocol == '00000010'):
        cmd = 'df'
    elif (protocol == '00000100'):
        cmd = 'finger'
    else:
        cmd = 'uptime'

    crc = stringbits[80:96]
    srcadd = stringbits[96:128]
    src = Bin2IP(srcadd)
    destadd = stringbits[128:160]
    dest = Bin2IP(destadd)
    options = stringbits[160:tlfinal+1]

    return (cmd, str_from_bits(options))
