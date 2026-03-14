# src/ct_lcg.py
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from lcg_utils import block2num, num2block, compose_num
from lcg_generator import LCGGenerator


class CTLCG:
    """
    LCG с манипулируемым усечением (CT-LCG).
    Принимает seed и наборы коэффициентов.
    """

    def __init__(self, seed_str: str, sets: list[tuple[int, int, int]]):
        """
        :param seed_str: Начальное состояние (12 символов: 3 блока по 4)
        :param sets: Список из 3 кортежей (a, c, m) для каждого внутреннего LCG
        """
        if len(seed_str) != 12:
            raise ValueError("Seed должен быть 12 символов (3 блока)")
        if len(sets) != 3:
            raise ValueError("Нужно передать 3 набора коэффициентов")

        s1, s2, s3 = seed_str[0:4], seed_str[4:8], seed_str[8:12]

        # Создаем 3 LCG с переданными параметрами
        self.lcg_first = LCGGenerator(s1, sets[0])
        self.lcg_second = LCGGenerator(s2, sets[1])
        self.lcg_control = LCGGenerator(s3, sets[2])

        # Сохраняем текущие численные состояния
        self.state_first = self.lcg_first.state
        self.state_second = self.lcg_second.state
        self.state_control = self.lcg_control.state

    def generate(self) -> tuple[str, str]:
        _, out_first = self.lcg_first.generate()
        _, out_second = self.lcg_second.generate()
        _, out_control = self.lcg_control.generate()

        self.state_first = block2num(out_first)
        self.state_second = block2num(out_second)
        self.state_control = block2num(out_control)

        composed_num = compose_num(self.state_first, self.state_second, self.state_control)
        outflow_str = num2block(composed_num)

        new_state_str = out_first + out_second + out_control

        return new_state_str, outflow_str

