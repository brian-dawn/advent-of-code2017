
BONUS_LENGTHS = [17, 31, 73, 47, 23]


def length_list(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return map(int, fp.read().split(','))


def ascii_length_list(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return map(ord, fp.read())


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


def run():
    lengths = length_list('day10.txt')
    tied, _ = run_instructions(lengths, 256)
    return tied[0] * tied[1]


def run_2():
    lengths = ascii_length_list('day10.txt') + BONUS_LENGTHS
    size = len(lengths)
    idx, lst = 0, None
    for i in range(64):
        lst, idx = run_instructions(lengths, 256, skip=size*i, idx=idx, lst=lst)
    chunks = [lst[i:i + 16] for i in range(0, len(lst), 16)]
    number_lst = [reduce(lambda a, b: a ^ b, chunk, 0) for chunk in chunks]
    return ''.join(map("{:02x}".format, number_lst))


if __name__ == '__main__':
    print run()
    print run_2()
