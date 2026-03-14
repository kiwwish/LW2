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


if __name__ == "__main__":
    # Запускаем все тесты последовательно
    if not verify_alphabet():
        print("Ошибка проверки алфавита!")
    else:
        test_lcg()
        test_ct_lcg()
        test_composite()
        test_final_check_mathcad()

    input("\nНажмите Enter для выхода...")