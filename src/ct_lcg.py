from prng_init import initialize_PRNG
from lcg_generator import ct_lcg_next
from lcg_utils import seed2num, num2block


def c_ct_lcg_next(flag: str, STATE, SEED, SET: list):
    out = 'something_wrong'
    stream = ''
    check = 0
    if flag == 'up':
        init = initialize_PRNG(SEED)
        state = []
        for i in range(4):
            state_i = seed2num([init[i][0:4], init[i][4:8], init[i][8:12]])
            state.append(state_i)
            check = 1
    elif flag == 'down':
        state = STATE
        check = 1
    if check == 1:
        for j in range(4):
            tmp = 0
            sign = 1
            for i in range(4):
                T = ct_lcg_next(state[i], SET[j])
                state[i] = T[1]
                tmp = (1048576 + sign * T[0] + tmp) % 1048576
                sign = 0 - sign
            stream = stream + num2block(tmp)
        out = [stream, state]
    return out

def produce_round_keys(key: str, num: int, set: list) -> list:
    result = c_ct_lcg_next("up", -1, key, set)
    all_outputs = []
    all_outputs.append(result[0])
    current_state = result[1]
    if num > 1:
        for i in range(num-1):
            result = c_ct_lcg_next("down", current_state, -1, set)
            all_outputs.append(result[0])
            current_state = result[1]
    return all_outputs


