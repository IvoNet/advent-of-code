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
from enum import Enum
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Direction(str, Enum):
    UP = "u"
    DOWN = "d"
    LEFT = "l"
    RIGHT = "r"


def walk_route(source, part1=True):
    row = 0
    col = source[row].index("|")
    current_char = "|"
    direction = Direction.DOWN
    route = []
    steps = 0
    while current_char != " ":
        steps += 1
        if current_char == "+":
            if direction in "du":
                direction = Direction.LEFT if source[row][col - 1] != ' ' else Direction.RIGHT
            else:
                direction = Direction.UP if source[row - 1][col] != ' ' else Direction.DOWN
        elif current_char not in "|-":
            route.append(current_char)
        if direction == Direction.DOWN:
            row += 1
        elif direction == Direction.UP:
            row -= 1
        elif direction == Direction.LEFT:
            col -= 1
        elif direction == Direction.RIGHT:
            col += 1
        current_char = source[row][col]
    if part1:
        return "".join(route)
    return steps


def parse(source):
    data = [x for x in source.splitlines(keepends=False)]
    width = max(len(x) for x in data)
    data = [list(x.ljust(width, " ")) for x in data]
    return data


def part_1(source):
    return walk_route(parse(source))


def part_2(source):
    return walk_route(parse(source), part1=False)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input", raw=True)
        self.test_source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test_a.input", raw=True)

    def test_example_data_part_1(self):
        self.assertEqual("ABCDEF", part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual("PBAZYFMHT", part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(38, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(16072, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
