import regex as re
from collections import defaultdict

PATTERN = re.compile(r'(\w+) (inc|dec) (-?\d+) if (\w+) (<|<=|==|!=|>=|>) (-?\d+)')


def get_instructions(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        for text in fp.readlines():
            m = PATTERN.search(text)
            yield [m.group(i) for i in range(1, 7)]

ALTER_MODES = {
    'inc': lambda x, y: x + y,
    'dec': lambda x, y: x - y
}


def alter(reg, op, amt):
    mode = ALTER_MODES[op]
    return lambda regs: mode(regs[reg], int(amt))

PRED_MODES = {
    '<': lambda x, y: x < y,
    '<=': lambda x, y: x <= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '>=': lambda x, y: x >= y,
    '>': lambda x, y: x > y
}


def predicate(reg, op, amt):
    mode = PRED_MODES[op]
    return lambda regs: mode(regs[reg], int(amt))


def run():
    registers = defaultdict(lambda: 0)
    for reg, op, amt, cond_reg, cond_op, cond_amt in get_instructions('day8.txt'):
        if predicate(cond_reg, cond_op, cond_amt)(registers):
            registers[reg] = alter(reg, op, amt)(registers)
    return registers[max(registers, key=registers.get)]


def run_2():
    cur_max = 0
    registers = defaultdict(lambda: 0)
    for reg, op, amt, cond_reg, cond_op, cond_amt in get_instructions('day8.txt'):
        if predicate(cond_reg, cond_op, cond_amt)(registers):
            result = alter(reg, op, amt)(registers)
            cur_max = max(result, cur_max)
            registers[reg] = result
    return cur_max


if __name__ == '__main__':
    print run()
    print run_2()
