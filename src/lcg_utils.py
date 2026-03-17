from alphabet import text2array, array2text

from alphabet import text2array, array2text


def block2num(BLOCK_IN: str) -> int:
    """
    Реализация строго по Mathcad:
    Цикл for i from 3 down to 0.
    """
    if len(BLOCK_IN) != 4:
        return "input_error"  # Как в методичке

    tmp = text2array(BLOCK_IN)
    out = 0
    pos = 1

    # В методичке: for i in 3, 2 .. 0
    for i in range(3, -1, -1):
        out = pos * tmp[i] + out
        pos = 32 * pos

    return out


def num2block(num_in: int) -> str:
    """
    Реализация строго по Mathcad:
    Запись в tmp[3-i].
    """
    rem = num_in
    tmp = [0] * 4

    # В методичке: for i in 0, 1 .. 3
    for i in range(4):
        tmp[3 - i] = rem % 32
        rem = rem // 32  # аналог trunc(num/den)

    return array2text(tmp)


# Тесты из методички
if __name__ == "__main__":
    test_cases = [
        ("АБВГ", 34916),
        ("_ЯЗЬ", 32028),
        ("ЯЯЯЯ", 1048575)
    ]

    print("--- ТЕСТИРОВАНИЕ ПО МЕТОДИЧКЕ ---")
    for block_str, expected_num in test_cases:
        res_num = block2num(block_str)
        res_block = num2block(expected_num)

        print(f"Блок: {block_str} -> Число: {res_num} (Ожидалось: {expected_num})")
        print(f"Число: {expected_num} -> Блок: {res_block} (Ожидалось: {block_str})")
        print("-" * 30)


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
        out[19-i] = rem % 2
        rem = rem // 2

    return out
#print(dec2bin(34916))

def bin2dec(BIN_IN: list[int]) -> int:
    """
    Преобразует массив из 20 битов в число.
    ВАЖНО: Индекс 0 — это МЛАДШИЙ бит (2^0).
    """
    out = 0
    for i in range(20):
        out = 2 * out + BIN_IN[i]

    return out


#print(bin2dec([0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0]))
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
#print(compose_num(1231,723482,448033))

def seed2nums(ARRAY_IN: list[str]) -> list[int]:
    """Преобразование массива строк в массив чисел. Слайд 'seed2nums'."""
    out = [0] * len(ARRAY_IN)
    for i in range(len(ARRAY_IN)):
        out[i] = block2num(ARRAY_IN[i])
    return out
#print(seed2nums(["АПЧХ","ЧПОК","ШУРА"]))