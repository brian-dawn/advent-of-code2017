from collections import namedtuple
import regex as re
import sys
import operator

Coord = namedtuple('Coord', ['x', 'y', 'z'])
Particle = namedtuple('Particle', ['num', 'p', 'v', 'a'])
Func_Particle = namedtuple('Func_Particle', ['num', 'func'])

PATTERN = re.compile(r'p=<(.*),(.*),(.*)>, v=<(.*),(.*),(.*)>, a=<(.*),(.*),(.*)>')


def parse(i_line):
    i, line = i_line
    m = PATTERN.search(line)
    return Particle(num=int(i),
                    p=Coord(*(int(m.group(i)) for i in range(1, 4))),
                    v=Coord(*(int(m.group(i)) for i in range(4, 7))),
                    a=Coord(*(int(m.group(i)) for i in range(7, 10))))


def to_func(coeffs):
    p, v, a = coeffs
    return lambda t: p + (v + 0.5 * a) * t + 0.5 * a * t**2


def coords_to_func(p_initial, v_initial, a_initial):
    return lambda t: (f(t) for f in map(to_func, zip(p_initial, v_initial, a_initial)))


def parse_func(i_line):
    i, line = i_line
    m = PATTERN.search(line)
    return Func_Particle(num=int(i),
                         func=coords_to_func(
                             Coord(*(int(m.group(i)) for i in range(1, 4))),
                             Coord(*(int(m.group(i)) for i in range(4, 7))),
                             Coord(*(int(m.group(i)) for i in range(7, 10)))
                         ))


def read_particles(file_name, func=False):
    mapper = parse_func if func else parse
    with open('../../resources/' + file_name, 'r') as fp:
        return map(mapper, enumerate(fp.readlines()))


def run():
    particles = read_particles('day20.txt')
    dist = sys.maxint
    part = 0
    for particle in particles:
        if sum(map(abs, particle.a)) < dist:
            dist = sum(map(abs, particle.a))
            part = particle.num
    return part


def add_coord(coord1, coord2):
    return tuple(map(operator.add, coord1, coord2))


def run_2():
    particle_map = {particle.num: particle for particle in read_particles('day20.txt')}
    for t in range(100):
        pos_map = {}
        for num in particle_map:
            particle = particle_map[num]
            new_v = add_coord(particle.v, particle.a)
            new_p = add_coord(particle.p, new_v)
            particle_map[num] = Particle(num=num, p=new_p, v=new_v, a=particle.a)
            try:
                part_nums = pos_map[new_p]
            except KeyError:
                part_nums = []
                pos_map[new_p] = part_nums
            part_nums.append(num)
        for _, part_nums in pos_map.iteritems():
            if len(part_nums) > 1:
                for num in part_nums:
                    del particle_map[num]
    return len(particle_map)


if __name__ == '__main__':
    print run()
    print run_2()
