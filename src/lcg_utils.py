from alphabet import text2array, array2text


def block2num(BLOCK_IN: str) -> int:
    if len(BLOCK_IN) != 4:
        return "input_error"

    tmp = text2array(BLOCK_IN)

    out = 0
    pos = 1

    for i in range(3, -1, -1):
        out = pos * tmp[i] + out
        pos = 32 * pos

    return out


def num2block(num_in: int) -> str:
    rem = num_in

    tmp = [0] * 4

    for i in range(4):
        tmp[3 - i] = rem % 32
        rem = rem // 32

    return array2text(tmp)


def dec2bin(num_in: int) -> list[int]:
    rem = num_in
    out = [0] * 20

    for i in range(20):
        out[19 - i] = rem % 2
        rem = rem // 2

    return out


def bin2dec(BIN_IN: list[int]) -> int:
    out = 0

    for i in range(20):
        out = 2 * out + BIN_IN[i]

    return out


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


def seed2num(array_in: list) -> list:

    out = []

    for i in range(3):
        out_i = block2num(array_in[i])
        out.append(out_i)

    return out