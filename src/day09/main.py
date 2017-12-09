
def get_char_stream(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return fp.read()


def push(stack, state):
    stack.append(state)


def pop(stack, _):
    stack.pop()


def no_op(*_):
    pass


class InsideGarbage:
    def __init__(self):
        pass

    def next(self, char):
        if char == '!':
            return InsideNot(), push, 0
        if char == '>':
            return self, pop, 0
        return self, no_op, 0


class InsideGroup:
    def __init__(self, val):
        self.val = val

    def next(self, char):
        if char == '!':
            return InsideNot(), push, 0
        if char == '<':
            return InsideGarbage(), push, 0
        if char == '{':
            return InsideGroup(self.val + 1), push, 0
        if char == '}':
            return self, pop, self.val
        return self, no_op, 0


class InsideNot:
    def __init__(self):
        pass

    def next(self, char):
        return self, pop, 0


class Start:
    def __init__(self):
        pass

    def next(self, char):
        if char == '{':
            return InsideGroup(1), push, 0
        return self, no_op, 0


def run():
    stream = get_char_stream('day9.txt')
    state_stack = [Start()]
    score = 0
    for char in stream:
        state, op, to_add = state_stack[-1].next(char)
        op(state_stack, state)
        score += to_add
    return score


if __name__ == '__main__':
    print run()
