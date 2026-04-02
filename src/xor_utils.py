from lcg_utils import block2num, num2block, dec2bin, bin2dec
from ct_lcg import produce_round_keys
from scytale import frw_P_scitala

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

set1 = []
set10 = [252564, 9109, 961193]
set1.append(set10)
set11 = [252564, 9109, 961193]
set1.append(set11)
set12 = [723482, 8677, 983609]
set1.append(set12)
SET0 = set1

set2 = []
set20 = [51190, 7927, 990711]
set2.append(set20)
set21 = [51190, 7927, 990711]
set2.append(set21)
set22 = [549234, 6949, 939683]
set2.append(set22)
SET1 = set2

set3 = []
set30 = [227796, 5107, 981875]
set3.append(set30)
set31 = [227796, 5107, 981875]
set3.append(set31)
set32 = [167490, 9871, 809137]
set3.append(set32)
SET2 = set3

set4 = []
set40 = [357630, 8971, 948209]
set4.append(set40)
set41 = [357630, 8971, 948209]
set4.append(set41)
set42 = [73335, 6779, 1014784]
set4.append(set42)
SET3 = set4

SET = []
SET.append(SET0)
SET.append(SET1)
SET.append(SET2)
SET.append(SET3)
key1 = 'ПОЛИМАТ_ТЕХНОБОГ'
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
keys1 = produce_round_keys(key1, 6, SET)
print('Результат операции побитового XOR для блоков АГАТ и ТАГА: ', block_xor(inA, inB), '\n'
       '', '\n'                                                                                  
      'Раундовые ключи:')
for i, out_str in enumerate(keys1):
    print(f"  Ключ {i+1}: {out_str}")
print('\n'
      'Результат перестановки "скитала" для блока "ДЖИГУРДА": ', frw_P_scitala('ДЖИГУРДА'))
"""


