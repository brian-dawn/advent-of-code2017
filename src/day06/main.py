

def get_memory_banks(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        return map(int, fp.read().split('\t'))


def str_mem(memory):
    return ''.join(map(str, memory))


def run():
    memory = get_memory_banks('day6.txt')
    mem_length = len(memory)
    current_memory = memory[:]
    past_mem = set()
    count = 0
    while str_mem(current_memory) not in past_mem:
        count += 1
        past_mem.add(str_mem(current_memory))
        idx = memory.index(max(memory))
        block = memory[idx]
        memory[idx] = 0
        while block:
            block -= 1
            idx += 1
            memory[idx % mem_length] += 1
        current_memory = memory[:]
    return count


def run_2():
    memory = get_memory_banks('day6.txt')
    mem_length = len(memory)
    current_memory = memory[:]
    past_mem = {}
    count = 0
    while str_mem(current_memory) not in past_mem:
        count += 1
        past_mem[str_mem(current_memory)] = count
        idx = memory.index(max(memory))
        block = memory[idx]
        memory[idx] = 0
        while block:
            block -= 1
            idx += 1
            memory[idx % mem_length] += 1
        current_memory = memory[:]
    return count - past_mem[str_mem(current_memory)] + 1

if __name__ == '__main__':
    print run()
    print run_2()