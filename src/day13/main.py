import itertools


def read_security(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        for line in fp:
            yield map(int, line.split(': '))


def sum_with_offset(offset, firewall):
    return sum(depth * rng for depth, rng in firewall if (depth + offset) % (rng * 2 - 2) == 0)


def run():
    return sum_with_offset(0, read_security('day13.txt'))


def run_2():
    firewall = [s for s in read_security('day13.txt')]
    for i in itertools.count():
        if i % (firewall[0][1] * 2 - 2) and sum_with_offset(i, firewall) == 0:
            return i


def gets_through(offset, firewall):
    for depth, rng in firewall:
        if (depth + offset) % (rng * 2 - 2) == 0:
            return False
    return True


def run_2_fast():
    firewall = [s for s in read_security('day13.txt')]
    for i in itertools.count():
        if gets_through(i, firewall):
            return i

if __name__ == '__main__':
    print run()
    print run_2_fast()
