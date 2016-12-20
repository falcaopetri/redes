import binascii

from bitarray import bitarray 

def binstr_to_bools(string):
    # TODO assert that string contains only 0's and 1's
    return [ c == '1' for c in string]

def str_from_bits(bits):
    # Source: http://stackoverflow.com/a/10238140
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
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
    b = bitarray()

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

    for string in to_append:
        b.extend(binstr_to_bools(string))

    return b.tobytes()


def decode(b):
    bits = bitarray()
    bits.frombytes(b)

    stringbits = bits.to01()
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
