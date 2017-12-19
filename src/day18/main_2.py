from collections import defaultdict, deque


class Program:
    def __init__(self, program_id):
        self.program_id = program_id
        self._registers = defaultdict(lambda: 0)
        self._registers['p'] = program_id
        self.index = 0
        self.waiting = False
        self.queue = deque()
        self.send_count = 0

    def send(self, val):
        self.send_count += 1
        self.queue.append(val)

    def receive(self, reg_x):
        if len(self.queue):
            self[reg_x] = self.queue.popleft()
            return True
        self.waiting = True
        return False

    def __getitem__(self, key):
        if isinstance(key, int):
            return key
        return self._registers[key]

    def __setitem__(self, key, value):
        self._registers[key] = value


def _snd(val, running, sleeping):
    sleeping.send(running[val])
    _jgz(1, 1, running)


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


def _rcv(reg_x, running):
    if running.receive(reg_x):
        _jgz(1, 1, running)


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
        return lambda running, sleeping: _snd(params[0], running, sleeping)
    if instr == 'set':
        return lambda running, _: _set(params[0], params[1], running)
    if instr == 'add':
        return lambda running, _: _add(params[0], params[1], running)
    if instr == 'mul':
        return lambda running, _: _mul(params[0], params[1], running)
    if instr == 'mod':
        return lambda running, _: _mod(params[0], params[1], running)
    if instr == 'rcv':
        return lambda running, _: _rcv(params[0], running)
    if instr == 'jgz':
        return lambda running, _: _jgz(params[0], params[1], running)


def read_instructions(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return map(parse, fp.readlines())


def still_running(prog, instr):
    return prog.index < len(instr) and not prog.waiting


def run():
    instructions = read_instructions('day18.txt')
    running = Program(0)
    sleeping = Program(1)
    while still_running(running, instructions) \
            or still_running(sleeping, instructions):
        instr = instructions[running.index]
        instr(running, sleeping)
        running, sleeping = sleeping, running
    return [p for p in (running, sleeping) if p.program_id == 0][0].send_count

if __name__ == '__main__':
    print run()
