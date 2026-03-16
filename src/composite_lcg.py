# src/composite_lcg.py
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from lcg_utils import block2num, num2block
from ct_lcg import CTLCG
from prng_init import initialize_PRNG
from functions import c_block

# Глобальное состояние генератора (как init_flag/state в методичке)
_global_generators = []
_global_initialized = False


def composite_lcg_next(seed_in=None):
    """
    Реализация C_CT_LCG_next строго по формуле из методички.

    Вход:
        seed_in – строка из 16 символов (для инициализации)
        либо "" / None для продолжения генерации

    Выход:
        [stream, state]
    """

    global _global_generators, _global_initialized

    stream = ""
    check = 0

    # -------------------------------------------------
    # БЛОК 1 — INIT
    # -------------------------------------------------

    if seed_in is not None and len(seed_in) == 16:

        INIT = initialize_PRNG(seed_in, c_block)

        _global_generators = []

        for i in range(4):

            seed_str = INIT[i]

            # параметры генераторов (слайд 43)
            if i == 0:
                params = [
                    (252564, 9109, 961193),
                    (252564, 9109, 961193),
                    (723482, 8677, 983609)
                ]

            elif i == 1:
                params = [
                    (51190, 7927, 990711),
                    (51190, 7927, 990711),
                    (549234, 6949, 939683)
                ]

            elif i == 2:
                params = [
                    (227796, 5107, 981875),
                    (227796, 5107, 981875),
                    (167490, 9871, 809137)
                ]

            else:
                params = [
                    (357630, 8971, 948209),
                    (357630, 8971, 948209),
                    (73335, 6779, 1014784)
                ]

            gen = CTLCG(seed_str, params)
            _global_generators.append(gen)

        _global_initialized = True
        check = 1

    elif seed_in is None or seed_in == "":

        if not _global_initialized:
            return ["input_error", None]

        check = 1

    else:
        return ["input_error", None]

    # -------------------------------------------------
    # БЛОК 2 — ОСНОВНАЯ ГЕНЕРАЦИЯ
    # -------------------------------------------------

    if check == 1:

        for j in range(4):

            tmp = 0
            sign = 1

            for i in range(4):

                new_state, out_val = _global_generators[i].generate()

                # T0 из формулы
                if isinstance(out_val, str):
                    value = block2num(out_val)
                else:
                    value = out_val

                tmp = (1048576 + sign * value + tmp) % 1048576

                sign = -sign

            block_str = num2block(tmp)

            stream += block_str

        # по формуле: out ← [stream, state]
        return [stream, _global_generators]

    return ["something_wrong", None]


# -------------------------------------------------
# ТЕСТ
# -------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("ТЕСТ ПО МЕТОДИЧКЕ")
    print("=" * 60)

    seed = "АБВГДЕЖЗИЙКЛМНОП"
    expected = "_Н_БОДП_ЮЦЛИУЯИ"

    res1 = composite_lcg_next(seed)[0]

    print("\nШаг 1:")
    print("Получено :", res1)
    print("Ожидалось:", expected)

    if res1 == expected:
        print("✅ Совпадает")
    else:
        print("❌ Не совпадает")

    res2 = composite_lcg_next("")[0]
    print("\nШаг 2:", res2)

    res3 = composite_lcg_next("")[0]
    print("Шаг 3:", res3)