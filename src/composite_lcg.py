# src/composite_lcg.py
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from lcg_utils import block2num, num2block
from ct_lcg import CTLCG
from prng_init import initialize_PRNG


class CompositeLCG:
    """
    Обёртка над 4 CT-LCG генераторами.
    Интерфейс: generate(input_data) -> str (16 символов).
    """

    # Наборы коэффициентов ИЗ СЛАЙДА 42 (таблица CHCLCG_set)
    # set0, set1, set2
    SETS = [
        # set0
        [(723482, 8677, 983609), (252564, 9109, 961193), (357630, 8971, 948209)],
        # set1
        [(51190, 7927, 990711), (51190, 7927, 990711), (549234, 6949, 939683)],
        # set2
        [(227796, 5107, 981875), (227796, 5107, 981875), (167490, 9871, 809137)],
        # set0 снова (для 4-го генератора)
        [(723482, 8677, 983609), (252564, 9109, 961193), (357630, 8971, 948209)]
    ]

    def __init__(self, cipher_core):
        self.cipher_core = cipher_core
        self.generators = []
        self.initialized = False

    def generate(self, input_data: str = "") -> str:
        """
        :param input_data: Seed (16 символов) для инициализации ИЛИ пустая строка "" для продолжения.
        :return: Строка из 16 символов (80 бит).
        """

        # --- РЕЖИМ "UP": ИНИЦИАЛИЗАЦИЯ ---
        if not self.initialized and len(input_data) == 16:
            print(f"[Init] Запуск инициализации...")

            init_data = initialize_PRNG(input_data, self.cipher_core)

            for i in range(4):
                params = self.SETS[i]
                self.generators.append(CTLCG(init_data[i], params))

            self.initialized = True

        elif not self.initialized:
            raise ValueError("Для первого вызова необходимо передать seed из 16 символов.")

        # --- РЕЖИМ "DOWN": ПРОДОЛЖЕНИЕ (Простая конкатенация) ---
        stream = ""

        for gen in self.generators:
            st, of = gen.generate()
            stream += of

        return stream


if __name__ == "__main__":
    from functions import c_block

    print("--- Тест интерфейса CompositeLCG ---")

    comp = CompositeLCG(c_block)
    seed = "АБВГДЕЖЗИЙКЛМНОП"

    res1 = comp.generate(seed)
    print(f"Step 1 (Init): {res1}")

    res2 = comp.generate("")
    print(f"Step 2 (Cont): {res2}")