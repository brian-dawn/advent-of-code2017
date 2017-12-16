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


DANCE_MAP = {
    's': parse_spin,
    'x': parse_exchange,
    'p': parse_partner
}
def parse(dance_str):
    return DANCE_MAP[dance_str[0]](dance_str[1:])


def read_dance_steps(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return fp.read().split(',')


def read_dance(file_name):
    return map(parse, read_dance_steps(file_name))


def run():
    dance_moves = read_dance('day16.txt')
    result = reduce(lambda d, f: f(d), dance_moves, [chr(i) for i in range(ord('a'), ord('p') + 1)])
    return ''.join(result)


def find_cycles(steps, dancers):
    name_map = {dancer: [dancer] for dancer in dancers}
    result = dancers
    something_changed = True
    while something_changed:
        something_changed = False
        result = reduce(lambda d, f: f(d), steps, result)
        for i in range(len(dancers)):
            chars = name_map[dancers[i]]
            new_char = result[i]
            if new_char in chars:
                continue
            something_changed = True
            chars += new_char
    return name_map


def run_2():
    dance_steps = read_dance_steps('day16.txt')
    dancers = [chr(i) for i in range(ord('a'), ord('p') + 1)]
    space_steps, name_steps = (map(parse, filter(lambda d: d[0] != 'p', dance_steps)),
                               map(parse, filter(lambda d: d[0] == 'p', dance_steps)))
    space_cycles = find_cycles(space_steps, dancers)
    name_cycles = find_cycles(name_steps, dancers)
    space_dancers = []
    for dancer in dancers:
        cycle = space_cycles[dancer]
        space_dancers += cycle[ITERATIONS % len(cycle)]
    result = []
    for dancer in space_dancers:
        cycle = name_cycles[dancer]
        result += cycle[ITERATIONS % len(cycle)]
    return ''.join(result)

if __name__ == '__main__':
    print run()
    print run_2()
