from collections import defaultdict
from collections import deque


class State:
    def __init__(self, prog0, prog1):
        self.program0 = prog0
        self.program1 = prog1


class Program:
    def __init__(self, program_id):
        self._registers = defaultdict(lambda: 0)
        self._registers['p'] = program_id
        self._send = 0
        self.index = 0
        self.received = deque()

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
    state = State(Program(0), Program(1))


if __name__ == '__main__':
    print run()
