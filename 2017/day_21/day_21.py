#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

BASE_GRID = [
    ".#.",
    "..#",
    "###",
]

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def diagonal(key):
    new_key = []
    for x in range(len(key)):
        tmp = []
        for y in range(len(key)):
            tmp.append(key[y][x])
        new_key.append("".join(tmp))
    return tuple(new_key)


def parse(source):
    rules = {}
    for line in source:
        k, v = line.strip().split(" => ")
        k = tuple(k.split("/"))
        v = v.split("/")
        rules[k] = v
        rules[diagonal(k)] = v

        k2 = tuple([s[::-1] for s in k])
        rules[k2] = v
        rules[diagonal(k2)] = v

        k3 = tuple(s for s in k[::-1])
        rules[k3] = v
        rules[diagonal(k3)] = v

        k4 = tuple([s[::-1] for s in k3])
        rules[k4] = v
        rules[diagonal(k4)] = v
    return rules


class ArtProgram:

    def __init__(self, rules, base=BASE_GRID) -> None:
        self.rules = rules
        self.grid = base
        self.index = 1

    def step(self, times=1):
        for _ in range(times):
            self.enhance()

    def enhance(self):
        if len(self.grid) % 2 == 0:
            return self.enhance_even()
        elif len(self.grid) % 3 == 0:
            return self.enhance_odd()
        else:
            raise ValueError("Bad dimensions")

    def enhance_odd(self):
        _("Enhance odd")
        new_grid = []
        for h in range(0, len(self.grid), 3):
            new_lines = [[], [], [], []]
            for w in range(0, len(self.grid), 3):
                k = tuple([self.grid[h][w:w + 3], self.grid[h + 1][w:w + 3], self.grid[h + 2][w:w + 3]])
                v = self.rules[k]
                for i, l in enumerate(v):
                    new_lines[i].extend(list(l))
            new_grid.extend(["".join(l) for l in new_lines])
        self.grid = new_grid

    def enhance_even(self):
        _("Enhance even")
        new_grid = []
        for h in range(0, len(self.grid), 2):
            new_lines = [[], [], []]
            for w in range(0, len(self.grid), 2):
                k = tuple([self.grid[h][w:w + 2], self.grid[h + 1][w:w + 2]])
                v = self.rules[k]
                for i, l in enumerate(v):
                    new_lines[i].extend(list(l))
            new_grid.extend(["".join(l) for l in new_lines])
        self.grid = new_grid

    def lit_pixels(self):
        return sum([sum([c == "#" for c in l]) for l in self.grid])

    def __repr__(self) -> str:
        return repr(self.grid)


def part_1(source, times=5):
    rules = parse(source)
    art_program = ArtProgram(rules)
    art_program.step(times)
    return art_program.lit_pixels()


def part_2(source, times=18):
    return part_1(source, times=times)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test.input")

    def test_example_data_part_1(self):
        self.assertEqual(12, part_1(self.test_source, times=2))

    def test_part_1(self):
        self.assertEqual(171, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(2498142, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
