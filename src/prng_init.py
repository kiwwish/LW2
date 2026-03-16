from functions import c_block, add_txt


def initialize_PRNG(Seed_IN: str, CIPHER_CORE):

    Const = [
        "ПЕРВОЕ_АКТЕРСТВО",
        "ВТОРОЙ_ДАЛЬТОНИК",
        "ТРЕТЬЯ_САДОВНИЦА",
        "ЧЕТВЕРТЫЙ_ГОБЛИН"
    ]

    OUT = []

    # 1. вычисляем Value[i]
    values = []

    for i in range(4):

        value_i = CIPHER_CORE([Const[i], Seed_IN], 16)

        if len(value_i) != 16 or "Ошибка" in value_i:
            return ["Ошибка"] * 4

        values.append(value_i)

    # 2. Secret
    secret = CIPHER_CORE(values, 16)

    if len(secret) != 16 or "Ошибка" in secret:
        return ["Ошибка"] * 4

    # 3. основной цикл
    for i in range(4):

        tmp = values[i]
        TMP = ""

        for j in range(4):

            tmp = add_txt(tmp, Const[i])

            block_out = CIPHER_CORE([tmp, secret], 4)

            if len(block_out) != 4 or "Ошибка" in block_out:
                return ["Ошибка"] * 4

            TMP += block_out

            tmp = add_txt(tmp, TMP)

        out_i = TMP[4:16]

        if len(out_i) != 12:
            print(f"[WARNING] i={i}: длина out_i = {len(out_i)}")

        OUT.append(out_i)

    return OUT