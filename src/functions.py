from polyTritimus import PolyalphabeticTrithemus
from alphabet import text2array, array2text, add_txt, sub_txt
def core_Tritimus (in_prime: str, in_aux: str) -> str:
    out = 'Ошибка ввода'
    if len(in_prime)==16 & len(in_aux)==16:
        cipher = PolyalphabeticTrithemus(in_prime)  # ключ — in_prime
        out = cipher.encrypt(in_aux)
    return out

#in1 = 'хорошо_быть_вами'
#in2 = 'кьеркегор_пропал'
#print (core_Tritimus(in1,in2))

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

IN = 'хорошо_быть_вами'
IN1 = 'кьеркегор_пропал'
IN2 = 'хорошо_пробросил'
# print(confuse(IN, IN1))

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
in_arr = ['ток', 'сок', 'мак', 'пар']
# print(mixinputs(in_arr))


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

# print(compress(IN,4))

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

in_arr1 = ['ХОРОШО_БЫТЬ_ВАМИ']
in_arr2 = ['ХОРОШО_БЫТЬ_ВАМИ',
       '________________',
       '________________',
       '________________']

# print(c_block(in_arr1, 16))
