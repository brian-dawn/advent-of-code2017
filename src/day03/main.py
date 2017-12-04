import math

INPUT = 265149


def manhattan_to_node(mem_address):
    # using centered octagonal numbers
    plane = math.ceil(.5 * (1 + math.sqrt(mem_address)) - 1)
    prev_oct_num = math.pow(2 * plane - 1, 2)
    next_oct_num = math.pow(2 * (plane + 1) - 1, 2)
    octal_inc = int((next_oct_num - prev_oct_num)/8)
    # fixes the bug on "corner" cases
    if mem_address in [prev_oct_num + i * octal_inc for i in range(2, 8, 2)]:
        return int((mem_address - prev_oct_num) % octal_inc + plane + octal_inc)
    return int((mem_address - prev_oct_num) % octal_inc + plane)


def run():
    return manhattan_to_node(INPUT)


node_transformers = [
    (-1, lambda n: (n[0], n[1] + 1)), # go up
    (0, lambda n: (n[0] - 1, n[1])),  # go left
    (0, lambda n: (n[0], n[1] - 1)),  # go down
    (1, lambda n: (n[0] + 1, n[1]))   # go right
]


def sum_adjacent_nodes(node, grid):
    result = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            adj_node = (node[0] + i, node[1] + j)
            try:
                result += grid[adj_node]
            except KeyError:
                continue  # treat errors as 0
    return result


def run_2():
    grid = {(0, 0): 1}
    plane = 1
    current_node = (1, 0)
    while True:
        for modifier, func in node_transformers:
            for _ in range(2 * plane + modifier):
                value = sum_adjacent_nodes(current_node, grid)
                grid[current_node] = value
                current_node = func(current_node)
                if value > INPUT:
                    return value
        plane += 1


if __name__ == '__main__':
    print run()
    print run_2()
