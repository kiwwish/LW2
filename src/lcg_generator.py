from lcg_utils import compose_num


def make_coeffs(bpr_in: list, spr_in: list, pow_in: int):

    ss = min(spr_in)
    bs = min(bpr_in)
    bb = max(bpr_in)
    sb = max(spr_in)

    MAX = 2 ** (pow_in) - 1

    tmp = bs * ss

    a = ss * bs * sb + 1
    c = bb

    for i in range(pow_in):

        if tmp * ss >= MAX:
            break

        else:
            tmp = tmp * ss

    m = tmp

    if (a < m) and (c < m):
        out = [a, c, m]

    else:
        out = 'wrong_guess'

    return out


def lcg_next(state_in: int, coefs_in: list):

    a = coefs_in[0]
    c = coefs_in[1]
    m = coefs_in[2]

    out = (a * state_in + c) % m

    return out


def ct_lcg_next(sate_in: list, set_in: list):

    first = lcg_next(sate_in[0], set_in[0])
    second = lcg_next(sate_in[1], set_in[1])
    control = lcg_next(sate_in[2], set_in[2])

    out = compose_num(first, second, control)

    state_out = [first, second, control]

    return [out, state_out]