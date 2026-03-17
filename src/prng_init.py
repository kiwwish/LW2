from functions import c_block
from alphabet import add_txt
from lcg_utils import seed2num


def initialize_PRNG(Seed_in: str) -> list:

    Const = [
        "ПЕРВОЕ_АКТЕРСТВО",
        "ВТОРОЙ_ДАЛЬТОНИК",
        "ТРЕТЬЯ_САДОВНИЦА",
        "ЧЕТВЕРТЫЙ_ГОБЛИН"
    ]

    OUT = []
    value = []

    for i in range(4):

        const = Const[i]

        value_i = c_block([const, Seed_in], 16)

        value.append(value_i)

    secret = c_block(value, 16)

    for i in range(4):

        tmp = value[i]

        TMP = ""

        for j in range(4):

            tmp = add_txt(tmp, Const[i])

            TMP = TMP + c_block([tmp, secret], 4)

            tmp = add_txt(tmp, TMP)

        out_i = TMP[4:16]

        OUT.append(out_i)

    return OUT