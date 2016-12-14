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

    return m[cmd]


def encode_request(cmd, param, src, dest):
    b = bitarray()

    version = '0010'
    ihl = '0101'
    tos = '00000000'
    ident = '0000000000000000'
    flags = '000'
    fargoff = '0000000000000'
    ttl = '01010101'

    protocol = cmd_to_bin(cmd)    

    crc = '0000000000000000' #TODO
    srcadd = '00000000000000000000000000000000' #TODO
    destadd = '00000000000000000000000000000001' #TODO

    options = bin(int.from_bytes(param.encode(), 'big'))[2:]
    size = len(options)

    total_length_value = bin(32 * 5 + size)[2:]
    tlfinal = total_length_value.zfill(16)

    to_append = [version, ihl, tos, tlfinal, ident, flags, fargoff, ttl, protocol, crc, srcadd, destadd]

    for string in to_append:
        b.extend(binstr_to_bools(string))

    options = param
    for c in options.encode():
        b.extend(bin(c)[2:].zfill(8))

    return b.tobytes()


def decode_request(b):
    bits = bitarray()
    bits.frombytes(b)

    stringbits = bits.to01()
    version = stringbits[0:4]
    ihl = int(stringbits[4:8], 2)
    tos = stringbits[8:16]
    tlfinal = int(stringbits[16:32], 2)
    //print("tlfinal", stringbits[16:32])
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
    destadd = stringbits[128:160]

    options = stringbits[160:tlfinal+1]

    return cmd + " " + str_from_bits(options)
