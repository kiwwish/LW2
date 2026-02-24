from alphabet import sym2num, num2sym, text2array, array2text

def Thrithemus_table(key: str) -> str:
    """Построение таблицы замены по ключу"""
    out = ""
    A = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ_"
    for i in range(len(key)):
        tmp = key[i]
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
        # Если символ не найден
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


class EnhancedSTrithemus:
    """Модификация S-блоков для шифра Тритимуса """

    @staticmethod
    def _compute_permutation(key_array):
        """Вычисление перестановки M на основе ключа"""
        # Инициализация M = [0, 1, 2, 3]
        M = [0, 1, 2, 3]

        # Вычисление sum по алгоритму
        s = 0
        for i in range(16):
            term = key_array[i]
            if i % 2 == 1:  # если i нечётное, (-1)^i = -1
                term = -term
            s = (24 + s + term) % 24

        # Перемешивание M (k = 0, 1, 2)
        for k in range(3):
            t = s % (4 - k)
            s = s // (4 - k)  # целочисленное деление
            # Обмен M[k] и M[k + t]
            tmp = M[k]
            M[k] = M[k + t]
            M[k + t] = tmp

        return M

    @staticmethod
    def frw_merge_block(block: str, key: str) -> str:
        """Прямое преобразование блока (fwr_merge_block)"""
        if len(block) != 4 or len(key) != 16:
            return "input_error"

        key_array = text2array(key)
        inp = text2array(block)
        M = EnhancedSTrithemus._compute_permutation(key_array)

        # Прямой алгоритм (j = 0..3)
        for j in range(4):
            b = M[(1 + j) % 4]
            a = M[j % 4]
            inp[b] = (inp[b] + inp[a]) % 32

        return array2text(inp)

    @staticmethod
    def inv_merge_block(block: str, key: str) -> str:
        """Обратное преобразование блока (inv_merge_block)"""
        if len(block) != 4 or len(key) != 16:
            return "input_error"

        key_array = text2array(key)
        inp = text2array(block)
        M = EnhancedSTrithemus._compute_permutation(key_array)

        # Обратный алгоритм (j = 3,2,1,0)
        for j in range(3, -1, -1):
            b = M[(1 + j) % 4]
            a = M[j % 4]
            inp[b] = (32 + inp[b] - inp[a]) % 32

        return array2text(inp)

    @staticmethod
    def encrypt_block(block: str, key: str) -> str:
        """Усиленное шифрование блока (frw_S_TrithemusM)"""
        if len(block) != 4 or len(key) != 16:
            return "input_error"

        # 1. inv_merge_block
        tmp1 = EnhancedSTrithemus.inv_merge_block(block, key)
        # 2. frw_S_Trithemus (простой S-блок)
        tmp2 = STrithemus.encrypt_block(tmp1, key)
        # 3. frw_merge_block
        out = EnhancedSTrithemus.frw_merge_block(tmp2, key)

        return out

    @staticmethod
    def decrypt_block(block: str, key: str) -> str:
        """Усиленное дешифрование блока (inv_S_TrithemusM)"""
        if len(block) != 4 or len(key) != 16:
            return "input_error"

        # 1. inv_merge_block
        tmp1 = EnhancedSTrithemus.inv_merge_block(block, key)
        # 2. inv_S_Trithemus (простой S-блок)
        tmp2 = STrithemus.decrypt_block(tmp1, key)
        # 3. frw_merge_block
        out = EnhancedSTrithemus.frw_merge_block(tmp2, key)

        return out
