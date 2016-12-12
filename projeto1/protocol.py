import binascii

from bitarray import bitarray 

def binstr_to_bools(string):
    # TODO assert that string contains only 0's and 1's
    return [ c == '1' for c in string]


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
    fargoff = '000000000000'
    ttl = '01010101'

    protocol = cmd_to_bin(cmd)    

    crc = '0000000000000000' #TODO
    srcadd = '00000000000000000000000000000000' #TODO
    destadd = '00000000000000000000000000000000' #TODO

    options = bin(int.from_bytes(param.encode(), 'big'))[2:]
    size = len(options)

    total_length = bitarray(bin(32 * 5 + size)[2:])

    i = 16 - total_length.length()

    s = ''

    while (i >= 0):
        s = s + '0'
        i -= 1

    tlfinal = bitarray(s)
    tlfinal.append(total_length)

    to_append = [version, ihl, tos, tlfinal, ident, flags, fargoff, ttl, protocol, crc, srcadd, destadd, options]

    for string in to_append:
        b.extend(binstr_to_bools(string))

    arr = b.tobytes()
    print(binascii.hexlify(arr))
    return b.tobytes()


def decode_request(b):
    return str(binascii.hexlify(b))
    # TODO implement
"""
    version = '0010'
    ihl = '0101'
    tos = '00000000'
    ident = '0000000000000000'
    flags = '000'
    fragoff = '000000000000'
    ttl = '01010101'

    if(cmd == 'ps'):
        protocol = '00000001'
    elif(cmd == 'df'):
        protocol = '00000010'
    elif(cmd == 'finger'):
        protocol = '00000100'
    else:
        protocol = '00001000'

    crc = '0000000000000000' #TODO
    srcadd = '00000000000000000000000000000000' #TODO
    destadd = '00000000000000000000000000000000' #TODO

    options = bitarray(bin(int.from_bytes(param.encode(), 'big')))
    size = options.length()
    
    total_length = Bitarray(bin(32 * 5 + size))
    i = 16 - totallenght.length()
    s = ''
    while (i >= 0):
        s = s + '0'

    tl_final = bitarray(s)
    tl_final.append(total_length)

    b.append(version + ihl + tos + tl_final + ident + flags + fargoff + ttl + protocol + crc + srcadd + destadd + options)

    return b.tobytes()

"""
