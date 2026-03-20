from lcg_utils import block2num, num2block, dec2bin, bin2dec

def subblocks_xor(block_a: str, block_b: str) -> str:
    decA = block2num(block_a)
    decB = block2num(block_b)
    binA = dec2bin(decA)
    binB = dec2bin(decB)
    binO =[]
    for i in range(len(binA)):
        binO_i = (binA[i] + binB[i]) % 2
        binO.append(binO_i)
    out = bin2dec(binO)
    return num2block(out)

"""
inA = 'АГАТ'
inB = 'ТАГА'
print(subblocks_xor(inA, inB))
"""

def block_xor(block_a: str, block_b: str) -> str:
    nb = len(block_a) // 4
    out = ''
    for i in range(nb):
        tmpA = block_a[i * 4: i * 4 + 4]
        tmpB = block_b[i * 4: i * 4 + 4]
        out = out + subblocks_xor(tmpA, tmpB)
    return out

"""
inA = 'АГАТ'
inB = 'ТАГА'
print(block_xor(inA, inB))
"""