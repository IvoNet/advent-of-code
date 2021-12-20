#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
from itertools import product
from pprint import pprint

from ivonet.files import read_rows


def initOn(init, dimensions):
    on = set()
    for i, row in enumerate(init):
        for j, val in enumerate(row):
            if val == '#':
                on.add(tuple([i, j] + [0] * (dimensions - 2)))
    return on


def cicle(init, dimensions, steps):
    on = initOn(init, dimensions)
    for _ in range(steps):
        c = {}
        for loc in on:
            for neighbor in product([-1, 0, 1], repeat=dimensions):
                new = tuple(map(sum, zip(loc, neighbor)))
                if new != loc:
                    if new not in c.keys():
                        c[new] = 1
                    else:
                        c[new] += 1
        stayOn = set(
            [loc for loc in on if loc in c.keys() and c[loc] in [2, 3]])
        turnOn = set([loc for loc, v in c.items()
                      if loc not in on and v == 3])
        on = stayOn | turnOn
    return len(on)


def part_1(data):
    return cicle(data, 3, 6)


def part_2(data):
    return cicle(data, 4, 6)


def test():
    pprint(list(product([-1, 0, 1], repeat=2)))

    sys.exit()


if __name__ == '__main__':
    test()
    source = read_rows("day_17.input")
    print("Part 1:", part_1(source))  #
    print("part 2:", part_2(source))  #
