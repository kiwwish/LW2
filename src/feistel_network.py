from xor_utils import block_xor
from feistel import round_Feistel, swap_blocks

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

"""
s1 = 'КОРЫСТЬ_СЛОНА_ЭХ'
s2 = 'НУЖНО_БОЛЬШЕ_ПЫЩ'
key_s = 'МТВ_ВСЕ_ЕЩЕ_ТЛЕН'
keys = produce_round_keys(key_s, 6, SET)
out1tf = frw_Feistel(s1, keys, 1)
lout1tf = inv_Feistel(out1tf, keys, 1)
out2tf = frw_Feistel(s2, keys, 4)
lout2tf = inv_Feistel(out2tf, keys, 4)
print(out1tf, lout1tf)
print(out2tf, lout2tf)
"""