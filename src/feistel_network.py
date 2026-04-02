from xor_utils import block_xor
from feistel import round_Feistel, swap_blocks
from ct_lcg import produce_round_keys

def frw_Feistel(block_in: str, keys: list, r: int) -> str:
    key_set = keys
    block = block_xor(block_in, key_set[0])
    for i in range(r + 1):
        block = round_Feistel(block, key_set[i])
    out = block_xor(block,key_set[r + 1])
    return out

def inv_Feistel(block: str, keys: list, r: int) -> str:
    key_set = keys
    block = block_xor(block, key_set[r + 1])
    block = swap_blocks(block)
    for i in range(r, -1, -1):
        block = round_Feistel(block, key_set[i])
    block = swap_blocks(block)
    out = block_xor(block, key_set[0])
    return out


s1 = 'КОРЫСТЬ_СЛОНА_ЭХ'
s2 = 'НУЖНО_БОЛЬШЕ_ПЫЩ'
key_s = 'МТВ_ВСЕ_ЕЩЕ_ТЛЕН'
# keys = produce_round_keys(key_s, 6, SET)
# out1tf = frw_Feistel(s1, keys, 1)
#lout1tf = inv_Feistel(out1tf, keys, 1)
#out2tf = frw_Feistel(s2, keys, 4)
#lout2tf = inv_Feistel(out2tf, keys, 4)
#print(out1tf, lout1tf)
#print(out2tf, lout2tf)


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

"""
print()
print('Новые раундовые ключи:')
keys1 = produce_round_keys(key_s, 6, SET)
for i, out_str in enumerate(keys1):
    print(f"  Ключ {i+1}: {out_str}")
print()
print('Применение многораундного алгоритма с числом раундов 1 и 4:', frw_Feistel(s1, keys1, 1), ', ', frw_Feistel(s2, keys1, 4))
"""