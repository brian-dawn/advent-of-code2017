from src import KnotHash

INPUT = 'jxqlasbh'


def scrub_region(matrix, row, column):
    if row in [-1, len(matrix)]\
            or column in [-1, len(matrix[0])]\
            or matrix[row][column] != '1':
        return
    matrix[row][column] = '0'
    scrub_region(matrix, row - 1, column)
    scrub_region(matrix, row + 1, column)
    scrub_region(matrix, row, column - 1)
    scrub_region(matrix, row, column + 1)


def run():
    return sum(
        [len([dig for dig in
              KnotHash.hash_value(INPUT + '-' + str(i), binary=True) if dig == '1'])
         for i in range(128)])


def run_2():
    binaries = map(list, [KnotHash.hash_value(INPUT + '-' + str(i), binary=True) for i in range(128)])
    acc = 0
    for row, binary in enumerate(binaries):
        for column, char in enumerate(binary):
            if char == '1':
                # mutating while iterating over. Gross.
                scrub_region(binaries, row, column)
                acc += 1
    return acc

if __name__ == '__main__':
    print run()
    print run_2()
