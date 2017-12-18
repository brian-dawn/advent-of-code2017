from collections import defaultdict


class State:
    def __init__(self):
        self._registers = defaultdict(lambda: 0)
        self.sound = None
        self.index = 0
        self.recovered = None

    def __getitem__(self, key):
        if isinstance(key, int):
            return key
        return self._registers[key]

    def __setitem__(self, key, value):
        self._registers[key] = value


def _snd(val, state):
    state.sound = state[val]
    _jgz(1, 1, state)


def _set(reg_x, val_y, state):
    state[reg_x] = state[val_y]
    _jgz(1, 1, state)


def _add(reg_x, val_y, state):
    state[reg_x] += state[val_y]
    _jgz(1, 1, state)


def _mul(reg_x, val_y, state):
    state[reg_x] *= state[val_y]
    _jgz(1, 1, state)


def _mod(reg_x, val_y, state):
    state[reg_x] %= state[val_y]
    _jgz(1, 1, state)


def _rcv(val_x, state):
    state.recovered = state.sound if state[val_x] else None
    _jgz(1, 1, state)


def _jgz(val_x, val_y, state):
    state.index += state[val_y] if state[val_x] > 0 else 1


def _maybe_reg_or_val(val):
    try:
        return int(val)
    except ValueError:
        return val.strip()


def parse(inst_str):
    parts = inst_str.split(' ')
    instr = parts[0]
    params = map(_maybe_reg_or_val, parts[1:])
    if instr == 'snd':
        return lambda state: _snd(params[0], state)
    if instr == 'set':
        return lambda state: _set(params[0], params[1], state)
    if instr == 'add':
        return lambda state: _add(params[0], params[1], state)
    if instr == 'mul':
        return lambda state: _mul(params[0], params[1], state)
    if instr == 'mod':
        return lambda state: _mod(params[0], params[1], state)
    if instr == 'rcv':
        return lambda state: _rcv(params[0], state)
    if instr == 'jgz':
        return lambda state: _jgz(params[0], params[1], state)


def read_instructions(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return map(parse, fp.readlines())


def run():
    instructions = read_instructions('day18.txt')
    state = State()
    while not state.recovered:
        instr = instructions[state.index]
        instr(state)
    return state.recovered


if __name__ == '__main__':
    print run()
