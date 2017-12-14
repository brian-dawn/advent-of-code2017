from src import KnotHash


def length_list(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return map(int, fp.read().split(','))


def read_value(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return fp.read()


def run():
    lengths = length_list('day10.txt')
    tied, _ = KnotHash._run_instructions(lengths, 256)
    return tied[0] * tied[1]


def run_2():
    return KnotHash.hash_value(read_value('day10.txt'))


if __name__ == '__main__':
    print run()
    print run_2()
