from alphabet import text2array, array2text

def block2num(BLOCK_IN: str) -> int:
    """
    Преобразование блока текста из 4-х символов в целое положительное число.
    :param BLOCK_IN: Строка из 4 символов.
    :return: Целое число (20 бит).
    :raises ValueError: Если длина строки не равна 4.
    """
    # Проверка типа данных и длины
    if not isinstance(BLOCK_IN, str):
        raise ValueError(f"Ожидалась строка, получено: {type(BLOCK_IN)}")

    if len(BLOCK_IN) != 4:
        raise ValueError(f"Ошибка: блок должен содержать ровно 4 символа, получено: {len(BLOCK_IN)}")

    tmp = text2array(BLOCK_IN)
    out = 0
    pos = 1

    for i in range(3, -1, -1):
        out = pos * tmp[i] + out
        pos = 32 * pos

    return out


def num2block(num_in: int) -> str:
    """
    Преобразование целого числа в блок из 4-х символов.
    """
    # Гарантируем диапазон 20 бит
    rem = num_in % (1 << 20)
    tmp = [0] * 4

    # Цикл for i in 0..3
    for i in range(4):
        tmp[3 - i] = rem % 32
        rem = rem // 32

    return array2text(tmp)


# src/lcg_utils.py

# src/lcg_utils.py

def dec2bin(num_in: int) -> list[int]:
    """
    Преобразует число в массив из 20 битов.
    ВАЖНО: Индекс 0 — это МИНУС (младший бит, 2^0), индекс 19 — старший (2^19).
    """
    rem = num_in
    out = [0] * 20

    # Заполняем массив С НАЧАЛА (индекс 0 — младший бит)
    for i in range(20):
        out[i] = rem % 2
        rem = rem // 2

    return out


def bin2dec(BIN_IN: list[int]) -> int:
    """
    Преобразует массив из 20 битов в число.
    ВАЖНО: Индекс 0 — это МЛАДШИЙ бит (2^0).
    """
    out = 0
    for i in range(20):
        # Если индекс 0, умножаем на 2^0, если 19, то на 2^19
        # Формула: out += bit * 2^i
        out += BIN_IN[i] * (2 ** i)

    return out


# src/lcg_utils.py

# src/lcg_utils.py

def compose_num(num1_in: int, num2_in: int, cont_in: int) -> int:
    arr1 = dec2bin(num1_in)
    arr2 = dec2bin(num2_in)
    arr3 = dec2bin(cont_in)

    arr = [0] * 20
    for i in range(20):
        # term1: если control=0 -> first
        term1 = arr2[i] * ((1 + arr3[i]) % 2)
        # term2: если control=1 -> second
        term2 = arr1[i] * arr3[i]
        arr[i] = term1 + term2

    return bin2dec(arr)