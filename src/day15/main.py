
GEN_A_INIT = 679
GEN_A_FACTOR = 16807
GEN_B_INIT = 771
GEN_B_FACTOR = 48271
MODULUS = 2147483647

RUN_1_LENGTH = 40000000
RUN_2_LENGTH = 5000000


def generator(init, factor, rule=lambda a: True):
    result = init
    while True:
        result *= factor
        result %= MODULUS
        if rule(result):
            yield result


def run():
    a = generator(GEN_A_INIT, GEN_A_FACTOR)
    b = generator(GEN_B_INIT, GEN_B_FACTOR)
    return len([1 for _ in range(RUN_1_LENGTH) if a.next() & 0xFFFF == b.next() & 0xFFFF])


def run_2():
    a = generator(GEN_A_INIT, GEN_A_FACTOR, rule=lambda x: x % 4 == 0)
    b = generator(GEN_B_INIT, GEN_B_FACTOR, rule=lambda x: x % 8 == 0)
    return len([1 for _ in range(RUN_2_LENGTH) if a.next() & 0xFFFF == b.next() & 0xFFFF])

if __name__ == '__main__':
    print run()
    print run_2()
