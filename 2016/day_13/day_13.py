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

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def create_maze(height, width, nr=10):
    maze = []
    for h in range(height):
        row = ""
        for w in range(width):
            if bin(w * w + 3 * w + 2 * w * h + h + h * h + nr)[2:].count("1") % 2 == 0:
                row += "."
            else:
                row += "#"
        maze.append(row)
    return maze


def repr_maze(maze):
    return "\n".join("".join(row) for row in maze)


def part_1(source):
    maze = create_maze(7, 10, int(source))
    _(repr_maze(maze))
    return None


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""10""")

    def test_generate_maze(self):
        expected = """.#.####.##
..#..#...#
#....##...
###.#.###.
.##..#..#.
..##....#.
#...##.###"""
        self.assertEqual(expected, repr_maze(create_maze(7, 10, 10)))

    def test_example_data_part_1(self):
        self.assertEqual(11, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
