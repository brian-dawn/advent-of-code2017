from collections import defaultdict


class State:
    def __init__(self):
        self._registers = defaultdict(lambda: 0)
        self.sound = None
        self.index = 0
        self.recovered = None
        self.mul_counter = 0

    def __getitem__(self, key):
        if isinstance(key, int):
            return key
        return self._registers[key]

    def __setitem__(self, key, value):
        self._registers[key] = value


def _set(reg_x, val_y, state):
    state[reg_x] = state[val_y]
    _jnz(1, 1, state)


def _sub(reg_x, val_y, state):
    state[reg_x] -= state[val_y]
    _jnz(1, 1, state)


def _mul(reg_x, val_y, state):
    state[reg_x] *= state[val_y]
    state.mul_counter += 1
    _jnz(1, 1, state)


def _jnz(val_x, val_y, state):
    state.index += state[val_y] if state[val_x] != 0 else 1


def _maybe_reg_or_val(val):
    try:
        return int(val)
    except ValueError:
        return val.strip()


def parse(inst_str):
    parts = inst_str.split(' ')
    instr = parts[0]
    params = map(_maybe_reg_or_val, parts[1:])
    if instr == 'set':
        return lambda state: _set(params[0], params[1], state)
    if instr == 'sub':
        return lambda state: _sub(params[0], params[1], state)
    if instr == 'mul':
        return lambda state: _mul(params[0], params[1], state)
    if instr == 'jnz':
        return lambda state: _jnz(params[0], params[1], state)


def read_instructions(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return map(parse, fp.readlines())


def run():
    instructions = read_instructions('day23.txt')
    state = State()
    while state.index < len(instructions):
        instr = instructions[state.index]
        instr(state)
    return state.mul_counter


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if not n & 1:
        return False
    for x in range(3, int(n**0.5)+1, 2):
        if n % x == 0:
            return False
    return True


def run_2():
    h = 0
    c = 125100
    for b in range(108100, c + 1, 17):
        h += 0 if is_prime(b) else 1
    return h

if __name__ == '__main__':
    print run()
    print run_2()
