# polyalphabetic.py
from alphabet import sym2num, num2sym, text2array


def Thrithemus_table(KEY_IN: str) -> str:
    """Та же функция из trithemus.py"""
    out = ""
    A = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ_"
    for i in range(len(KEY_IN)):
        tmp = KEY_IN[i]
        while tmp in out:
            tmp_num = sym2num(tmp)
            tmp = num2sym((tmp_num + 1) % 32)
        if len(out) < 32:
            out += tmp

    for ch in A:
        if ch not in out:
            out += ch

    return out


def frw_Trithemus_char(ch: str, table: str) -> str:
    """Шифрование одного символа (сдвиг на 8)"""
    pos = table.find(ch)
    if pos == -1:
        return ch
    new_pos = (pos + 8) % 32
    return table[new_pos]


def inv_Trithemus_char(ch: str, table: str) -> str:
    """Дешифрование одного символа (сдвиг на -8)"""
    pos = table.find(ch)
    if pos == -1:
        return ch
    new_pos = (pos - 8) % 32
    return table[new_pos]


def shift_Trithemus(TABLE_IN: str, sym_in: str, bias_in: int) -> str:
    """Сдвиг таблицы"""
    s = sym_in
    str_part = TABLE_IN[bias_in:]  # часть с bias_in до конца
    rem = TABLE_IN[:bias_in]  # часть с начала до bias_in

    # Если символ уже в rem, сдвигаем пока не найдём свободный
    while s in rem:
        s_num = sym2num(s)
        s = num2sym((s_num + 1) % 32)

    # Находим и удаляем s из str_part
    x = str_part.find(s)
    if x == -1:
        # Если символ не найден (теоретически не должно быть)
        return TABLE_IN

    # Удаляем символ s из str_part
    str_part = str_part[:x] + str_part[x + 1:]

    # Новая таблица: s + rem + str_part
    return s + rem + str_part


class PolyalphabeticTrithemus:
    """Класс для полиалфавитного шифра Тритемуса"""

    def __init__(self, key: str):
        self.key = key.upper()
        self.key_array = text2array(self.key)

    def encrypt(self, text: str) -> str:
        """Шифрование текста"""
        out = ""
        text = text.upper()
        key_table = Thrithemus_table(self.key)

        for i in range(len(text)):
            k = i % len(self.key)
            b = (len(self.key) + i) % 32
            ch = text[i]

            # Шифруем символ
            csym = frw_Trithemus_char(ch, key_table)
            out += csym

            # Сдвигаем таблицу
            key_table = shift_Trithemus(key_table, num2sym(self.key_array[k]), b)

        return out

    def decrypt(self, cipher: str) -> str:
        """Дешифрование текста"""
        out = ""
        cipher = cipher.upper()
        key_table = Thrithemus_table(self.key)

        for i in range(len(cipher)):
            k = i % len(self.key)
            b = (len(self.key) + i) % 32
            ch = cipher[i]

            # Дешифруем символ
            psym = inv_Trithemus_char(ch, key_table)
            out += psym

            # Сдвигаем таблицу (так же как при шифровании!)
            key_table = shift_Trithemus(key_table, num2sym(self.key_array[k]), b)

        return out


# В конец polyalphabetic.py добавить:

class STrithemus:
    """Класс для S-блоков шифра Тритемуса"""

    @staticmethod
    def encrypt_block(block: str, key: str) -> str:
        """Шифрование одного блока (4 символа)"""
        if len(block) != 4:
            return "input_error"
        if len(key) != 16:
            return "input_error"

        # Используем полиалфавитный шифр
        cipher = PolyalphabeticTrithemus(key)
        return cipher.encrypt(block)

    @staticmethod
    def decrypt_block(block: str, key: str) -> str:
        """Дешифрование одного блока (4 символа)"""
        if len(block) != 4:
            return "input_error"
        if len(key) != 16:
            return "input_error"

        # Используем полиалфавитный шифр
        cipher = PolyalphabeticTrithemus(key)
        return cipher.decrypt(block)