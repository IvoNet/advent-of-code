#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import unittest
from itertools import product
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints


def init_on(init, dimensions):
    on = set()
    for i, row in enumerate(init):
        for j, val in enumerate(row):
            if val == '#':
                on.add(tuple([i, j] + [0] * (dimensions - 2)))
    return on


def cicle(init, dimensions, steps):
    on = init_on(init, dimensions)
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
        stay_on = set(
            [loc for loc in on if loc in c.keys() and c[loc] in [2, 3]])
        turn_on = set([loc for loc, v in c.items()
                      if loc not in on and v == 3])
        on = stay_on | turn_on
    return len(on)


def part_1(data):
    return cicle(data, 3, 6)


def part_2(data):
    return cicle(data, 4, 6)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(304, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(1868, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
