import collections


def _get_program_stacks(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        for line in fp.readlines():
            line = line.strip('\n')
            name, line = line.split(' (')
            maybe_list = line.split('-> ')
            weight = maybe_list[0].strip().strip(')')
            names = []
            if len(maybe_list) > 1:
                names = maybe_list[1].split(', ')
            yield name, int(weight), names


def get_program_stacks():
    return [a for a in _get_program_stacks('day7.txt')]


def find_root_node(stack_list):
    for name, _, _ in stack_list:
        good = True
        for _, _, names in stack_list:
            if name in names:
                good = False
                break
        if good:
            return name


def run():
    return find_root_node(get_program_stacks())


class DiscTree:
    def __init__(self, name, weight, children):
        self.name = name
        self.children = children
        self.weight = weight
        self.full_weight = weight + sum([child.full_weight for child in children])

    def find_unbalanced_tree(self):
        if not self.children:
            return None, True
        if len(set([child.full_weight for child in self.children])) == 1:
            return self, False
        for child in self.children:
            maybe_result, done = child.find_unbalanced_tree()
            if maybe_result:
                return (maybe_result, True) if done else (self, True)

    def __str__(self):
        return self.name + ' ' + str(self.weight) + ' ' + str(self.full_weight) + '\n' + '\n'.join(str(child) for child in self.children)


def build_tree(tree_dict, root_node_name):
    return DiscTree(root_node_name,
                    tree_dict[root_node_name][0],
                    [build_tree(tree_dict, name) for name in tree_dict[root_node_name][1]])


def adjusted_weight(tree, target_weight):
    print tree.weight, target_weight, tree.full_weight, tree.name
    return tree.weight - (tree.full_weight - target_weight)


def run_2():
    stacks = get_program_stacks()
    tree_dict = {}
    for name, weight, children in stacks:
        tree_dict[name] = weight, children
    tree = build_tree(tree_dict, find_root_node(stacks))
    unbal_tree, _ = tree.find_unbalanced_tree()
    counter = collections.Counter([child.full_weight for child in unbal_tree.children])
    good, bad = 0, 0
    for key in counter:
        if counter[key] == 1:
            bad = key
        else:
            good = key
    return adjusted_weight([child for child in unbal_tree.children if child.full_weight == bad][0], good)


if __name__ == '__main__':
    print run()
    print run_2()
