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

from ivonet.files import read_int_matrix
from ivonet.grid import Location, north, east, south, west
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def is_visible(tree_height, direction: iter) -> bool:
    for i, value in direction:
        if value >= tree_height:
            return False
    return True


def scenic_score_direction(tree_height: int, direction: iter) -> int:
    score = 0
    for i, value in direction:
        score += 1
        if tree_height <= value:
            break
    return score


def part_1(source):
    height: int = len(source)
    width: int = len(source[0])
    visible_trees: int = (height + width) * 2 - 4  # borders pre calculated
    for r in range(1, len(source) - 1):
        for c in range(1, len(source[r]) - 1):
            loc: Location = Location(r, c)
            tree_height: int = source[r][c]
            if is_visible(tree_height, north(source, loc, value=True)) or \
                    is_visible(tree_height, east(source, loc, value=True)) or \
                    is_visible(tree_height, south(source, loc, value=True)) or \
                    is_visible(tree_height, west(source, loc, value=True)):
                visible_trees += 1
    return visible_trees


def part_2(source):
    highest_scenic_score: int = 0
    for r in range(1, len(source) - 1):
        for c in range(1, len(source[r]) - 1):
            loc: Location = Location(r, c)
            tree_height: int = source[r][c]
            north_score = scenic_score_direction(tree_height, north(source, loc, value=True))
            east_score = scenic_score_direction(tree_height, east(source, loc, value=True))
            south_score = scenic_score_direction(tree_height, south(source, loc, value=True))
            west_score = scenic_score_direction(tree_height, west(source, loc, value=True))
            tree_score = north_score * east_score * south_score * west_score
            if highest_scenic_score < tree_score:
                highest_scenic_score = tree_score

    return highest_scenic_score


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_int_matrix(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_int_matrix("""30373
25512
65332
33549
35390""")

    def test_example_data_part_1(self):
        self.assertEqual(21, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(1705, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(8, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(371200, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
