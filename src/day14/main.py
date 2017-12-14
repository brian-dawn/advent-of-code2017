INPUT = 'jxqlasbh'
SALT = [17, 31, 73, 47, 23]


def flip_sublist(lst, start_idx, length):
    def flip_sublist_simple():
        return lst[:start_idx] + lst[start_idx:start_idx + length][::-1] + lst[start_idx + length:]

    def flip_sublist_overflow():
        end = length - len(lst) + start_idx
        sub_list = (lst[start_idx:] + lst[:end])[::-1]
        back, front = sub_list[:len(lst) - start_idx], sub_list[len(lst) - start_idx:]
        return front + lst[end:start_idx] + back

    return flip_sublist_simple() if start_idx + length <= len(lst) else flip_sublist_overflow()


def run_instructions(lengths, size, skip=0, idx=0, lst=None):
    if not lst:
        lst = [i for i in range(size)]
    for length in lengths:
        lst = flip_sublist(lst, idx, length)
        idx = (idx + length + skip) % size
        skip += 1
    return lst, idx


def hash_value(value):
    lengths = map(ord, value) + SALT
    size = len(lengths)
    idx, lst = 0, None
    for i in range(64):
        lst, idx = run_instructions(lengths, 256, skip=size * i, idx=idx, lst=lst)
    chunks = [lst[i:i + 16] for i in range(0, len(lst), 16)]
    number_lst = [reduce(lambda a, b: a ^ b, chunk, 0) for chunk in chunks]
    return ''.join(map("{:02x}".format, number_lst))


def to_binary_rep(hex_str):
    return bin(int(hex_str, 16))[2:].zfill(128)


def run():
    acc = 0
    for i in range(128):
        val = hash_value(INPUT + '-' + str(i))
        binary = to_binary_rep(val)
        acc += len([dig for dig in binary if dig == '1'])
    return acc


def scrub_region(matrix, row, column):
    matrix[row][column] = '0'
    if row != 0 and matrix[row-1][column] == '1':
        scrub_region(matrix, row - 1, column)
    if row != len(matrix) - 1 and matrix[row+1][column] == '1':
        scrub_region(matrix, row + 1, column)
    if column != 0 and matrix[row][column-1] == '1':
        scrub_region(matrix, row, column - 1)
    if column != len(matrix[0]) - 1 and matrix[row][column+1] == '1':
        scrub_region(matrix, row, column + 1)


def run_2():
    binaries = []
    acc = 0
    for i in range(128):
        val = hash_value(INPUT + '-' + str(i))
        binaries.append([dig for dig in to_binary_rep(val)])
    for row, binary in enumerate(binaries):
        for column, char in enumerate(binary):
            if char == '1':
                scrub_region(binaries, row, column)
                acc += 1
    return acc

if __name__ == '__main__':
    print run()
    print run_2()
