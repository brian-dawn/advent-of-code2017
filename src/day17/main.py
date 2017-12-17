INPUT = 386


def run():
    idx = 0
    circ_buff = [0]
    for i in range(1, 2018):
        idx = (INPUT + idx) % i + 1
        circ_buff.insert(idx, i)
    return circ_buff[circ_buff.index(2017) + 1]


def run_2():
    idx = 0
    result = -1
    for i in range(1, 50000001):
        idx = (INPUT + idx) % i + 1
        result = i if idx == 1 else result
    return result

if __name__ == '__main__':
    print run()
    print run_2()

