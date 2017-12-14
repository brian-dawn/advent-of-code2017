SALT = [17, 31, 73, 47, 23]


def _flip_sublist(lst, start_idx, length):
    def flip_sublist_simple():
        return lst[:start_idx] + lst[start_idx:start_idx + length][::-1] + lst[start_idx + length:]

    def flip_sublist_overflow():
        end = length - len(lst) + start_idx
        sub_list = (lst[start_idx:] + lst[:end])[::-1]
        back, front = sub_list[:len(lst) - start_idx], sub_list[len(lst) - start_idx:]
        return front + lst[end:start_idx] + back

    return flip_sublist_simple() if start_idx + length <= len(lst) else flip_sublist_overflow()


def _run_instructions(lengths, size, skip=0, idx=0, lst=None):
    if not lst:
        lst = [i for i in range(size)]
    for length in lengths:
        lst = _flip_sublist(lst, idx, length)
        idx = (idx + length + skip) % size
        skip += 1
    return lst, idx


def _to_binary_rep(hex_str):
    return bin(int(hex_str, 16))[2:].zfill(128)


def hash_value(value, salt=SALT, binary=False):
    lengths = map(ord, value) + salt
    size = len(lengths)
    idx, lst = 0, None
    for i in range(64):
        lst, idx = _run_instructions(lengths, 256, skip=size * i, idx=idx, lst=lst)
    chunks = [lst[i:i + 16] for i in range(0, len(lst), 16)]
    number_lst = [reduce(lambda a, b: a ^ b, chunk, 0) for chunk in chunks]
    result = ''.join(map("{:02x}".format, number_lst))
    if binary:
        return _to_binary_rep(result)
    return result
