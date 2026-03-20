def frw_P_scitala(block: str) -> str:
    q = int(len(block) / 2)
    f = len(block) % 2
    tmpA = block[: q + f]
    tmpB = block[q + f:]
    out = ''
    for i in range(q):
        if i % 2 == 0:
            out = out + tmpA[i: i + 1]
            out = out + tmpB[i: i + 1]
        else:
            out = out + tmpB[i: i + 1]
            out = out + tmpA[i: i + 1]
    if f == 1:
        out = out + tmpA[q: q + 1]
    return out

# print(frw_P_scitala('ДЖИГУРДА'), frw_P_scitala('ДЖИГУРДАЯ'))

def inv_P_scitala(block: str) -> str:
    q = len(block) // 2
    f = len(block) % 2
    tmpA = ''
    tmpB = ''

    for i in range(q):  # i от 0 до q-1
        if i % 2 == 0:
            tmpA = tmpA + block[2 * i]
            tmpB = tmpB + block[2 * i + 1]  #
        else:
            tmpB = tmpB + block[2 * i]
            tmpA = tmpA + block[2 * i + 1]

    if f == 1:
        tmpA = tmpA + block[2 * q]

    out = tmpA + tmpB
    return out

#print(inv_P_scitala('ДУРЖИДАГ'))
