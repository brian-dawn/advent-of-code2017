from src import KnotHash

INPUT = 'jxqlasbh'


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


def run():
    acc = 0
    for i in range(128):
        binary = KnotHash.hash_value(INPUT + '-' + str(i), binary=True)
        acc += len([dig for dig in binary if dig == '1'])
    return acc


def run_2():
    binaries = []
    acc = 0
    for i in range(128):
        val = KnotHash.hash_value(INPUT + '-' + str(i), binary=True)
        binaries.append([dig for dig in val])
    for row, binary in enumerate(binaries):
        for column, char in enumerate(binary):
            if char == '1':
                scrub_region(binaries, row, column)
                acc += 1
    return acc

if __name__ == '__main__':
    print run()
    print run_2()
