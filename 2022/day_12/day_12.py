#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import sys
import unittest
from pathlib import Path
from typing import Callable

from ivonet import infinite
from ivonet.alphabet import alphabet
from ivonet.files import read_rows
from ivonet.grid import Location, neighbors_defined_grid
from ivonet.iter import ints
from ivonet.search import bfs, node_to_path

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def is_goal(goal: Location) -> Callable[[Location], bool]:
    """Returns a function that tests if a given location is the goal."""

    def reached(current: Location) -> bool:
        return current == goal

    return reached


def successors(matrix: list[list[int]]) -> Callable[[Location], list[Location]]:
    """Finds the viable successor location from the given location.
    Only up, down, left and right are allowed.
    But only if that direction is at max 1 elevation higher than the given location.
    It may be lower to any degree.
    """

    def adjacent(ml: Location) -> list[Location]:
        nb = [Location(r, c) for r, c in
              neighbors_defined_grid(Location(ml.row, ml.col), grid=(len(matrix), len(matrix[0])), diagonal=False)]

        return [n for n in nb if matrix[n.row][n.col] <= matrix[ml.row][ml.col] + 1]

    return adjacent or []


def read_matrix(source):
    matrix: list[list[int]] = []
    start: Location = Location(0, 0)
    goal: Location = Location(0, 0)
    possible_starting_points: list[Location] = []
    for r, row in enumerate(source):
        new = []
        for c, col in enumerate(row):
            if col == "a":
                possible_starting_points.append(Location(r, c))
            if col == "S":
                start = Location(r, c)
                new.append(alphabet().index("a"))
                continue
            if col == "E":
                goal = Location(r, c)
                new.append(alphabet().index("z"))
                continue
            new.append(alphabet().index(col))
        matrix.append(new)
    return start, goal, matrix, possible_starting_points


def part_1(source):
    start, goal, matrix, __ = read_matrix(source)
    solution = bfs(start,
                   is_goal(goal),
                   successors(matrix))
    pad = node_to_path(solution)
    return len(pad) - 1  # do not count the start state


def part_2(source):
    _, goal, matrix, possible_starting_points = read_matrix(source)
    shortest = infinite
    for start in possible_starting_points:
        solution = bfs(start,
                       is_goal(goal),
                       successors(matrix))
        if solution:
            length = len(node_to_path(solution)) - 1
            if shortest > length:
                shortest = length
    return shortest


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""")

    def test_example_data_part_1(self):
        self.assertEqual(31, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(361, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(29, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(354, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
