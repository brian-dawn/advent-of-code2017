import regex as re

PATTERN = re.compile(r'(\d+) <-> (.*)')


def read_pipes(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        for line in fp.readlines():
            m = PATTERN.search(line)
            yield int(m.group(1)), map(int, m.group(2).split(','))


def run():
    pipe_map = {}
    for node, to_nodes in read_pipes('day12.txt'):
        pipe_map[node] = to_nodes

    todo = {0}
    done = set()
    while todo:
        val = todo.pop()
        if val in done:
            continue
        nodes = pipe_map[val]
        for node in nodes:
            todo.add(node)
        done.add(val)
    return len(done)


def run_2():
    pipe_map = {}
    for node, to_nodes in read_pipes('day12.txt'):
        pipe_map[node] = to_nodes

    vals = set(pipe_map.keys())
    groups = 0
    while vals:
        groups += 1
        build_group_of = vals.pop()
        todo = {build_group_of}
        done = set()
        while todo:
            val = todo.pop()
            if val in done:
                continue
            nodes = pipe_map[val]
            for node in nodes:
                todo.add(node)
            done.add(val)
            vals.remove(val) if val in vals else None
    return groups

if __name__ == '__main__':
    print run()
    print run_2()
