

def get_lines(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        for text in fp.read().split('\n'):
            yield [int(elem) for elem in text.split('\t')]


def run():
    lines = get_lines('day2.txt')
    return sum([max(line) - min(line) for line in lines])


def run_2():
    lines = get_lines('day2.txt')
    return sum(
                sum([
                        [a/b for i, a in enumerate(line)
                         for j, b in enumerate(line)
                         if a % b == 0
                         and i != j]
                        for line in lines
                        ], [])
    )

if __name__ == '__main__':
    print run()
    print run_2()
