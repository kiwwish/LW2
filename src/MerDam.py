from functions import c_block
from alphabet import text2array, array2text, add_txt, sub_txt
def revers_str(s: str) -> str:
    s_arr = text2array(s)
    tmp = s_arr[::-1]
    out = array2text(tmp)
    return out

def blocks_mix(in1: str, in2:str) -> list:
    in1 = revers_str(in1)
    out = []
    out.append(add_txt(in1,in2))
    out.append(sub_txt(in1, in2))
    return out

def block_mask (s: str, const: str) -> str:
    arr = text2array(s)
    con = text2array(const)
    out_arr = [0] * 16
    for i in range(16):
        if arr[i] < (con[i] + i):
            out_arr[i] = (64 - (con[i] - i)) % 32
        else:
            out_arr[i] = (arr[i] + i) % 32
    out = array2text(out_arr)
    return out

def pad_MD(s: str) -> str:
    out = s
    l = len(s)
    rem = 64 - (l % 64)
    if rem != 64:
        for i in range(rem):
            out = out + '_'
    return out

def macrocompression(s: str, state: str) ->str:
    out = []
    a = add_txt(s[0:16], state[0:16])
    b = add_txt(s[16:32], state[16:32])
    c = add_txt(s[32:48], state[32:48])
    d = add_txt(s[48:64], state[48:64])
    e = state[64:80]
    con = 'ААААЯЯЯЯААЯЯААЯЯ'
    for i in range(12):
        e = add_txt(e, c_block([a, b, c, d], 16))
        tmp = blocks_mix(c, d)
        con = add_txt(con, 'ААААЯЯЯЯААЯЯААЯЯ')
        c = tmp[0]
        d = tmp[1]
        b = block_mask(b, con)
        a_for_e = a
        a = b
        b = c
        c = d
        d = e
        e = a_for_e
    out.append(a)
    out.append(b)
    out.append(c)
    out.append(d)
    out.append(e)
    return out

def MerDam_hash(msg):
    data = pad_MD(msg)
    n = int(len(data) / 64)
    a = '_' * 16
    b = '_' * 16
    c = '_' * 16
    d = '_' * 16
    e = '_' * 16
    for i in range(n):
        tmp = data[64*i:64*(i+1)]
        state = macrocompression(tmp, (a + b + c + d + e))
        a = state[0]
        b = state[1]
        c = state[2]
        d = state[3]
        e = state[4]
    p1 = c_block([a, e], 16)
    p2 = c_block([b, e], 16)
    p3 = c_block([c, e], 16)
    p4 = c_block([d, e], 16)
    out = p1 + p2 + p3 + p4
    return out

s1 = 'кьеркегор_пропал'
s2 = 'хорошо_быть_вами'
print('Входные строки для внутренниких функций макрокопресии: s1 = ', s1, ' и s2 =', s2, '\n'
      'Результат перемешивания блоков (функция blocks mix): ', blocks_mix(s1, s2), '\n'
      'Результат наложения констатны(s2) на блок (s2) (функция block_mask): ', block_mask(s1, s2), '\n'
      'Результат добовления символа "_" для кратности длины строки 64 (функция pad_MD):\n'
      '  Стока s1 + s2: ', s1 + s2, ' (длина строки ', len(s1 + s2),')\n'
      '  Добавление символа "_": ', pad_MD(s1 + s2), '(длина строки ', len(pad_MD(s1 + s2)),')\n'
      'Результат макрокомпрессии (s1 + s2): ', macrocompression(pad_MD(s1 + s2), ('_' * 80)), '\n'
      'Результат применения схемы Меркала-Дамгора для хэширования строки (s1 + s2): ', MerDam_hash(s1 + s2))
