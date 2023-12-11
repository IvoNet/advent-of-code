#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2023 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import collections
import itertools
import os
import sys
import unittest
from pathlib import Path

from ivonet.grid import Location

collections.Callable = collections.abc.Callable
from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def manhattan(expand_columns: list[int], expand_rows: list[int], galaxy_left: Location, galaxy_right: Location,
              expand_times: int):
    """
    expand_times is added for every x in expand_columns and y in expand_rows that lies between galaxy_left
    and galaxy_right (or vice versa). This means that expand_times is added for every row and column that
    is expanded and lies between the two galaxies.
    """
    total = abs(galaxy_left.row - galaxy_right.row) + abs(galaxy_left.col - galaxy_right.col)

    for x in expand_columns:
        if (galaxy_left.row <= x <= galaxy_right.row) or (galaxy_left.row > x > galaxy_right.row):
            total += 1 + 0 if expand_times == 0 else expand_times - 1

    for y in expand_rows:
        if (galaxy_left.col <= y <= galaxy_right.col) or (galaxy_left.col > y > galaxy_right.col):
            total += 1 + 0 if expand_times == 0 else expand_times - 1

    return total


def galaxy_distances_v1(source, expand_times=1000000):
    """ same as galaxy_distances but with a lot of list comprehension implementation """
    universe = [line.strip() for line in source]
    galaxies = [Location(x, y) for y, line in enumerate(universe) for x, ch in enumerate(line) if ch == '#']
    expand_columns = [j for j in range(len(universe[0])) if len(set(x[j] for x in universe)) == 1]
    expand_rows = [j for j, line in enumerate(universe) if "#" not in line]
    return sum(manhattan(expand_columns, expand_rows, p[0], p[1], expand_times) for p in
               itertools.combinations(galaxies, 2))


def galaxy_distances(source, expand_times=1000000):
    """
    This function calculates the total distance between all pairs of galaxies in the given universe.

    Parameters:
    source (list): A list of strings representing the universe. Each string is a row in the universe,
                   and each character in the string is a cell in that row. A '#' character represents a galaxy.
    expand_times (int): The number of times the universe expands. Default is 1000000.

    Returns:
    total (int): The total distance between all pairs of galaxies.

    The function works as follows:
    1. It first converts the source into a list of strings where each string represents a row in the universe.
    2. It then finds the coordinates of all galaxies in the universe and stores them in the 'galaxies' list.
    3. It identifies all columns and rows that can be expanded (i.e., they contain only one type of cell)
       and stores their indices in the 'expand_columns' and 'expand_rows' lists, respectively.
    4. It then calculates the total distance between all pairs of galaxies. The distance between two galaxies
       is the Manhattan distance between them, plus the number of times the universe expands for every row and
       column that lies between the two galaxies and can be expanded.
    5. The function returns the total distance between all pairs of galaxies.
    """
    # function implementation...
    universe = []
    for line in source:
        universe.append(line.strip())

    galaxies = []
    for y, line in enumerate(universe):
        for x, ch in enumerate(line):
            if ch == '#':
                galaxies.append(Location(x, y))

    expand_columns = []
    for j in range(len(universe[0])):
        column_set = set()
        for x in universe:
            column_set.add(x[j])
        if "#" not in column_set:
            expand_columns.append(j)

    expand_rows = []
    for j, line in enumerate(universe):
        if "#" not in line:
            expand_rows.append(j)

    total = 0
    for p in itertools.combinations(galaxies, 2):
        total += manhattan(expand_columns, expand_rows, p[0], p[1], expand_times)

    return total


def part_1(source):
    """
    - expand universe
    - find galaxies
    - find pairs of galaxies
    - find shortest path between pairs of galaxies (manhattan distance with a twist)
    - What is the sum of these lengths?
    """
    return galaxy_distances(source, 0)


def part_2(source, times=1000000):
    """
    same as part_1 but with more expansion
    """
    return galaxy_distances(source, times)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""")
        self.test_source2 = read_rows("""""")

    def test_example_data_part_1(self):
        self.assertEqual(374, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(10077850, part_1(self.source))

    def test_example_data_part_2_1(self):
        self.assertEqual(1030, part_2(self.test_source, 10))

    def test_example_data_part_2_2(self):
        self.assertEqual(8410, part_2(self.test_source, 100))

    def test_part_2(self):
        self.assertEqual(504715068438, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
