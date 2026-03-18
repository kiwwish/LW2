import sys
import os
import math
import matplotlib.pyplot as plt

try:
    import matplotlib
    matplotlib.use('TkAgg') 
except:
    pass

# Добавляем src в путь
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_dir)

try:
    from lcg_generator import LCGGenerator
    HAS_CLASS = True
except ImportError:
    from lcg_generator import lcg_next
    HAS_CLASS = False

from lcg_utils import dec2bin, block2num, num2block

# Параметры теста

REPLICATIONS = 200
BITS_PER_REP = 4000

# Коэффициенты: можно использовать кортеж или список
# Вариант 1: Из методички (SET₀) — для сдачи лабы
#LCG_COEFS = [723482, 8677, 983609]

# Вариант 2: Оптимальные для 20 бит — для качества
LCG_COEFS = [524269, 1, 1048576]

LCG_SEED = "ЛУЛУ"           # Для класса (строка)
LCG_SEED_NUM = 12345        # Для функций (число)

# Получение битов: версия для класса

def get_bits_from_lcg_class(lcg, count: int) -> list[int]:
    """Генерация битов через класс LCGGenerator"""
    bits = []
    while len(bits) < count:
        _, outflow = lcg.generate()
        num = block2num(outflow)
        block_bits = dec2bin(num) 
        bits.extend(block_bits)
    return bits[:count]

# Получение битов: версия для функций
def get_bits_from_lcg_func(state: int, coefs: list, count: int) -> tuple[list[int], int]:
    """
    Генерация битов через функцию lcg_next.
    Возвращает: (биты, новое_состояние)
    """
    bits = []
    current_state = state
    while len(bits) < count:
        current_state = lcg_next(current_state, coefs)
        block_bits = dec2bin(current_state)  
        bits.extend(block_bits)
    return bits[:count], current_state

# Тест 1: Частотный монобитный
def frequency_test(sequence: list[int]) -> float:
    n = len(sequence)
    n1 = sum(sequence)
    n0 = n - n1
    p1 = n1 / n
    p0 = n0 / n
    if p1 == 0 or p0 == 0:
        return float('inf')
    s = math.sqrt(n * p1 * p0) / n
    x = abs(p0 - p1) / s
    return x

# Тест 2: Максимальная длина серии единиц
def longest_run_ones(sequence: list[int]) -> int:
    max_run = 0
    cur_run = 0
    for bit in sequence:
        if bit == 1:
            cur_run += 1
            max_run = max(max_run, cur_run)
        else:
            cur_run = 0
    return max_run

# Основной запуск
def main():
    print("=" * 60)
    print("NIST-style тесты для LCG")
    print("=" * 60)
    print(f"   Репликаций: {REPLICATIONS}")
    print(f"   Бит на репликацию: {BITS_PER_REP}")
    print(f"   Режим: {'Класс' if HAS_CLASS else 'Функции'}")
    print(f"   Coefs: {LCG_COEFS}")
    print("=" * 60)
    
    x_stats = []
    m_stats = []
    passed_freq = 0
    passed_run = 0
    
    for rep in range(REPLICATIONS):
        if HAS_CLASS:
            lcg = LCGGenerator(LCG_SEED, tuple(LCG_COEFS))
            skip_bits = rep * BITS_PER_REP
            _ = get_bits_from_lcg_class(lcg, skip_bits)
            seq = get_bits_from_lcg_class(lcg, BITS_PER_REP)
        else:
            state = LCG_SEED_NUM % LCG_COEFS[2]
            skip_bits = rep * BITS_PER_REP
            _, state = get_bits_from_lcg_func(state, LCG_COEFS, skip_bits)
            seq, state = get_bits_from_lcg_func(state, LCG_COEFS, BITS_PER_REP)
        
        # Тест 1
        x = frequency_test(seq)
        x_stats.append(x)
        if x < 3:
            passed_freq += 1
        
        # Тест 2
        m = longest_run_ones(seq)
        m_stats.append(m)
        if 10 <= m <= 15:
            passed_run += 1
        
        if (rep + 1) % 50 == 0:
            print(f"   Обработано: {rep + 1}/{REPLICATIONS}")
    
    # Результаты в терминале
    freq_rate = passed_freq / REPLICATIONS
    run_rate = passed_run / REPLICATIONS
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ")
    print("=" * 60)
    print(f"   Тест 1 (Частотный):     {passed_freq}/{REPLICATIONS} прошло ({freq_rate:.2%})")
    print(f"   Тест 2 (Серии единиц):  {passed_run}/{REPLICATIONS} прошло ({run_rate:.2%})")
    print("=" * 60)
    
    # Статистика по x
    x_min, x_max = min(x_stats), max(x_stats)
    x_avg = sum(x_stats) / len(x_stats)
    print(f"\nСтатистика по тесту 1 (x):")
    print(f"   Мин: {x_min:.4f}, Макс: {x_max:.4f}, Среднее: {x_avg:.4f}")
    print(f"   Критерий: x < 3")
    
    # Статистика по m
    m_min, m_max = min(m_stats), max(m_stats)
    m_avg = sum(m_stats) / len(m_stats)
    print(f"\nСтатистика по тесту 2 (m):")
    print(f"   Мин: {m_min}, Макс: {m_max}, Среднее: {m_avg:.2f}")
    print(f"   Критерий: 10 ≤ m ≤ 15")
    
    # Распределение m
    print(f"\nРаспределение m по значениям:")
    m_counts = {}
    for m in m_stats:
        m_counts[m] = m_counts.get(m, 0) + 1
    for m in sorted(m_counts.keys()):
        bar = "█" * m_counts[m]
        status = "✓" if 10 <= m <= 15 else "✗"
        print(f"   m={m:2d}: {bar} ({m_counts[m]}) {status}")
    
    print("\n" + "=" * 60)
    if freq_rate >= 0.95 and run_rate >= 0.70:
        print("Генератор показывает хорошее качество!")
    else:
        print("Генератор требует улучшения параметров")
    print("=" * 60)
    
    # ==========================================
    # Гистограммы
    # ==========================================
    fig, axs = plt.subplots(1, 2, figsize=(14, 5))
    
    # График 1: Распределение x
    axs[0].hist(x_stats, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
    axs[0].axvline(x=3, color='red', linestyle='--', linewidth=2, label='Критерий: x < 3')
    axs[0].set_title(f'Частотный тест: распределение x\nУспешных: {freq_rate:.2%}')
    axs[0].set_xlabel('Значение статистики x')
    axs[0].set_ylabel('Количество репликаций')
    axs[0].legend()
    axs[0].grid(axis='y', alpha=0.3)
    
    # График 2: Распределение m
    min_m, max_m = min(m_stats), max(m_stats)
    axs[1].hist(m_stats, bins=range(min_m, max_m + 2), 
                color='coral', edgecolor='black', alpha=0.7, align='left')
    axs[1].axvline(x=10, color='green', linestyle='--', linewidth=2, label='Границы [10, 15]')
    axs[1].axvline(x=15, color='green', linestyle='--', linewidth=2)
    axs[1].set_title(f'Тест серий: распределение длины m\nУспешных: {run_rate:.2%}')
    axs[1].set_xlabel('Максимальная длина серии единиц')
    axs[1].set_ylabel('Количество репликаций')
    axs[1].legend()
    axs[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_file = 'lcg_nist_results.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nГрафики сохранены в '{output_file}'")
    plt.show()

if __name__ == "__main__":
    main()