import regex as re

PATTERN = re.compile(r'(\d+) <-> (.*)')


def read_pipes(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        for line in fp.readlines():
            m = PATTERN.search(line)
            yield int(m.group(1)), map(int, m.group(2).split(','))


def get_pipe_map():
    pipe_map = {}
    for node, to_nodes in read_pipes('day12.txt'):
        pipe_map[node] = to_nodes
    return pipe_map


def group_containing(value, pipe_map):
    todo = {value}
    done = set()
    while todo:
        val = todo.pop()
        if val in done:
            continue
        nodes = pipe_map[val]
        for node in nodes:
            todo.add(node)
        done.add(val)
    return done


def run():
    return len(group_containing(0, get_pipe_map()))


def run_2():
    pipe_map = get_pipe_map()
    nodes = set(pipe_map.keys())
    groups = 0
    while nodes:
        groups += 1
        build_group_of = nodes.pop()
        group = group_containing(build_group_of, pipe_map)
        nodes = nodes.difference(group)
    return groups

if __name__ == '__main__':
    print run()
    print run_2()
