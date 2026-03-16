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
    Реализация строго по формуле C_CT_LCG_next из приложения (слайд 41).
    """

    # Наборы коэффициентов ИЗ ПРИЛОЖЕНИЯ (слайд 43)
    SETS = [
        # set1
        [(252564, 9109, 961193), (252564, 9109, 961193), (723482, 8677, 983609)],
        # set2
        [(51190, 7927, 990711), (51190, 7927, 990711), (549234, 6949, 939683)],
        # set3
        [(227796, 5107, 981875), (227796, 5107, 981875), (167490, 9871, 809137)],
        # set4
        [(357630, 8971, 948209), (357630, 8971, 948209), (73335, 6779, 1014784)]
    ]

    def __init__(self, cipher_core):
        self.cipher_core = cipher_core
        self.generators = []
        self.initialized = False

    def generate(self, input_data: str = "") -> str:
        """
        Реализация C_CT_LCG_next по формуле со слайда 41.
        Каждый вызов возвращает 16 символов (4 блока по 4 символа).
        """
        if not self.initialized:
            if len(input_data) != 16:
                raise ValueError("Первый вызов требует seed из 16 символов")

            print("[Init] Запуск инициализации...")
            init_data = initialize_PRNG(input_data, self.cipher_core)

            for i, seed in enumerate(init_data):
                if len(seed) != 12:
                    raise ValueError(f"Сид {i} имеет длину {len(seed)}, ожидалось 12")
                self.generators.append(CTLCG(seed, self.SETS[i]))

            self.initialized = True
            return self.generate("")  # сразу первый полезный блок

        # ─── Основной цикл: 4 блока по 4 символа ─────────────────────────────
        stream = ""
        MOD = 1048576

        for block_idx in range(4):

            tmp = 0
            sign = 1

            for gen_idx, gen in enumerate(self.generators):

                state, out = gen.generate()

                if isinstance(out, str):
                    value = block2num(out)
                else:
                    value = out

                tmp = (tmp + sign * value) % MOD
                sign = -sign

            block = num2block(tmp)

            stream += block

        return stream


if __name__ == "__main__":
    from functions import c_block

    print("--- Тест интерфейса CompositeLCG ---")

    comp = CompositeLCG(c_block)
    seed = "АБВГДЕЖЗИЙКЛМНОП"

    res1 = comp.generate(seed)
    print(f"Step 1 (Init) : {res1}")

    res2 = comp.generate("")
    print(f"Step 2 : {res2}")

    res3 = comp.generate("")
    print(f"Step 3 : {res3}")