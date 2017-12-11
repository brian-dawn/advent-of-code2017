
STEP_FUNCS = {
    'n': lambda x, y, z: (x, y + 1, z - 1),
    'ne': lambda x, y, z: (x + 1, y, z - 1),
    'se': lambda x, y, z: (x + 1, y - 1, z),
    's': lambda x, y, z: (x, y - 1, z + 1),
    'sw': lambda x, y, z: (x - 1, y, z + 1),
    'nw': lambda x, y, z: (x - 1, y + 1, z)
}


def read_directions(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return fp.read().split(',')


def run():
    steps = read_directions('day11.txt')
    curr = 0, 0, 0
    for step in steps:
        curr = STEP_FUNCS[step](*curr)
    return sum(map(abs, curr))/2


def run_2():
    steps = read_directions('day11.txt')
    curr = 0, 0, 0
    furthest = 0
    for step in steps:
        curr = STEP_FUNCS[step](*curr)
        furthest = max(furthest, sum(map(abs, curr))/2)
    return furthest

if __name__ == '__main__':
    print run()
    print run_2()
