from collections import namedtuple


def read_map(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return [[c for c in l] for l in fp.readlines()]

Direction = namedtuple('Direction', ['move', 'turns', 'forbidden'])
up_down_turns = []
UP = Direction(move=lambda x, y: (x - 1, y), turns=up_down_turns, forbidden=['|', ' ', '\n'])
DOWN = Direction(move=lambda x, y: (x + 1, y), turns=up_down_turns, forbidden=['|', ' ', '\n'])
RIGHT = Direction(move=lambda x, y: (x, y + 1), turns=[UP, DOWN], forbidden=['-', ' ', '\n'])
LEFT = Direction(move=lambda x, y: (x, y - 1), turns=[UP, DOWN], forbidden=['-', ' ', '\n'])
up_down_turns.append(RIGHT)
up_down_turns.append(LEFT)
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]


def get_char(map_grid, point):
    try:
        return map_grid[point[0]][point[1]]
    except IndexError:
        return ' '


def run():
    map_grid = read_map('day19.txt')
    result = ''
    count = 0
    position = (-1, 0)
    for i, c in enumerate(map_grid[0]):
        if c == '|':
            position = (0, i)
    cur_dir = DOWN
    cur_char = '|'
    impact = True
    while impact:
        impact = False
        while cur_char not in ['+', ' ', '\n']:
            impact = True
            position = cur_dir.move(*position)
            count += 1
            cur_char = get_char(map_grid, position)
            if ord('A') <= ord(cur_char) <= ord('Z'):
                result += cur_char
        for turn in cur_dir.turns:
            if get_char(map_grid, turn.move(*position)) not in cur_dir.forbidden:
                cur_dir = turn
                cur_char = 'keep going!'
                break
    return result, count


if __name__ == '__main__':
    print run()
