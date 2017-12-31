from collections import defaultdict
from itertools import takewhile
import regex as re

START_DEF = re.compile(r'Begin in state (\w)\.')
DURATION_DEF = re.compile(r'Perform a diagnostic checksum after (\d+) steps\.')

STATE_DEF = re.compile(r'In state (\w):')

CONDITION_DEF = re.compile(r'If the current value is (0|1):')
WRITE_DEF = re.compile(r'Write the value (0|1)\.')
MOVE_DEF = re.compile(r'Move one slot to the (right|left)\.')
CHANGE_DEF = re.compile(r'Continue with state (\w)\.')

MOVE_FUNCS = {
    'right': lambda mach: mach.right(),
    'left': lambda mach: mach.left()
}


class Machine:
    def __init__(self, state_key, duration, states):
        self.current_state_key = state_key
        self.duration = duration
        self.states = states
        self.tape = defaultdict(lambda: 0)
        self.cursor = 0

    def checksum(self):
        return sum(self.tape.itervalues())

    def read(self):
        return self.tape[self.cursor]

    def write(self, val):
        self.tape[self.cursor] = val

    def right(self):
        self.cursor += 1

    def left(self):
        self.cursor -= 1

    def state_change(self, new_state_key):
        self.current_state_key = new_state_key

    def current_state(self):
        return self.states[self.current_state_key]

    def run(self):
        for i in range(self.duration):
            self.current_state().apply(self)


class State:
    def __init__(self, name, branch_0, branch_1):
        self.name = name
        self.branch_0 = branch_0
        self.branch_1 = branch_1

    def apply(self, machine):
        branch = self.branch_1 if machine.read() else self.branch_0
        branch.apply(machine)


class Branch:
    def __init__(self, write, move, change):
        self.write = write
        self.move = move
        self.change = change

    def apply(self, machine):
        self.write(machine)
        self.move(machine)
        self.change(machine)


def read_blueprints(file_name):
    def write_func(val):
        return lambda mach: mach.write(val)

    def move_func(direction):
        return MOVE_FUNCS[direction]

    def state_func(state_key):
        return lambda mach: mach.state_change(state_key)

    def parse_branch(branch_lines):
        write = write_func(int(WRITE_DEF.search(branch_lines[0]).group(1)))
        move = move_func(MOVE_DEF.search(branch_lines[1]).group(1))
        change = state_func(CHANGE_DEF.search(branch_lines[2]).group(1))
        return Branch(write, move, change)

    def parse_state(state_lines):
        name = STATE_DEF.search(state_lines[0]).group(1)
        branch_0 = parse_branch(state_lines[2:5])
        branch_1 = parse_branch(state_lines[6:])
        return State(name, branch_0, branch_1)

    def parse_states(line_list):
        result = {}
        while line_list:
            state_lines = [l for l in takewhile(lambda line: line != '\n', line_list)]
            state = parse_state(state_lines)
            result[state.name] = state
            line_list = line_list[len(state_lines) + 1:]
        return result

    with open('../../resources/' + file_name, 'r') as fp:
        lines = fp.readlines()
        begin, dur = lines[0:2]
        begin = START_DEF.search(begin).group(1)
        dur = int(DURATION_DEF.search(dur).group(1))
        states = parse_states(lines[3:])
        return Machine(begin, dur, states)


def run():
    machine = read_blueprints('day25.txt')
    machine.run()
    return machine.checksum()

if __name__ == '__main__':
    print run()
