def read_data(file_name):
    file_ref = open('../../resources/' + file_name, 'r')
    result = file_ref.read()
    file_ref.close()
    return [int(i) for i in result.split('\n')]


def run():
    loop = read_data('day5.txt')
    current_idx = 0
    counter = 0
    length = len(loop)
    while current_idx < length:
        loop[current_idx] += 1
        current_idx += loop[current_idx] - 1
        counter += 1
    return counter


def run_2():
    loop = read_data('day5.txt')
    current_idx = 0
    counter = 0
    length = len(loop)
    while current_idx < length:
        prev_idx = current_idx
        current_idx += loop[current_idx]
        loop[prev_idx] += 1 if loop[prev_idx] < 3 else -1
        counter += 1
    return counter

if __name__ == '__main__':
    print run()
    print run_2()
