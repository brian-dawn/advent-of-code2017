ITERATIONS = 1000000000


def perform_spin(amt, dancers):
    return dancers[-amt:] + dancers[:-amt]


def perform_exchange(a, b, dancers):
    dancers = dancers[:]
    dancers[a], dancers[b] = dancers[b], dancers[a]
    return dancers


def perform_partner(a, b, dancers):
    return perform_exchange(dancers.index(a), dancers.index(b), dancers)


def parse_spin(dance_str):
    return lambda dancers: perform_spin(int(dance_str), dancers)


def parse_exchange(dance_str):
    a, b = dance_str.split('/')
    return lambda dancers: perform_exchange(int(a), int(b), dancers)


def parse_partner(dance_str):
    a, b = dance_str.split('/')
    return lambda dancers: perform_partner(a, b, dancers)


def parse(dance_str):
    return {
        's': parse_spin,
        'x': parse_exchange,
        'p': parse_partner
    }[dance_str[0]](dance_str[1:])


def read_dance(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return map(parse, fp.read().split(','))


def run():
    dance_moves = read_dance('day16.txt')
    result = reduce(lambda d, f: f(d), dance_moves, [chr(i) for i in range(ord('a'), ord('p') + 1)])
    return ''.join(result)


def run_2():
    dance_moves = read_dance('day16.txt')
    current = [chr(i) for i in range(ord('a'), ord('p') + 1)]
    results = []
    while not results or current != results[0]:
        results.append(current)
        current = reduce(lambda d, f: f(d), dance_moves, current)
    return ''.join(results[ITERATIONS % len(results)])

if __name__ == '__main__':
    print run()
    print run_2()
