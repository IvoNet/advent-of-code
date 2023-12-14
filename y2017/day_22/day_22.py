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
from collections import defaultdict
from enum import Enum
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source: list[str]) -> dict[tuple[int, int], int]:
    matrix = defaultdict(int)
    for r, row in enumerate(source):
        for c, col in enumerate(row):
            matrix[(r, c)] = 1 if col == "#" else 0
    return matrix


class Directions(str, Enum):
    UP = "u"
    LEFT = "l"
    DOWN = "d"
    RIGHT = "r"


DIRECTIONS = {Directions.RIGHT: (0, 1), Directions.DOWN: (1, 0), Directions.LEFT: (0, -1), Directions.UP: (-1, 0)}


def turn_2(state, direction: Directions):
    dirs = {(0, direction.UP): direction.LEFT,
            (0, direction.RIGHT): direction.UP,
            (0, direction.LEFT): direction.DOWN,
            (0, direction.DOWN): direction.RIGHT,

            (1, direction.UP): direction.RIGHT,
            (1, direction.RIGHT): direction.DOWN,
            (1, direction.LEFT): direction.UP,
            (1, direction.DOWN): direction.LEFT,

            (2, direction.UP): direction.UP,
            (2, direction.RIGHT): direction.RIGHT,
            (2, direction.LEFT): direction.LEFT,
            (2, direction.DOWN): direction.DOWN,

            (3, direction.UP): direction.DOWN,
            (3, direction.RIGHT): direction.LEFT,
            (3, direction.LEFT): direction.RIGHT,
            (3, direction.DOWN): direction.UP}

    return dirs[state, direction]


def turn_1(direction: Directions, heading: Directions):
    gps = {(Directions.UP, Directions.RIGHT): Directions.RIGHT,
           (Directions.RIGHT, Directions.RIGHT): Directions.DOWN,
           (Directions.DOWN, Directions.RIGHT): Directions.LEFT,
           (Directions.LEFT, Directions.RIGHT): Directions.UP,
           (Directions.UP, Directions.LEFT): Directions.LEFT,
           (Directions.LEFT, Directions.LEFT): Directions.DOWN,
           (Directions.DOWN, Directions.LEFT): Directions.RIGHT,
           (Directions.RIGHT, Directions.LEFT): Directions.UP}
    return gps[(direction, heading)]


def part_1(source, bursts=10000):
    matrix: dict[tuple[int, int], int] = parse(source)
    d: Directions = Directions.UP
    row = len(source) // 2
    col = len(source) // 2
    infected: int = 0
    for _ in range(bursts):
        if matrix[(row, col)] == 1:
            matrix[(row, col)] = 0
            d = turn_1(d, d.RIGHT)
        elif matrix[(row, col)] == 0:
            matrix[(row, col)] = 1
            d = turn_1(d, d.LEFT)
            infected += 1
        coord = DIRECTIONS[d]
        row += coord[0]
        col += coord[1]
    return infected


def part_2(source, bursts=10000000):
    matrix: dict[tuple[int, int], int] = parse(source)
    d: Directions = Directions.UP
    row = len(source) // 2
    col = len(source) // 2
    infected: int = 0
    for _ in range(bursts):
        if matrix[(row, col)] == 1:
            matrix[(row, col)] = 3  # formally infected
            d = turn_2(1, d)
        elif matrix[(row, col)] == 0:
            matrix[(row, col)] = 2  # Weakened
            d = turn_2(0, d)
        elif matrix[(row, col)] == 2:
            matrix[(row, col)] = 1  # Infected
            infected += 1
            d = turn_2(2, d)
        elif matrix[(row, col)] == 3:
            matrix[(row, col)] = 0  # Cleaned
            d = turn_2(3, d)
        else:
            raise ValueError("Should not happen")
        coord = DIRECTIONS[d]
        row += coord[0]
        col += coord[1]
    return infected


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""..#
#..
...""")

    def test_example_data_part_1(self):
        self.assertEqual(5, part_1(self.test_source, bursts=7))

    def test_example_data_1_part_1(self):
        self.assertEqual(41, part_1(self.test_source, bursts=70))

    def test_example_data_2_part_1(self):
        self.assertEqual(5587, part_1(self.test_source, bursts=10000))

    def test_part_1(self):
        self.assertEqual(5369, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(2511944, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2510774, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
