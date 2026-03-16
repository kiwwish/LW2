import sys
import os

# Добавляем папку src в путь поиска модулей
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_dir)

# --- ТЕСТИРОВАНИЕ ---
from lcg_generator import LCGGenerator
from ct_lcg import CTLCG
from composite_lcg import CompositeLCG
from functions import c_block
from alphabet import verify_alphabet


def test_lcg():
    print("\n--- Тест базового LCG ---")

    # Коэффициенты строго по методичке (слайд 38)
    COEFS_IN = (357630, 8971, 948209)

    try:
        lcg = LCGGenerator("ЛУЛУ", COEFS_IN)
        print(f"Seed: ЛУЛУ, Coeffs: {COEFS_IN}")

        for i in range(10):
            st, of = lcg.generate()
            print(f"Step {i + 1}: State={st}, Outflow={of}")

    except Exception as e:
        print(f"Ошибка в LCG: {e}")


def test_ct_lcg():
    print("\n--- Тест CT-LCG (по Mathcad) ---")

    # Seed должен быть ровно 12 символов
    seed = "АПЧХЧПОКШУРА"

    # Наборы коэффициентов (как в классе CTLCG или CompositeLCG)
    sets = [
        (723482, 8677, 983609),  # set0
        (252564, 9109, 961193),  # set1
        (357630, 8971, 948209)  # set2
    ]

    try:
        # Передаем оба аргумента: seed и sets
        ct_lcg = CTLCG(seed, sets)
        print(f"Seed: {seed} (длина: {len(seed)})")

        for i in range(10):
            st, of = ct_lcg.generate()
            print(f"Step {i + 1}: State={st}, Outflow={of}")

            if len(st) != 12 or len(of) != 4:
                print(f"  Внимание: Длина State={len(st)}, Outflow={len(of)}")

    except Exception as e:
        print(f"Ошибка: {e}")


def test_composite():
    print("\n--- Тест Композиционного генератора (C-CT-LCG) ---")

    seed = "АБВГДЕЖЗИЙКЛМНОП"

    try:
        # 1. Создаем объект ТОЛЬКО с функцией шифрования
        composite = CompositeLCG(c_block)
        print(f"Seed: {seed}")

        # 2. Первый шаг: ИНИЦИАЛИЗАЦИЯ (передаем seed)
        res1 = composite.generate(seed)
        print(f"Step 1 (Init):     Output={res1} (длина={len(res1)})")

        if len(res1) != 16:
            print(f"  Ошибка: Длина вывода должна быть 16, получено {len(res1)}")

        # 3. Следующие шаги: ПРОДОЛЖЕНИЕ (передаем пустую строку)
        for i in range(4):
            res = composite.generate("")
            step_num = i + 2
            print(f"Step {step_num}:   Output={res} (длина={len(res)})")

            if len(res) != 16:
                print(f"  Ошибка: Длина вывода должна быть 16, получено {len(res)}")

    except Exception as e:
        print(f"Ошибка: {e}")


def test_final_check_mathcad():
    """
    Финальная проверка: Сравнение результата работы Композиционного генератора
    с точными данными из методички (слайд 42).

    Вход: seed = "АБВГДЕЖЗИЙКЛМНОП"
    Ожидаемый первый выход (out_0) для Tritemus: "_Н_БОДП_ЮЦЛИУЯИ"
    """
    print("\n" + "=" * 60)
    print("ФИНАЛЬНАЯ ПРОВЕРКА ПО ДАННЫМ МЕТОДИЧКИ (СЛАЙД 42)")
    print("=" * 60)

    from composite_lcg import CompositeLCG
    from functions import c_block

    # Входные данные из методички
    seed_mathcad = "АБВГДЕЖЗИЙКЛМНОП"
    expected_out_trithemus = "_Н_БОДП_ЮЦЛИУЯИ"

    try:
        # 1. Создаем объект ТОЛЬКО с функцией шифрования
        gen = CompositeLCG(c_block)

        # 2. Генерируем первую последовательность (ИНИЦИАЛИЗАЦИЯ)
        result = gen.generate(seed_mathcad)

        print(f"\n📝 Входной seed: {seed_mathcad}")
        print(f"✅ Ваш результат (1-й блок): {result}")
        print(f"🎯 Результат из Mathcad:      {expected_out_trithemus}")

        if result == expected_out_trithemus:
            print("\n🎉 УСПЕХ! Результат полностью совпадает с методичкой.")
            print("Ваша лабораторная работа выполнена корректно!")
        else:
            print("\n⚠️ Внимание: Результаты не совпадают.")
            print("Возможные причины:")
            print("  1. В функции initialize_PRNG есть нюанс (например, порядок битов).")
            print("  2. В классе CompositeLCG используется другой набор коэффициентов SET.")
            print("  3. В функции compose_num логика склейки отличается.")

    except Exception as e:
        print(f"\n❌ Критическая ошибка при запуске: {e}")
        import traceback
        traceback.print_exc()


# main.py

def test_prng_examples_trithemus():

    from prng_init import initialize_PRNG
    from functions import c_block

    print("\n" + "=" * 60)
    print("ТЕСТ ПРИМЕРОВ ИЗ МЕТОДИЧКИ (core_Tritemus)")
    print("=" * 60)

    IN1 = "ХОРОШО_БЫТЬ_ВАМИ"
    IN2 = "________________"
    IN3 = "ХОРОШО_ВЫТЬ_ВАМИ"
    IN4 = "___А____________"

    seeds = [IN1, IN2, IN3, IN4]

    for seed in seeds:

        print(f"\n--- Seed: '{seed}' ---")

        result = initialize_PRNG(seed, c_block)

        print("Полученный результат:")

        for line in result:
            print(line)


def test_c_block_examples_final():
    from functions import c_block, core_Tritimus

    # Точные примеры из методички (слайд с IN1...IN9)

    # IN1
    inp_IN1 = ("ХОРОШО_БЫТЬ_ВАМИ",)
    exp_IN1_16 = "ОВПВР_ЗШЛНУИНПЮД"
    exp_IN1_8 = "_ВЧЬЩЮСН"

    # IN2
    inp_IN2 = ("ХОРОШО_БЫТЬ_ВАМИ", "________________", "________________", "________________")
    exp_IN2_16 = "ОВПВР_ЗШЛНУИНПЮД"
    exp_IN2_8 = "_ВЧЬЩЮСН"

    # IN3
    inp_IN3 = ("ХОРОШО_БЫТЬ_ВАМИ", "________А_______")
    exp_IN3_16 = "О_ТСР_ПКЬНГФНТХА"
    exp_IN3_8 = "__ВЭЙАЩХ"

    # IN4
    inp_IN4 = ("ХОРОШО_БЫТЬ_ВАМИ", "___А____________")
    exp_IN4_16 = "ЧИШФЮ_АНЬОУЬОШЦД"
    exp_IN4_8 = "ХИЩВКЗКА"

    # IN5
    inp_IN5 = ("ХОРОШО_БЫТЬ_ВАМИ", "КЬЕРКЕГОР_ПРОПАЛ")
    exp_IN5_16 = "ШЦЗЫБЖЩСЧПСЙЕУО"
    exp_IN5_8 = "ФСБМБЕГА"

    # IN6
    inp_IN6 = ("ЧЕРНЫЙ_АББАТ_ПОЛ", "ХОРОШО_БЫТЬ_ВАМИ", "КЬЕРКЕГОР_ПРОПАЛ")
    exp_IN6_16 = "ЙЖЭБИЛЖЬВЙЦГБУЖ"
    exp_IN6_8 = "ТТГЮЖБЮЮ"

    # IN7
    inp_IN7 = ("__A___________", "________________", "________________", "________________")
    exp_IN7_16 = "ОРСЗДЫЖШАЭХЛФИЖР"
    exp_IN7_8 = "УЛШАУЕЭЭ"

    # IN8
    inp_IN8 = ("________________", "________________", "________________", "________________")
    exp_IN8_16 = "РЗФВЛЫУЩ_ЯХМДЙЧР"
    exp_IN8_8 = "ЭВИЭДИНЮ"

    # IN9
    inp_IN9 = ("__A___________--", "________________", "__A_____________", "________________")
    exp_IN9_16 = "ЦШЮЬЗЩШТЯБХЦЛЖЮЮ"
    exp_IN9_8 = "ЯТЦОКИУФ"

    print("\n--- ФИНАЛЬНЫЙ ТЕСТ ФУНКЦИИ C_BLOCK (по методичке) ---\n")

    all_passed = True

    tests = [
        ("IN1", inp_IN1, exp_IN1_16, exp_IN1_8),
        ("IN2", inp_IN2, exp_IN2_16, exp_IN2_8),
        ("IN3", inp_IN3, exp_IN3_16, exp_IN3_8),
        ("IN4", inp_IN4, exp_IN4_16, exp_IN4_8),
        ("IN5", inp_IN5, exp_IN5_16, exp_IN5_8),
        ("IN6", inp_IN6, exp_IN6_16, exp_IN6_8),
        ("IN7", inp_IN7, exp_IN7_16, exp_IN7_8),
        ("IN8", inp_IN8, exp_IN8_16, exp_IN8_8),
        ("IN9", inp_IN9, exp_IN9_16, exp_IN9_8),
    ]

    for name, inp, exp_16, exp_8 in tests:
        inp_list = list(inp)

        result_16 = c_block(inp_list, 16)
        match_16 = result_16 == exp_16

        result_8 = c_block(inp_list, 8)
        match_8 = result_8 == exp_8

        status_16 = "✅" if match_16 else "❌"
        status_8 = "✅" if match_8 else "❌"

        print(f"{name}:")
        print(f"  Expected (16): {exp_16} | Got:      {result_16} | {status_16}")
        print(f"  Expected (8):  {exp_8}    Got:      {result_8}  | {status_8}")

        if not (match_16 and match_8):
            all_passed = False

        print("-" * 60)

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Функция c_block работает идеально.")
    else:
        print("⚠️ ОБНАРУЖЕНЫ РАЗЛИЧИЯ. Проверьте логику add_txt или mixinputs.")
    print("=" * 60)


# Вызов теста

if __name__ == "__main__":
    # Запускаем все тесты последовательно
    if not verify_alphabet():
        print("Ошибка проверки алфавита!")
    else:
       #test_lcg()
       #test_ct_lcg()
       #test_composite()
       # test_final_check_mathcad()

      test_prng_examples_trithemus()

    input("\nНажмите Enter для выхода...")