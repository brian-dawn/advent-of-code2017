from collections import defaultdict


class Direction:
    def __init__(self, step_mod, left=None, right=None, reverse=None):
        self.step_mod = step_mod
        self.left = left
        self.right = right
        self.reverse = reverse

    def change_dir(self, state):
        if state == '.':
            return self.left
        if state == '#':
            return self.right
        if state == 'W':
            return self
        if state == 'F':
            return self.reverse


UP_MOD, DOWN_MOD, LEFT_MOD, RIGHT_MOD = (0, 1), (0, -1), (-1, 0), (1, 0)
UP = Direction(UP_MOD)
DOWN = Direction(DOWN_MOD, reverse=UP)
LEFT = Direction(LEFT_MOD, left=DOWN, right=UP)
RIGHT = Direction(RIGHT_MOD, left=UP, right=DOWN, reverse=LEFT)
UP.left, UP.right, UP.reverse = LEFT, RIGHT, DOWN
DOWN.left, DOWN.right = RIGHT, LEFT
LEFT.reverse = RIGHT


def read_network(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return [[c for c in line.strip()] for line in fp.readlines()]


def change_for_node(node_val, cur_dir, mapper):
    return mapper[node_val], cur_dir.change_dir(node_val)


def add_coords(one, two):
    return one[0] + two[0], one[1] + two[1]


def initial_network():
    init_network = read_network('day22.txt')
    network = defaultdict(lambda: '.')
    mid_y, mid_x = int(len(init_network)/2), int(len(init_network[0])/2)
    for i in range(len(init_network)):
        for j in range(len(init_network[i])):
            network[(j-mid_x, -(i-mid_y))] = init_network[i][j]
    return network


def run_with_map(state_mapper, size):
    network = initial_network()
    direction = UP
    location = (0, 0)
    infect_count = 0
    for _ in range(size):
        val = network[location]
        val, direction = change_for_node(val, direction, state_mapper)
        network[location] = val
        infect_count += 1 if val == '#' else 0
        location = add_coords(location, direction.step_mod)
    return infect_count

BASIC_MAPPER = {
    '.': '#',
    '#': '.'
}
def run():
    return run_with_map(BASIC_MAPPER, 10000)

EVOLVED_MAPPER = {
    '.': 'W',
    'W': '#',
    '#': 'F',
    'F': '.'
}
def run_2():
    return run_with_map(EVOLVED_MAPPER, 10000000)

if __name__ == '__main__':
    print run()
    print run_2()
