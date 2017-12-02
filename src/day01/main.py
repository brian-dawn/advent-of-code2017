import regex as re

PATTERN = re.compile(r'((\d)\2+)')


def read_data(file_name):
    file_ref = open('../../resources/' + file_name, 'r')
    result = file_ref.read()
    file_ref.close()
    return result


def run():
    data = read_data('day1.txt')
    matches = PATTERN.findall(data)
    result = reduce(lambda a, b: a + b, [int(match[0]) * (len(match) - 1) for match, _ in matches])
    result += int(data[0]) if data[-1] == data[0] else 0
    return result


def run_2():
    data = read_data('day1.txt')
    loop_limit = len(data)/2
    return 2 * reduce(lambda a, b: a + b, [int(x) for i, x in enumerate(data) if i < loop_limit and x == data[loop_limit + i]])


def run_2_again():
    """Wherein I refuse to give up on regular expressions"""
    data = read_data('day1.txt')
    half_count = len(data)/2
    pattern_str = r'(\d)\d{' + str(half_count - 1) + r'}\1'
    pattern = re.compile(pattern_str)
    matches = pattern.findall(data, overlapped=True)
    return reduce(lambda a, b: a + b, [2 * int(match) for match in matches])

if __name__ == '__main__':
    print run()
    print run_2()
    print run_2_again()
