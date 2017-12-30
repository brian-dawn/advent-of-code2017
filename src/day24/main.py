
def parse(line):
    a, b = line.split('/')
    return int(a), int(b)


def read_components(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return map(parse, fp.readlines())


def dfs_max(components, current_port=0):
    result = 0
    for i, comp in enumerate(components):
        a, b = comp
        if b == current_port:
            a, b = b, a
        if a == current_port:
            new_comp = components[:i] + components[i+1:]
            result = max(result, a + b + dfs_max(new_comp, current_port=b))
    return result


def dfs_longest(components, current_port=0):
    strength, length = 0, 0
    for i, comp in enumerate(components):
        a, b = comp
        if b == current_port:
            a, b = b, a
        if a == current_port:
            new_comp = components[:i] + components[i+1:]
            new_str, new_len = dfs_longest(new_comp, current_port=b)
            old_length = length
            length = max(length, new_len + 1)
            if length == new_len + 1:
                if old_length == length:
                    strength = max(strength, a + b + new_str)
                else:
                    strength = a + b + new_str
    return strength, length


def run():
    components = read_components('day24.txt')
    return dfs_max(components)


def run_2():
    components = read_components('day24.txt')
    return dfs_longest(components)


def run_2_test():
    components = read_components('day24_test.txt')
    return dfs_longest(components)

if __name__ == '__main__':
    print run()
    print run_2()
