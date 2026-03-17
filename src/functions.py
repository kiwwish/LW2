from polyTritimus import PolyalphabeticTrithemus
from alphabet import text2array, array2text, add_txt, sub_txt
def core_Tritimus (in_prime: str, in_aux: str) -> str:
    out = 'Ошибка ввода'
    if len(in_prime) == 16 & len(in_aux) == 16:
        cipher = PolyalphabeticTrithemus(in_prime)  # ключ — in_prime
        out = cipher.encrypt(in_aux)
    return out

def confuse (in1: str, in2: str) -> str:
    if len(in1) == 16 & len(in2) == 16:
        arr1 = text2array(in1)
        arr2 = text2array(in2)
        for i in range(16):
            if arr1[i] > arr2[i]:
                arr1[i] = (arr1[i]+i) % 32
            else:
                arr1[i] = (arr2[i] + i) % 32
            tmp = array2text(arr1)
            out = add_txt(add_txt(tmp, in1), in2)
    return out

def mixinputs (in_arr):
    in1 = in_arr[0]
    in2 = in_arr[1]
    in3 = in_arr[2]
    in4 = in_arr[3]
    out = []
    out1 = add_txt(in1, in2)
    out2 = sub_txt(in1, in2)
    out3 = add_txt(out2, add_txt(in3, in4))
    out4 = add_txt(out1, sub_txt(in3, in4))
    out.append(out1)
    out.append(out2)
    out.append(out3)
    out.append(out4)
    return out

def compress (in_16: str, out_n) -> str:
    out = 'Ошибка ввода'
    if len(in_16) != 16:
        return out
    if out_n == 16:
        return in_16.upper()
    a1 = in_16[0:4]
    a2 = in_16[4:8]
    a3 = in_16[8:12]
    a4 = in_16[12:16]
    if out_n == 8:
        a13 = a1 + a3  # concat(a1, a3)
        a24 = a2 + a4  # concat(a2, a4)
        out = add_txt(a13, a24)
    elif out_n == 4:
        a13 = sub_txt(a1, a3)
        a24 = sub_txt(a2, a4)
        out = add_txt(a13, a24)
    else:
        out = in_16.upper()
    return out

def c_block (in_arr: list, out_size: int) -> str:
    out = 'Ошибка ввода'
    r = len(in_arr)
    c = ['________________',
         'ПРОЖЕКТОР_ЧЕПУХИ',
         'КОЛЫХАТЬ_ПАРОДИЮ',
         'КАРМАННЫЙ_АТАМАН']
    flag = 1
    for i in range(r):
        if len(in_arr[i]) == 16:
            c[i] = add_txt(c[i], in_arr[i])
        else:
            flag = 0
    if flag == 1:
        c = mixinputs(c)
        tmp1 = core_Tritimus(c[0], c[2])
        tmp2 = core_Tritimus(c[3], c[1])
        tmp3 = confuse(tmp1, tmp2)
        out = core_Tritimus(tmp3, tmp1)
        out = compress(out, out_size)
    return out

#in_arr1 = ['ХОРОШО_БЫТЬ_ВАМИ']
#in_arr2 = ['ХОРОШО_БЫТЬ_ВАМИ',
#       '________________',
#       '________________',
#       '________________']

#in1 = 'хорошо_быть_вами'
#in2 = 'кьеркегор_пропал'
#print('Входные строки: in1 = ', in1, ' и in2 = ', in2, '\n'
#      'Результат работы полиалфавитного шифра Тритимуса (in1 - входная строка, in2 - ключ): ', core_Tritimus(in1, in2), '\n'
#     'Результат работы функции confuse: ', confuse(in1, in2), '\n'
#     'Результат работы функции comress для in1 до длины 8: ', compress(in1, 8), '\n'
#     'Результат работы функции comress для in2 до длины 4: ', compress(in2, 4), '\n'
#     '\n'
#     'Массивы строк: ', '\n'
#     '   in_arr1 = ', in_arr1, '\n'
#     '   in_arr2 = ', in_arr2, '\n'
#     '\n'
#     'Результат функции сжатия (функция c_block) массива in_arr1 дл строки из 8 символов: ', c_block(in_arr1, 8), '\n'
#     'Результат функции сжатия (функция c_block) массива in_arr2 дл строки из 4 символов: ', c_block(in_arr2, 4))


""" Функции для лабораторной работы №3 """

def block2num(BLOCK_IN: str) -> int:
    if len(BLOCK_IN) != 4:
        return "input_error"  # Как в методичке
    tmp = text2array(BLOCK_IN)
    out = 0
    pos = 1
    for i in range(3, -1, -1):
        out = pos * tmp[i] + out
        pos = 32 * pos
    return out

#print(block2num('АБВГ'))

def num2block(num_in: int) -> str:
    rem = num_in
    tmp = [0] * 4
    for i in range(4):
        tmp[3 - i] = rem % 32
        rem = rem // 32
    return array2text(tmp)

#print(num2block(34916))

def dec2bin(num_in: int) -> list[int]:
    rem = num_in
    out = [0] * 20
    for i in range(20):
        out[19-i] = rem % 2
        rem = rem // 2
    return out

#print(dec2bin(34916))

def bin2dec(BIN_IN: list[int]) -> int:
    out = 0
    for i in range(20):
        out = 2 * out + BIN_IN[i]
    return out

#a = dec2bin(34916)
#print(bin2dec(a))

def initialize_PRNG(Seed_in: str) -> list:

    Const = [
        "ПЕРВОЕ_АКТЕРСТВО",
        "ВТОРОЙ_ДАЛЬТОНИК",
        "ТРЕТЬЯ_САДОВНИЦА",
        "ЧЕТВЕРТЫЙ_ГОБЛИН"]

    OUT = []
    value = []
    for i in range(4):
        const = Const[i]
        value_i = c_block([const, Seed_in], 16)
        value.append(value_i)
    secret = c_block(value, 16)

    for i in range(4):
        tmp = value[i]
        TMP = ""
        for j in range(4):
            tmp = add_txt(tmp, Const[i])
            TMP = TMP + c_block([tmp, secret], 4)
            tmp = add_txt(tmp, TMP)

        out_i = TMP[4:16]
        OUT.append(out_i)
    return OUT

#in1 = 'ХОРОШО_БЫТЬ_ВАМИ'
#in2 = '________________'
#print(initialize_PRNG(in1))
#print(initialize_PRNG(in2))

def make_coeffs(bpr_in: list, spr_in: list, pow_in: int ) -> int:
    ss = min(spr_in)
    bs = min(bpr_in)
    bb = max(bpr_in)
    sb = max(spr_in)
    MAX = 2**(pow_in) - 1
    tmp = bs * ss
    a = ss * bs * sb + 1
    c = bb
    for i in range(pow_in):
        if tmp * ss >= MAX:
            break
        else:
            tmp = tmp * ss
    m = tmp
    if (a < m) and (c < m):
        out = [a, c, m]
    else:
        out = 'wrong_guess'
    return out

#arr_1 = [8677, 739]
#arr_2 = [11, 89]
#print(make_coeffs(arr_1, arr_2, 20))

def lcg_next(state_in: int, coefs_in: list) -> list:
    a = coefs_in[0]
    c = coefs_in[1]
    m = coefs_in[2]
    out = (a * state_in + c) % m
    return out

#lcg_set1 = [723482, 8677, 983609]
#cg_seed1 = block2num('ЛУЛУ')
#out = LCG_next(lcg_seed1, lcg_set1)
#print(num2block(out))

def compose_num(num1: int, num2: int, cont: int) -> int:
    arr1 = dec2bin(num1)
    arr2 = dec2bin(num2)
    arr3 = dec2bin(cont)
    arr = []
    for i in range(20):
        arr_i = (arr1[i] * arr3[i]) + (arr2[i] * ((1 + arr3[i]) % 2))
        arr.append(arr_i)
    out = bin2dec(arr)
    return out
"""
num1 = 1231
print(dec2bin(num1))
num2 = 723482
print(dec2bin(num2))
cont1 = 448033
cont2 = 41505
cont3 = 666
print(compose_num(num1, num2,cont1))
print(compose_num(num1, num2, cont2))
print(compose_num(num1, num2, cont3))
"""
def seed2num(array_in: list) -> list:
    out = []
    for i in range (3):
        out_i = block2num(array_in[i])
        out.append(out_i)
    return out

#print(seed2num_1(['АПЧХ', 'ЧПОК', 'ШУРА']))

def ct_lcg_next(sate_in: list, set_in: list) -> list:
    first = lcg_next(sate_in[0], set_in[0])
    second = lcg_next(sate_in[1], set_in[1])
    control = lcg_next(sate_in[2], set_in[2])
    out = compose_num(first, second, control)
    state_out = [first, second, control]
    return [out, state_out]

"""
s1 = seed2num(['АПЧХ', 'ЧПОК', 'ШУРА'])
s2 = seed2num(['ЗЗЕП', 'ТОБУ', 'ИВТС'])
s3 = seed2num(['ЭМПД', 'ЦКПР', 'КЩГЫ'])

set = []
set_0 = [723482, 8677, 983609]
set_1 = [252564, 9109, 961193]
set_2 = [357630, 8971, 948209]
set.append(set_0)
set.append(set_1)
set.append(set_2)
print(set)

out1_0 = ct_lcg_next(s1, set)
print(out1_0)
"""

def wrap_ct_clcg_next(flag: str, STATE, SEED, SET: list) -> list:
    out = 'something_wrong'
    stream = ''
    check = 0
    if flag == 'up':
        init = initialize_PRNG(SEED)
        state = []
        for i in range(4):
            state_i = seed2num([init[i][0:4], init[i][4:8], init[i][8:12]])
            state.append(state_i)
            check = 1
    elif flag == 'down':
        state = STATE
        check = 1
    if check == 1:
        for j in range(4):
            tmp = 0
            sign = 1
            for i in range(4):
                T = ct_lcg_next(state[i], SET[j])
                state[i] = T[1]
                tmp = (1048576 + sign * T[0] + tmp) % 1048576
                sign = 0 - sign
            stream = stream + num2block(tmp)
        out = [stream, state]
    return out

set1 =[]
set10 = [252564, 9109, 961193]
set1.append(set10)
set11 = [252564, 9109, 961193]
set1.append(set11)
set12 = [723482, 8677, 983609]
set1.append(set12)
SET0 = set1

set2 =[]
set20 = [51190, 7927, 990711]
set2.append(set20)
set21 = [51190, 7927, 990711]
set2.append(set21)
set22 = [549234, 6949, 939683]
set2.append(set22)
SET1 = set2

set3 =[]
set30 = [227796, 5107, 981875]
set3.append(set30)
set31 = [227796, 5107, 981875]
set3.append(set31)
set32 = [167490, 9871, 809137]
set3.append(set32)
SET2 = set3

set4 =[]
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

seed = 'АБВГДЕЖЗИЙКЛМНОП'
result = wrap_ct_clcg_next("up", -1, seed, SET)
all_outputs = []
all_outputs.append(result[0])
current_state = result[1]

for i in range(8):
    result = wrap_ct_clcg_next("down", current_state, -1, SET)
    all_outputs.append(result[0])
    current_state = result[1]

for i, out_str in enumerate(all_outputs):
    print(out_str)


