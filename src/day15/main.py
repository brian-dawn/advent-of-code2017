
GEN_A_INIT = 679
GEN_A_FACTOR = 16807
GEN_B_INIT = 771
GEN_B_FACTOR = 48271
RADIX = 2147483647

RUN_1_LENGTH = 40000000
RUN_2_LENGTH = 5000000


def generate(prev_val, factor, rule=lambda a: True):
    val = (prev_val * factor) % RADIX
    if rule(val):
        return val
    return generate(val, factor, rule)


def run():
    judge = 0
    a_last_val = GEN_A_INIT
    b_last_val = GEN_B_INIT
    for i in range(RUN_1_LENGTH):
        a_last_val = generate(a_last_val, GEN_A_FACTOR)
        b_last_val = generate(b_last_val, GEN_B_FACTOR)
        a_bin = "{0:b}".format(a_last_val).zfill(32)[16:]
        b_bin = "{0:b}".format(b_last_val).zfill(32)[16:]
        judge += 1 if a_bin == b_bin else 0
    return judge


def run_2():
    judge = 0
    a_last_val = GEN_A_INIT
    b_last_val = GEN_B_INIT
    for i in range(RUN_2_LENGTH):
        a_last_val = generate(a_last_val, GEN_A_FACTOR, rule=lambda x: x % 4 == 0)
        b_last_val = generate(b_last_val, GEN_B_FACTOR, rule=lambda x: x % 8 == 0)
        a_bin = "{0:b}".format(a_last_val).zfill(32)[16:]
        b_bin = "{0:b}".format(b_last_val).zfill(32)[16:]
        judge += 1 if a_bin == b_bin else 0
    return judge

if __name__ == '__main__':
    # print run()
    print run_2()
