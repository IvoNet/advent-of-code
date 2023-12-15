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
import os
from pathlib import Path

import pytest

from ivonet.grid import transpose

collections.Callable = collections.abc.Callable

import sys

from ivonet.files import read_rows
from ivonet.iter import ints, make_hashable

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def p(grid):
    if DEBUG:
        for row in grid:
            print("".join(row))
        print()


def parse(source):
    return [list(row) for row in source]


class SpinCycle:

    def __init__(self, source):
        self.source = source
        self.grid: list[list] = source

    def flip(self) -> SpinCycle:
        """
        This method performs a flip operation on the grid. The steps are as follows:

        1. Transpose the grid: This is done because it's easier to work with rows than columns.
        2. Sort each group in each row: The grid is iterated row by row. Each row is split into groups by the "#" character.
         Each group is sorted in descending order and then joined back together with the "#" character.
        3. Transpose the grid back: The grid is transposed back to its original orientation.

        :return: The score after performing the cycle operation.
        """

        # Transpose the grid because it is easier to work with rows than cols
        self.grid = transpose(self.grid)

        # Sort each group in each row
        self.roll_rounded_rocks()

        # Transpose the grid back
        self.grid = transpose(self.grid)
        return self

    def roll_rounded_rocks(self):
        """
        This method sorts each group in each row of the grid. The grid is iterated row by row.
        Each row is split into groups by the "#" character. Each group is sorted in descending
        order and then joined back together with the "#" character. This operation is performed
        in-place, modifying the current grid.
        """
        # Sort each group in each row
        for i in range(len(self.grid)):
            row = "".join(self.grid[i]).split("#")
            sorted_row = []
            for group in row:
                sorted_group = "".join(sorted(list(group), reverse=True))
                sorted_row.append(sorted_group)
            self.grid[i] = "#".join(sorted_row)

    def score(self):
        # Calculate and return the score
        score = 0
        height = len(self.grid)
        for r, row in enumerate(self.grid):
            # the second part of this formula calculates the difference between the total number of rows and the
            # current row index.
            round_rocks_count = row.count("O") * (height - r)
            _(f"Row {r} has {row.count('O')} rounded rocks and a score of {round_rocks_count}")
            score += round_rocks_count
        _(f"Total score: {score:>31}")
        return score

    def cycle(self) -> SpinCycle:
        """
        rotate counterclockwise 90 degrees 4 times to do a full cycle
        - north -> west -> south -> east (counterclockwise)
        so this method does that with a transpose and a reverse
        we of course do the whole rolling of rounded rocks here too
        """
        for _ in range(4):
            self.grid = transpose([list(row) for row in self.grid])
            self.roll_rounded_rocks()
            self.grid = [row[::-1] for row in self.grid]  # turn the grid 1 quarter to the left
            p(self.grid)
        return self

    def cycles(self, iterations=1_000_000_000) -> SpinCycle:
        """
        Does iterations Cycle and then calculates the load on the north beam
        but 1 billion times is a bit much and a pattern will probably emerge sooner
        remember enough cycles and the pattern will repeat itself
        """
        explored = {make_hashable(self.grid)}
        grids = [self.grid]
        cycled = 0
        while cycled < iterations:
            cycled += 1
            self.cycle()
            if make_hashable(self.grid) in explored:
                break
            explored.add(make_hashable(self.grid))
            grids.append(self.grid)

        _(f"Found a pattern after {cycled} cycles")
        pattern_idx = grids.index(self.grid)
        _(f"First occurrence at {pattern_idx}")

        self.grid = grids[(iterations - pattern_idx) % (cycled - pattern_idx) + pattern_idx]
        return self


def part_1(source):
    return SpinCycle(source).flip().score()


def part_2(source, times=1_000_000_000):
    return SpinCycle(source).cycles(times).score()


def test_puzzle(test_source, source):
    assert part_1(test_source) == 136
    assert part_1(source) == 110821
    assert part_2(test_source) == 64
    assert part_2(source) == 83516


@pytest.fixture
def day():
    return str(ints(Path(__file__).name)[0])


@pytest.fixture
def source(day):
    return read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")


@pytest.fixture
def test_source(day):
    return read_rows(f"{os.path.dirname(__file__)}/test_{day.zfill(2)}.input")
