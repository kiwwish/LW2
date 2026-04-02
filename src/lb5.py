from MerDam import MerDam_hash
from alphabet import num2sym, str2vec


def kdf(mat: str, salt: str, con: list[str], size: list[int], iter: int) -> list:
    tmp = mat + salt
    out = []
    for i in range(iter + 1):
        ext = MerDam_hash(tmp)
        tmp = ext + tmp
    prk = tmp
    for i in range(len(size)):
        q = (size[i] - (size[i] % 64)) / 64
        rem = i
        res = ''
        while rem > 0:
            h = rem % 32
            res = res + num2sym(h)
            rem = (rem - h) / 32
        if q > 0:
            hash = prk
            for j in range(q + 1):
                tmp = hash + con[i] + prk
                hash = MerDam_hash(tmp)
                res = hash + res
        else:
            tmp = prk + con[i] + prk
            res = MerDam_hash(tmp)
        out_i = res[0: size[i]]
        out.append(out_i)
    return out

"""
pass1 = 'ЧЕЧЕТКА'
pass2 = 'АПРОЛ'
salt1 = 'СЕАНС'
salt2 = 'АТЛЕТ'
context = ['СЕАНСОВЫЙ_КЛЮЧ', 'КЛЮЧ_РАСПРЕДЕЛЕНИЯ_КЛЮЧЕЙ']
size = [32, 16]

print(kdf(pass1, salt1, context, size, 2))
print(kdf(pass2, salt1, context, size, 2))
"""

def bin2msg(bin: list) -> str:
    B = len(bin)
    b = B // 5
    q = B % 5
    out = ''

    for i in range(b):
        t = 0
        # Читаем биты в том же порядке, как они были записаны
        # В msg2bin биты записываются от младшего к старшему
        for j in range(4, -1, -1):  # Идем с конца блока к началу
            t = t * 2 + bin[i * 5 + j]
        out = out + num2sym(t)

    if q > 0:
        for k in range(q):
            out = out + str(bin[b * 5 + k])

    return out

def sym2bin(s):
    alphabet = '_АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ'
    return alphabet.find(s)

def num2sym(num):
    alphabet = '_АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ'
    if 0 <= num < len(alphabet):
        return alphabet[num]
    return '?'

def isSym(s):
    alphabet = '_АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ'
    return 1 if s in alphabet else -1

def msg2bin(msg) -> list:
    m = len(msg)
    i = 0
    f = 0
    tmp = []

    while i < m and isSym(msg[i]) == 1:
        p = msg[i]
        c = sym2bin(p)
        bits = []
        for j in range(4, -1, -1):
            bit = (c >> j) & 1
            bits.append(bit)
            tmp.append(bit)
        if i == m - 1:
            f = 1
            break
        else:
            i = i + 1
    if f == 0:
        for k in range(i, m):
            p = msg[k]
            if p in '01':
                tmp.append(int(p))
            else:
                c = sym2bin(p)
                for j in range(4, -1, -1):
                    bit = (c >> j) & 1
                    tmp.append(bit)
    return tmp

def bin2msg(bin: list) -> str:
    B = len(bin)
    b = B // 5
    q = B % 5
    out = ''
    for i in range(b):
        t = 0
        for j in range(5):
            bit = bin[i * 5 + j]
            t = 2 * t + bit
        out = out + num2sym(t)
    if q > 0:
        for k in range(q):
            bit = bin[b * 5 + k]
            print(bit, end='')
            out = out + str(bit)
        print()
    return out

"""
test = 'ГНОЛЛЫ_ПИЛИЛИ_ПЫЛЕСОС_ЛОСЕСЕМ'
x = msg2bin(test)
y = bin2msg(x)
print(f"\nОригинал: {test}")
print(f"Результат: {y}")

test_1 = 'ГНОЛЛЫ_ПИЛИЛИ_ПЫЛЕСОС_ЛОСОСЕМ00111'
x1 = msg2bin(test_1)
y1 = bin2msg(x1)
print(f"\nОригинал: {test_1}")
print(f"Результат: {y1}")
"""