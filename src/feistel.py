from polyTritimus import EnhancedSTrithemus
from alphabet import add_txt, sub_txt
from xor_utils import block_xor
from scytale import frw_P_scitala, inv_P_scitala

def frw_routine_Feistel(block: str, key: str) -> str:
    left = block[0: 4]
    right = block[4: 8]
    tmp = EnhancedSTrithemus.encrypt_block(right, key)
    left = add_txt(tmp, left)
    return right + left

in1 = 'ГОР_СВЕТ'
in2 = 'ЕГОР_КОТ'
key = 'ЗОЛОТУХА_ПИКЕТКА'
#print(frw_routine_Feistel(in2, key))
out1 = frw_routine_Feistel(in1, key)
out2 = frw_routine_Feistel(in2, key)

def inv_routine_Feistel(block: str, key: str) -> str:
    l = len(block)
    left = block[: l//2]
    right = block[l//2:]
    tmp = EnhancedSTrithemus.encrypt_block(left, key)
    right = sub_txt(right, tmp)
    return right + left

#print(inv_routine_Feistel(out1, key), inv_routine_Feistel(out2, key))

def frw_inner_Feistel(block: str, key: str, r: int) -> str:
    tmp = frw_P_scitala(block)
    for i in range(r):
        tmp = frw_routine_Feistel(tmp, key)
    return frw_P_scitala(tmp)

out1t = frw_inner_Feistel(in1, key, 2)
out2t = frw_inner_Feistel(in2, key, 2)
#print(out1t, out2t)

def inv_inner_Feistel(block: str, key: str, r: int) -> str:
    tmp = inv_P_scitala(block)
    for i in range(r):
        tmp = inv_routine_Feistel(tmp, key)
    return inv_P_scitala(tmp)

#print(inv_inner_Feistel(out1t, key, 2))

def round_Feistel(block: str, key: str) -> str:
    left = block[:8]
    right = block[8:]
    tmp = frw_inner_Feistel(right, key, 3)
    left = block_xor(tmp, left)
    return right + left

def swap_blocks(block: str) -> str:
    left = block[:8]
    right = block[8:]
    return right + left

"""in_1 = 'КОРЫСТЬ_СЛОНА_ЭХ'
in_2 = 'НУЖНО_БОЛЬШЕ_ПЫЩ'
key_1 = 'МТВ_ВСЕ_ЕЩЕ_ТЛЕН'
out1l = round_Feistel(in_1, key_1)
out2l = round_Feistel(in_2, key_1)
tmp1l = swap_blocks(out1l)
tmp2l = swap_blocks(out2l)
print(out1l, out2l)
print(tmp1l, tmp2l)
"""
