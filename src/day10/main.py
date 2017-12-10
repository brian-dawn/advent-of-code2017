
def length_list(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return map(int, fp.read().split(','))


class Node:
    def __init__(self, val, prev):
        self.val = val
        self.prev = prev
        self.next = None
        self.is_head = False

    def flip(self):
        self.prev, self.next = self.next, self.prev

    def nth(self, n):
        return self.next.nth(n - 1) if n else self

    def to_str(self, length):
        return str(self.val) + ((', ' + self.next.to_str(length - 1)) if length - 1 else '')


def looped_list(length):
    head = Node(0, None)
    head.is_head = True
    cur = head
    for i in range(1, length):
        new = Node(i, cur)
        cur.next = new
        cur = new
    cur.next = head
    head.prev = cur
    return head


def flip_section(start_node, length):

    end = start_node.nth(length - 1)
    print start_node.val, end.val


def run():
    lengths = length_list('day10.txt')
    head = looped_list(256)
    cur = head
    flip_section(cur, 3)
    for length in lengths:
        pass

if __name__ == '__main__':
    print run()
