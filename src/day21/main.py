import regex as re


STARTING_POINT = [['.', '#', '.'],
                  ['.', '.', '#'],
                  ['#', '#', '#']]

PATTERN = re.compile(r'(.*) => (.*)')


def transform_to_matrix(string):
    return [[c for c in sub_str] for sub_str in string.split('/')]


def transform_to_string(matrix):
    return '/'.join(''.join(arr) for arr in matrix)


def flip(matrix):
    return [reversed(sub_arr) for sub_arr in matrix]


def flop(matrix):
    return reversed(matrix)


def rotate(matrix):
    return zip(*matrix[::-1])


def map_for_line(line):
    m = PATTERN.search(line)
    key, value = transform_to_matrix(m.group(1)), transform_to_matrix(m.group(2))
    result = {}
    for _ in range(4):
        result[transform_to_string(key)] = value
        result[transform_to_string(flip(key))] = value
        result[transform_to_string(flop(key))] = value
        key = rotate(key)
    return result


def rule_map(lines):
    rules = {}
    for line in lines:
        rules.update(map_for_line(line))
    return rules


def read_rules(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return rule_map(fp.readlines())


def extract_chunk(matrix, top_left, size):
    x, y = top_left
    return [[matrix[i][j] for i in range(x, x + size)] for j in range(y, y + size)]


def make_chunks(matrix):
    chunk_size = 3 if len(matrix) % 2 else 2
    row_count = len(matrix) / chunk_size
    chunks = []
    for i in range(row_count):
        chunks.append([])
        for j in range(row_count):
            chunks[i].append(extract_chunk(matrix, (i * chunk_size, j * chunk_size), chunk_size))
    return chunks


def enhance_chunk(chunk, rules):
    return rules[transform_to_string(chunk)]


def merge_chunks(chunk_matrix):
    result = []
    for i, chunk_row in enumerate(chunk_matrix):
        chunk_size = len(chunk_row[0][0])
        for _ in range(chunk_size):
            result.append([])
        for j, chunk in enumerate(chunk_row):
            for k, row in enumerate(chunk):
                result[k + chunk_size * i] += row
    return result


def enhance(matrix, rules, num_times):
    if not num_times:
        return matrix
    chunks = make_chunks(matrix)
    transformed = [[enhance_chunk(chunk, rules) for chunk in chunk_row] for chunk_row in chunks]
    matrix = merge_chunks(transformed)
    return enhance(matrix, rules, num_times - 1)


def run():
    rules = read_rules('day21.txt')
    enhanced = enhance(STARTING_POINT, rules, 5)
    return sum(len(filter(lambda c: c == '#', sub_arr)) for sub_arr in enhanced)


def run_2():
    rules = read_rules('day21.txt')
    enhanced = enhance(STARTING_POINT, rules, 18)
    return sum(len(filter(lambda c: c == '#', sub_arr)) for sub_arr in enhanced)

if __name__ == '__main__':
    print run()
    print run_2()
