from MerDam import MerDam_hash
from alphabet import num2sym, add_txt, sym2num
from lcg_utils import dec2bin, block2num, bin2dec, num2block
from feistel_network import frw_Feistel, SET
from ct_lcg import produce_round_keys

def kdf(mat: str, salt: str, con: list[str], size: list[int], iter: int) -> list:
    tmp = mat + salt
    out = []
    for i in range(iter + 1):
        ext = MerDam_hash(tmp)
        tmp = ext + tmp
    prk = tmp
    for i in range(len(size)):
        q = (size[i] - (size[i] % 64)) / 64
        rem = i
        res = ''
        while rem > 0:
            h = rem % 32
            res = res + num2sym(h)
            rem = (rem - h) / 32
        if q > 0:
            hash = prk
            for j in range(q + 1):
                tmp = hash + con[i] + prk
                hash = MerDam_hash(tmp)
                res = hash + res
        else:
            tmp = prk + con[i] + prk
            res = MerDam_hash(tmp)
        out_i = res[0: size[i]]
        out.append(out_i)
    return out

"""
pass1 = 'ЧЕЧЕТКА'
pass2 = 'АПРОЛ'
salt1 = 'СЕАНС'
salt2 = 'АТЛЕТ'
context = ['СЕАНСОВЫЙ_КЛЮЧ', 'КЛЮЧ_РАСПРЕДЕЛЕНИЯ_КЛЮЧЕЙ']
size = [32, 16]

print(kdf(pass1, salt1, context, size, 2))
print(kdf(pass2, salt1, context, size, 2))
"""

def bin2msg(bin: list) -> str:
    B = len(bin)
    b = B // 5
    q = B % 5
    out = ''

    for i in range(b):
        t = 0
        # Читаем биты в том же порядке, как они были записаны
        # В msg2bin биты записываются от младшего к старшему
        for j in range(4, -1, -1):  # Идем с конца блока к началу
            t = t * 2 + bin[i * 5 + j]
        out = out + num2sym(t)

    if q > 0:
        for k in range(q):
            out = out + str(bin[b * 5 + k])

    return out

def sym2bin(s):
    alphabet = '_АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ'
    return alphabet.find(s)

def num2sym(num):
    alphabet = '_АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ'
    if 0 <= num < len(alphabet):
        return alphabet[num]
    return '?'

def isSym(s):
    alphabet = '_АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ'
    return 1 if s in alphabet else -1

def msg2bin(msg) -> list:
    m = len(msg)
    i = 0
    f = 0
    tmp = []

    while i < m and isSym(msg[i]) == 1:
        p = msg[i]
        c = sym2bin(p)
        bits = []
        for j in range(4, -1, -1):
            bit = (c >> j) & 1
            bits.append(bit)
            tmp.append(bit)
        if i == m - 1:
            f = 1
            break
        else:
            i = i + 1
    if f == 0:
        for k in range(i, m):
            p = msg[k]
            if p in '01':
                tmp.append(int(p))
            else:
                c = sym2bin(p)
                for j in range(4, -1, -1):
                    bit = (c >> j) & 1
                    tmp.append(bit)
    return tmp

def bin2msg(bin: list) -> str:
    B = len(bin)
    b = B // 5
    q = B % 5
    out = ''
    for i in range(b):
        t = 0
        for j in range(5):
            bit = bin[i * 5 + j]
            t = 2 * t + bit
        out = out + num2sym(t)
    if q > 0:
        for k in range(q):
            bit = bin[b * 5 + k]
            print(bit, end='')
            out = out + str(bit)
        print()
    return out

"""
test = 'ГНОЛЛЫ_ПИЛИЛИ_ПЫЛЕСОС_ЛОСЕСЕМ'
x = msg2bin(test)
y = bin2msg(x)
print(f'\nОригинал: {test}')
print(f'Результат: {y}')

test_1 = 'ГНОЛЛЫ_ПИЛИЛИ_ПЫЛЕСОС_ЛОСОСЕМ00111'
x1 = msg2bin(test_1)
y1 = bin2msg(x1)
print(f'\nОригинал: {test_1}')
print(f'Результат: {y1}')
"""
INPUTS_ARRAY = ['ГАРРИ_С_ОТКРЫТЫМ_РТОМ_СМОТРЕЛ_НА_СЕМЕЙНОЕ_ХРАНИЛИЩЕ_ТЧК_У_НЕГО_БЫЛО_ТАК_МНОГО_ВОПРОСОВ_ЗПТ_ЧТО_ОН_ДАЖЕ_НЕ_ЗНАЛ_ЗПТ_С_КАКОГО_ИМЕННО_НАЧАТЬ_ТЧК_МАКГОНАГАЛЛ_СТОЯЛА_У_ДВЕРИ_И_НАБЛЮДАЛА_ЗА_МАЛЬЧИКОМ_ТЧК_ОНА_НЕБРЕЖНО_ОПИРАЛАСЬ_О_СТЕНУ_ЗПТ_НО_ВЗГЛЯД_У_НЕЕ_БЫЛ_НАПРЯЖЕННЫЙ_ТЧК_И_НЕСПРОСТА_ТЧК_ОКАЗАТЬСЯ_ПЕРЕД_ОГРОМНОЙ_КУЧЕЙ_ЗОЛОТЫХ_МОНЕТ_ТИРЕ_ТА_ЕЩЕ_ПРОВЕРКА_НА_ПРОЧНОСТЬ_ТЧК_',
                'ИСТОРИЯ_ГАНСА_КАСТОРПА_ЗПТ_КОТОРУЮ_МЫ_ХОТИМ_ЗДЕСЬ_РАССКАЗАТЬ_ЗПТ_ТИРЕ_ОТНЮДЬ_НЕ_РАДИ_НЕГО_ПОСКОЛЬКУ_ЧИТАТЕЛЬ_В_ЕГО_ЛИЦЕ_ПОЗНАКОМИТСЯ_ЛИШЬ_С_САМЫМ_ОБЫКНОВЕННЫМ_ЗПТ_ХОТЯ_И_ПРИЯТНЫМ_МОЛОДЫМ_ЧЕЛОВЕКОМ_ЗПТ_ТИРЕ_ИЗЛАГАЕТСЯ_РАДИ_САМОЙ_ЭТОЙ_ИСТОРИИ_ЗПТ_ИБО_ОНА_КАЖЕТСЯ_НАМ_В_ВЫСОКОЙ_СТЕПЕНИ_ДОСТОЙНОЙ_ОПИСАНИЯ_ПРИЧЕМ_ЗПТ_К_ЧЕСТИ_ГАНСА_КАСТОРПА_ЗПТ_СЛЕДУЕТ_ОТМЕТИТЬ_ЗПТ_ЧТО_ЭТО_ИМЕННО_ЕГО_ИСТОРИЯ_ЗПТ_А_ВЕДЬ_НЕ_С_ЛЮБЫМ_И_КАЖДЫМ_ЧЕЛОВЕКОМ_МОЖЕТ_СЛУЧИТЬСЯ_ИСТОРИЯ_ТЧК_ТАК_ВОТ_ДВТЧ_ЭТА_ИСТОРИЯ_ПРОИЗОШЛА_МНОГО_ВРЕМЕНИ_НАЗАД_ЗПТ_ОНА_ЗПТ_ТАК_СКАЗАТЬ_ЗПТ_УЖЕ_ПОКРЫЛАСЬ_БЛАГОРОДНОЙ_РЖАВЧИНОЙ_СТАРИНЫ_ЗПТ_И_ПОВЕСТВОВАНИЕ_О_НЕЙ_ДОЛЖНО_ЗПТ_РАЗУМЕЕТСЯ_ЗПТ_ВЕСТИСЬ_В_ФОРМАХ_ДАВНО_ПРОШЕДШЕГО_ТЧК_ДЛЯ_ИСТОРИИ_ЭТО_НЕ_ТАКОЙ_УЖ_БОЛЬШОЙ_НЕДОСТАТОК_ЗПТ_СКОРЕЕ_ДАЖЕ_ПРЕИМУЩЕСТВО_ЗПТ_ИБО_ЛЮБАЯ_ИСТОРИЯ_ДОЛЖНА_БЫТЬ_ПРОШЛЫМ_ЗПТ_И_ЧЕМ_БОЛЕЕ_ОНА_ТИРЕ_ПРОШЛОЕ_ЗПТ_ТЕМ_ЛУЧШЕ_И_ДЛЯ_ЕЕ_ОСОБЕННОСТЕЙ_КАК_ИСТОРИИ_И_ДЛЯ_РАССКАЗЧИКА_ЗПТ_КОТОРЫЙ_БОРМОЧЕТ_СВОИ_ЗАКЛИНАНИЯ_НАД_ПРОШЕДШИМИ_ВРЕМЕНАМИ_ТЧК_ОДНАКО_ПРИХОДИТСЯ_ПРИЗНАТЬ_ЗПТ_ЧТО_ОНА_ЗПТ_ТАК_ЖЕ_КАК_В_НАШУ_ЭПОХУ_И_САМИ_ЛЮДИ_ЗПТ_ОСОБЕННО_ЖЕ_РАССКАЗЧИКИ_ИСТОРИЙ_ЗПТ_ГОРАЗДО_СТАРЕЕ_СВОИХ_ЛЕТ_ЗПТ_ЕЕ_ВОЗРАСТ_ИЗМЕРЯЕТСЯ_НЕ_ПРОТЕКШИМИ_ДНЯМИ_ЗПТ_И_БРЕМЯ_ЕЕ_ГОДОВ_ТИРЕ_НЕ_ЧИСЛОМ_ОБРАЩЕНИЙ_ЗЕМЛИ_ВОКРУГ_СОЛНЦА_ТЧК_СЛОВОМ_ЗПТ_ОНА_ОБЯЗАНА_СТЕПЕНЬЮ_СВОЕЙ_ДАВНОСТИ_НЕ_САМОМУ_ВРЕМЕНИ_ТЧК_ОТМЕТИМ_ЗПТ_ЧТО_В_ЭТИХ_СЛОВАХ_МЫ_ДАЕМ_МИМОХОДОМ_НАМЕК_И_УКАЗАНИЕ_НА_СОМНИТЕЛЬНОСТЬ_И_СВОЕОБРАЗНУЮ_ДВОЙСТВЕННОСТЬ_ТОЙ_ЗАГАДОЧНОЙ_СТИХИИ_ЗПТ_КОТОРАЯ_ЗОВЕТСЯ_ВРЕМЕНЕМ_ТЧК_ОДНАКО_ЗПТ_НЕ_ЖЕЛАЯ_ИСКУССТВЕННО_ЗАТЕМНЯТЬ_ВОПРОС_ЗПТ_ПО_СУЩЕСТВУ_СОВЕРШЕННО_ЯСНЫЙ_ЗПТ_СКАЖЕМ_СЛЕДУЮЩЕЕ_ДВТЧ_ОСОБАЯ_ДАВНОСТЬ_НАШЕЙ_ИСТОРИИ_ЗАВИСИТ_ЕЩЕ_И_ОТ_ТОГО_ЗПТ_ЧТО_ОНА_ПРОИСХОДИТ_НА_НЕКОЕМ_РУБЕЖЕ_И_ПЕРЕД_ПОВОРОТОМ_ЗПТ_ГЛУБОКО_РАСЩЕПИВШИМ_НАШУ_ЖИЗНЬ_И_СОЗНАНИЕ_МНГТЧ_ОНА_ПРОИСХОДИТ_ЗПТ_ИЛИ_ЗПТ_ЧТОБЫ_ИЗБЕЖАТЬ_ВСЯКИХ_ФОРМ_НАСТОЯЩЕГО_ЗПТ_СКАЖЕМ_ЗПТ_ПРОИСХОДИЛА_ЗПТ_ПРОИЗОШЛА_НЕКОГДА_ЗПТ_КОГДА_ТИРЕ_ТО_ЗПТ_В_СТАРОДАВНИЕ_ВРЕМЕНА_ЗПТ_В_ДНИ_ПЕРЕД_ВЕЛИКОЙ_ВОЙНОЙ_ЗПТ_С_НАЧАЛОМ_КОТОРОЙ_НАЧАЛОСЬ_СТОЛЬ_МНОГОЕ_ЗПТ_ЧТО_ПОТОМ_ОНО_УЖЕ_И_НЕ_ПЕРЕСТАВАЛО_НАЧИНАТЬСЯ_ТЧК_ИТАК_ЗПТ_ОНА_ПРОИСХОДИТ_ПЕРЕД_ТЕМ_ПОВОРОТОМ_ЗПТ_ПРАВДА_НЕЗАДОЛГО_ДО_НЕГО_ТЧК_НО_РАЗВЕ_ХАРАКТЕР_ДАВНОСТИ_КАКОЙ_ТИРЕ_НИБУДЬ_ИСТОРИИ_НЕ_СТАНОВИТСЯ_ТЕМ_ГЛУБЖЕ_ЗПТ_СОВЕРШЕННЕЕ_И_СКАЗОЧНЕЕ_ЗПТ_ЧЕМ_БЛИЖЕ_ОНА_К_ЭТОМУ_ПЕРЕД_ТЕМ_ВПРС_КРОМЕ_ТОГО_ЗПТ_НАША_ИСТОРИЯ_ЗПТ_БЫТЬ_МОЖЕТ_ЗПТ_И_ПО_СВОЕЙ_ВНУТРЕННЕЙ_ПРИРОДЕ_НЕ_ЛИШЕНА_НЕКОТОРОЙ_СВЯЗИ_СО_СКАЗКОЙ_ТЧК_МЫ_БУДЕМ_ОПИСЫВАТЬ_ЕЕ_ВО_ВСЕХ_ПОДРОБНОСТЯХ_ЗПТ_ТОЧНО_И_ОБСТОЯТЕЛЬНО_ЗПТ_ТИРЕ_ИБО_КОГДА_ЖЕ_ВРЕМЯ_ПРИ_ИЗЛОЖЕНИИ_КАКОЙ_ТИРЕ_НИБУДЬ_ИСТОРИИ_ЛЕТЕЛО_ИЛИ_ТЯНУЛОСЬ_ПО_ПОДСКАЗКЕ_ПРОСТРАНСТВА_И_ВРЕМЕНИ_ЗПТ_КОТОРЫЕ_НУЖНЫ_ДЛЯ_ЕЕ_РАЗВЕРТЫВАНИЯ_ВПРС_НЕ_ОПАСАЯСЬ_УПРЕКА_В_ПЕДАНТИЗМЕ_ЗПТ_МЫ_СКОРЕЕ_СКЛОННЫ_УТВЕРЖДАТЬ_ЗПТ_ЧТО_ЛИШЬ_ОСНОВАТЕЛЬНОСТЬ_МОЖЕТ_БЫТЬ_ЗАНИМАТЕЛЬНОЙ_ТЧК_СЛЕДОВАТЕЛЬНО_ЗПТ_ОДНИМ_МАХОМ_РАССКАЗЧИК_С_ИСТОРИЕЙ_ГАНСА_НЕ_СПРАВИТСЯ_ТЧК_СЕМИ_ДНЕЙ_НЕДЕЛИ_НА_НЕЕ_НЕ_ХВАТИТ_ЗПТ_НЕ_ХВАТИТ_И_СЕМИ_МЕСЯЦЕВ_ТЧК_САМОЕ_ЛУЧШЕЕ_ТИРЕ_И_НЕ_СТАРАТЬСЯ_УЯСНИТЬ_СЕБЕ_ЗАРАНЕЕ_ЗПТ_СКОЛЬКО_ИМЕННО_ПРОЙДЕТ_ЗЕМНОГО_ВРЕМЕНИ_ЗПТ_ПОКА_ОНА_БУДЕТ_ДЕРЖАТЬ_ЕГО_В_СВОИХ_ТЕНЕТАХ_ТЧК_СЕМИ_ЛЕТ_ЗПТ_ДАСТ_БОГ_ЗПТ_ВСЕ_ЖЕ_НЕ_ПОНАДОБИТСЯ_ТЧК_ИТАК_ЗПТ_МЫ_НАЧИНАЕМ_ТЧК',
                'ЛОРДЫ_И_ЛЕДИ_ВИЗЕНГАМОТА_В_ФИОЛЕТОВЫХ_МАНТИЯХ_ЗПТ_ОТМЕЧЕННЫХ_СЕРЕБРЯНОЙ_ЛИТЕРОЙ_В_ЗПТ_С_ХОЛОДНЫМ_УПРЕКОМ_СМОТРЕЛИ_НА_ДРОЖАЩУЮ_ДЕВОЧКУ_ЗПТ_ЗАКОВАННУЮ_В_ЦЕПИ_ТЧК_ЕСЛИ_В_РАМКАХ_КАКОЙТО_ЭТИЧЕСКОЙ_СИСТЕМЫ_ОНИ_И_ПОРИЦАЛИ_СЕБЯ_ЗПТ_ТО_ОПРЕДЕЛЕННО_СТАВИЛИ_ЭТО_СЕБЕ_В_ЗАСЛУГУ_ТЧК_ГАРРИ_С_ТРУДОМ_МОГ_РОВНО_ДЫШАТЬ_ТЧК_ЕГО_ТЕМНАЯ_СТОРОНА_ПРИДУМАЛА_ПЛАН_МНГТЧ_И_ОТСТУПИЛА_НАЗАД_ТЧК_СЛИШКОМ_ЛЕДЯНОЙ_ТОН_НЕ_ПОЙДЕТ_НА_ПОЛЬЗУ_ГЕРМИОНЕ_ТЧК_БУДУЧИ_ЛИШЬ_НАПОЛОВИНУ_ПОГРУЖЕННЫМ_В_СВОЮ_ТЕМНУЮ_СТОРОНУ_ЗПТ_ГАРРИ_ПОЧЕМУТО_ЭТОГО_НЕ_ПОНИМАЛ_МНГТЧ',
                'А_БЖ0101011010111101011010101010101001111010100101011010101010100101001010010101010001010101001010101011101100111111011101',
                'ОБЖ_ГОД_В_Я011',
                'ШИФРОПАНКИ_ЭТО_НЕФОРМАЛЬНАЯ_ГРУППА_ЛЮДЕЙ_ЗПТ_ЗАИНТЕРЕСОВАННЫХ_В_СОХРАНЕНИИ_АНОНИМНОСТИ_И_ИНТЕРЕСУЮЩИХСЯ_КРИПТОГРАФИЕЙ_ТЧК_ПЕРВОНАЧАЛЬНО_ШИФРОПАНКИ_ОБЩАЛИСЬ_С_ПОМОЩЬЮ_СЕТИ_АНОНИМНЫХ_РЕМЕЙЛЕРОВ_ТЧК_ЦЕЛЬЮ_ДАННОЙ_ГРУППЫ_БЫЛО_ДОСТИЖЕНИЕ_АНОНИМНОСТИ_И_БЕЗОПАСНОСТИ_ПОСРЕДСТВОМ_АКТИВНОГО_ИСПОЛЬЗОВАНИЯ_КРИПТОГРАФИИ_ТЧК']

"""
print(len(INPUTS_ARRAY))
for i in range(len(INPUTS_ARRAY)):
    print([len(INPUTS_ARRAY[i]), len((msg2bin(INPUTS_ARRAY[i])))])
"""

ASSOCDATA_ARRAY = (['ВА', 'АЛИСА__А', 'БОБ____А', 'КОТОПОЕЗД'],
                   ['ВБ', 'АЛИСА_АЖ', 'БОБ___ОЧ', 'ЕГИПТЯНИН'],
                   ['В_', 'АЛИСА_ЯЗ', 'БОБ___ЬЬ', 'ЩЕГОЛЯНИЕ'],
                   ['ВБ', 'БОБ___ЬЬ', 'АЛИСА_ЯЗ', 'ЭКЛАМПСИЯ'],
                   ['ВБ', 'БОБ___ЬЬ', 'АЛИСА_ЯЗ', 'ЕГИПТЯНИН'],
                   ['ВБ', 'АЛИСА_ЯЗ', 'БОБ___ЬЬ', 'ЕГИПТЯНИН'])

def check_padding(binmsg_in):
    bins = binmsg_in
    M = len(bins)
    blocks = M // 80
    remainder = M % 80
    f = 0
    numblocks = 0
    padlength = 0
    if remainder == 0:
        tb = bins[M - 20: M]
        ender = tb[17: 20]
        if ender == [0, 0, 1]:
            NB = tb[7: 17]
            PL = tb[0: 7]
            padlength = 0
            for i in range(7):
                padlength = 2 * padlength + PL[i]
            numblocks = 0
            for i in range(10):
                numblocks = 2 * numblocks + NB[i]
            if numblocks == blocks and 23 <= padlength < 103:
                start_idx = M - padlength
                end_idx = M - 20
                tb = bins[start_idx:end_idx]
                starter = tb[0]
                if starter == 1:
                    f = 1
                    for j in range(1, padlength - 20):
                        if j < len(tb):
                            tmp = tb[j]
                            if tmp == 1:
                                f = 0
                                break
                else:
                    f = 0
            else:
                f = 0
        else:
            f = 0
    out = (f, [numblocks, padlength])
    return out

def produce_padding(rem_in, blocks_in):
    if rem_in == 0:
        b = blocks_in + 1
        r = 80
    elif rem_in <= 57:
        r = 80 - rem_in
        b = blocks_in + 1
    else:
        b = blocks_in + 2
        r = 160 - rem_in
    pad = [0] * r
    pad[0] = 1
    rt = r
    for i in range(6, -1, -1):
        pad[r - 20 + i] = rt % 2
        rt //= 2
    b_temp = b
    for i in range(9, -1, -1):
        pad[r - 13 + i] = b_temp % 2
        b_temp //= 2
    pad[r - 3] = 0
    pad[r - 2] = 0
    pad[r - 1] = 1
    return pad

def pad_message(msg_in):
    pad = ''
    bins = msg2bin(msg_in)
    M = len(bins)
    blocks = M // 80
    remainder = M % 80
    if remainder == 0:
        f = check_padding(bins)[0]
    else:
        f = 1
    if f == 1:
        pad = produce_padding(remainder, blocks)
        bins = bins + pad
        out = bin2msg(bins)
    else:
        out = msg_in
    return out

def unpad_message(msg_in):
    bins = msg2bin(msg_in)
    M = len(bins)
    T = check_padding(bins)
    T1 = T[1]
    if T[0] == 1:
        pl = T1[1]
        tmp = bins[0: M - pl]
        out = bin2msg(tmp)
    return out

"""
IN1 = INPUTS_ARRAY[5]
IN2 = pad_message(IN1)
tmp = check_padding(msg2bin(IN2))
inter = pad_message(IN2)
tmp1 = check_padding(msg2bin(inter))
out = unpad_message(inter)
print(len(IN1), len(msg2bin(IN1)))
print(len(IN2), len(msg2bin(IN2)))
print(tmp)
print(len(inter), len(msg2bin(inter)))
print(tmp1)
print(len(out), len(msg2bin(out)))
"""

def prepare_packet(data_in, iv_in, msg_in):
    data = data_in
    iv = add_txt('________________', iv_in)
    msg = pad_message(msg_in)
    l = len(msg2bin(msg))
    a = ''
    tmp = l
    for i in range(5):
        a = num2sym(l % 32) + a
        l = l // 32
    data.append(a)
    mac = ''
    return [data, iv, msg, mac]

def validate_packet(packet_in):
    data = packet_in[0]
    iv = packet_in[1]
    msg = packet_in[2]
    mac = packet_in[3]
    f = 1
    t = data[0][0]
    s = data[0][1]
    ml = len(mac)
    if t != 'В':
        f = 0
    elif (s == 'А' or s == 'Б') and ml != 16:
        f = 0
    elif (s == '_') and ml != 0:
        f = 0
    return f

def transnit(packet_in):
    data = packet_in[0]
    iv = packet_in[1]
    msg = packet_in[2]
    mac = packet_in[3]
    out = data[0] + data[1] + data[2] + data[3] + data[4]
    out = msg2bin(out + iv + msg + mac)
    return out

def recieve(stream_in):
    p = bin2msg(stream_in)
    type = p[0:2]
    sender = p[2: 10]
    reciever = p[10: 18]
    session = p[18: 27]
    length = p[27: 32]
    iv = p[32: 48]
    L = 0
    for i in range(5):
        t = length[i]
        l = sym2num(t)
        L = L * 32 + l
    L = L // 5
    message = p[48: 48 + L]
    mac = p[48 + L:]
    out = ([type, sender, reciever, session, length], iv, message, mac)
    return out
"""
print(ASSOCDATA_ARRAY[1])
xtst = prepare_packet(ASSOCDATA_ARRAY[1], 'КОЛЕСО', INPUTS_ARRAY[1])
print(xtst)
ytst = recieve(transnit(xtst))
print(ytst)
print(validate_packet(ytst))
"""

def textxor(A_in, B_in):
    out = ''
    for i in range(4):
        a = A_in[i * 4: i * 4 + 4]
        b = B_in[i * 4: i * 4 + 4]
        A = dec2bin(block2num(a))
        B = dec2bin(block2num(b))
        C = []
        for j in range(20):
            C_j = (A[j] + B[j]) % 2
            C.append(C_j)
        c = bin2dec(C)
        out = out + num2block(c)
    return out
"""
A1 = 'ГОЛОВКА_КРУЖИТСЯ'
B1 = 'СИНЕВАТАЯ_БОРОДА'
A2 = 'МЫШКА_БЫЛА_ЛИХОЙ'
B2 = 'ЗЕЛЕНЫЙ_КОТОЗМИЙ'
C1 = textxor(A1, A2)
C2 = textxor(A1, B2)
print(C1, C2)
print(textxor(C1, A2), textxor(C1, A1))
print(textxor(C2, A1), textxor(C2, A2))
"""

def enc_CTR(msg_in, iv_in, key_in):
    m = len(msg_in) // 16
    iv_starter = iv_in[:12]
    ctr = 0
    out = ''
    for i in range(m):
        iv_ender = num2block(ctr)
        iv = iv_starter + iv_ender
        keystream = frw_Feistel(iv, key_in, 6)
        inp = msg_in[i * 16: i * 16 + 16]
        out = out + textxor(inp, keystream)
        ctr += 1
    return out

tst = INPUTS_ARRAY[0]
iv1 = 'АЛИСА_УМЕЕТ_ПЕТЬ'
iv2 = 'БОБ_НЕМНОГО_ПЬЯН'
iv3 = 'БОБ_НЕМНОГО_УНЫЛ'
keyset = produce_round_keys('СЕАНСОВЫЙ_КЛЮЧИК', 8, SET)
f_tst1m = enc_CTR(tst, iv1, keyset)
print(f_tst1m)
print(len(f_tst1m))
i_test1m = enc_CTR(f_tst1m, iv1, keyset)
print(i_test1m)

f_test1 = enc_CTR(tst, iv2, keyset)
print(f_test1)
i_test10 = enc_CTR(f_test1, iv2, keyset)
print(i_test10)
i_test11 = enc_CTR(f_test1, iv1, keyset)
i_test1 = enc_CTR(f_test1, iv3, keyset)
if i_test11 == tst:
    print('Совпадают')
else:
    print('Не совпадают')
if i_test1 == tst:
    print('Совпадают')
else:
    print('Не совпадают')

def mac_CBC(msg_in, iv_in,key_in):
    m = len(msg_in) // 16
    out = ''
    feedback = iv_in
    for i in range(m):
        inp = msg_in[i * 16: i * 16 + 16]
        temp = textxor(feedback, inp)
        feedback = frw_Feistel(temp, key_in, 6)
        out = out + feedback
    return feedback

F_TEST1 = mac_CBC(tst, iv1, keyset)
print(F_TEST1)

def combine(strset):
    out = ''
    for i in range(len(strset)):
        out = out + strset[i]
    return out

def blockxor(A_in, B_in):
    A = dec2bin(block2num(A_in))
    B = dec2bin(block2num(B_in))
    C = []
    for j in range(20):
        C_j = (A[j] + B[j]) % 2
        C.append(C_j)
    c = bin2dec(C)
    return num2block(c)

#print(blockxor('КОНЬ', 'А__Г'))

