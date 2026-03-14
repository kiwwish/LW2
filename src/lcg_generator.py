from lcg_utils import block2num, num2block, compose_num


class LCGGenerator:
    def __init__(self, seed_str: str, COEFS_IN: tuple[int, int, int]):
        """
        :param seed_str: Начальное состояние (4 символа)
        :param COEFS_IN: Вектор коэффициентов [a, c, m] (как в Mathcad)
        """
        if len(COEFS_IN) != 3:
            raise ValueError("Коэффициенты должны быть кортежем из 3 чисел: (a, c, m)")

        self.COEF = COEFS_IN

        self.state = block2num(seed_str)

    def generate(self) -> tuple[str, str]:
        # Распаковка вектора внутри метода
        a, c, m = self.COEF

        # Формула: out = mod(a * state_in + c, m)
        next_val = (a * self.state + c) % m
        self.state = next_val

        new_state_str = num2block(next_val)
        outflow_str = new_state_str

        return new_state_str, outflow_str


