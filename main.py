import sys
import os

# Добавляем папку src в путь поиска модулей
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_dir)

from ct_lcg import wrap_ct_clcg_next

# Наборы коэффициентов (из методички)

set1 = []
set10 = [252564, 9109, 961193]
set1.append(set10)
set11 = [252564, 9109, 961193]
set1.append(set11)
set12 = [723482, 8677, 983609]
set1.append(set12)
SET0 = set1

set2 = []
set20 = [51190, 7927, 990711]
set2.append(set20)
set21 = [51190, 7927, 990711]
set2.append(set21)
set22 = [549234, 6949, 939683]
set2.append(set22)
SET1 = set2

set3 = []
set30 = [227796, 5107, 981875]
set3.append(set30)
set31 = [227796, 5107, 981875]
set3.append(set31)
set32 = [167490, 9871, 809137]
set3.append(set32)
SET2 = set3

set4 = []
set40 = [357630, 8971, 948209]
set4.append(set40)
set41 = [357630, 8971, 948209]
set4.append(set41)
set42 = [73335, 6779, 1014784]
set4.append(set42)
SET3 = set4

SET = []
SET.append(SET0)
SET.append(SET1)
SET.append(SET2)
SET.append(SET3)



seed = 'АБВГДЕЖЗИЙКЛМНОП'



# первый запуск генератора
result = wrap_ct_clcg_next("up", -1, seed, SET)

all_outputs = []
all_outputs.append(result[0])

current_state = result[1]


# генерируем ещё 8 блоков
for i in range(8):

    result = wrap_ct_clcg_next("down", current_state, -1, SET)

    all_outputs.append(result[0])

    current_state = result[1]


for i, out_str in enumerate(all_outputs):
    print(f"Step {i+1}: {out_str}")

