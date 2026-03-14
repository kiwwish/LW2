from functions import c_block, add_txt


def initialize_PRNG(Seed_IN: str, CIPHER_CORE):
    """
    Инициализация генераторов через С-блок.
    Реализация строго по формуле initialize_PRNG из Mathcad (слайд 37).
    """
    Const = [
        "ПЕРВОЕ_АКТЕРСТВО",
        "ВТОРОЙ_ДАЛЬТОНИК",
        "ТРЕТЬЯ_САДОВНИЦА",
        "ЧЕТВЕРТЫЙ_ГОБЛИН"
    ]

    OUT = []

    for i in range(4):
        # 1. Value_i <- C_block([Const_i, Seed_IN], "16", CIPHER_CORE)
        # ИСПРАВЛЕНО: Сначала Const, потом Seed
        value_i = CIPHER_CORE([Const[i], Seed_IN], 16)

        # 2. Secret <- C_block(Value, "16", CIPHER_CORE)
        secret = CIPHER_CORE(value_i, 16)

        tmp = ""
        TMP = ""

        for j in range(4):
            # 3. tmp <- add_txt(tmp, Const_j)
            tmp = add_txt(tmp, Const[j])

            # 4. TMP <- concat(TMP, C_block([tmp, Secret], "4", CIPHER_CORE))
            block_out = CIPHER_CORE([tmp, secret], 4)
            TMP += block_out

            # 5. tmp <- add_txt(tmp, TMP)
            tmp = add_txt(tmp, TMP)

        # 6. OUT_i <- substr(TMP, 4, 12)
        # ИСПРАВЛЕНО: Индекс 4, длина 12 -> срез [4:16]
        out_i = TMP[4:16]

        OUT.append(out_i)

    return OUT