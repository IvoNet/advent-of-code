#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
These two helped in my thought process.
Still had to find out this formula on my onw though...
https://stackoverflow.com/questions/36834505/creating-a-spiral-array-in-python
https://www.py4u.net/discuss/158349
"""

import os
import sys
import unittest
from math import sqrt, ceil
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


NORTH, S, W, E = (0, -1), (0, 1), (-1, 0), (1, 0)  # directions
turn_right = {NORTH: E, E: S, S: W, W: NORTH}  # old -> new direction


def spiral(width, height):
    if width < 1 or height < 1:
        raise ValueError
    x, y = width // 2, height // 2  # start near the center
    dx, dy = NORTH  # initial direction
    matrix = [[None] * width for _ in range(height)]
    count = 0
    while True:
        count += 1
        matrix[y][x] = count  # visit
        # try to turn right
        new_dx, new_dy = turn_right[dx, dy]
        new_x, new_y = x + new_dx, y + new_dy
        if (0 <= new_x < width and 0 <= new_y < height and
                matrix[new_y][new_x] is None):  # can turn right
            x, y = new_x, new_y
            dx, dy = new_dx, new_dy
        else:  # try to move straight
            x, y = x + dx, y + dy
            if not (0 <= x < width and 0 <= y < height):
                return matrix  # nowhere to go


def print_matrix(matrix):
    width = len(str(max(el for row in matrix for el in row if el is not None)))
    fmt = "{:0%dd}" % width
    for row in matrix:
        print(" ".join("_" * width if el is None else fmt.format(el) for el in row))


class MazeLocation(NamedTuple):
    row: int
    col: int


def manhattan_distance(start: MazeLocation, goal: MazeLocation) -> float:
    xdist: int = abs(start.col - goal.col)
    ydist: int = abs(start.row - goal.row)
    return xdist + ydist


def part_1(source):
    """This is doing it by actually creating the spiral
    Works like a charm but should also be calculable right?
    see my trials in part_1a
    """
    nr = int(source)
    width = int(ceil(sqrt(nr)))
    matrix = spiral(width, width)
    start = None
    goal = None
    for h, row in enumerate(matrix):
        if nr in row:
            start = MazeLocation(h, row.index(nr))
        if 1 in row:
            goal = MazeLocation(h, row.index(1))
    _(start, goal)
    return manhattan_distance(start, goal)


def part_1a(source):
    """My observations of this problem as I am thinking them so you see the process I am going through
    - the width I kinda found out by trial and error at first by creating a spiral way big enough and actually printing
      it to file. I proved not to be as difficult 600 * 600 was big enough as 360000 contains my number ... square root?
      Tried it and failed because of rounding stuff so a plus 1 issue that worked. that led me to the ceil function
    - now I know that at the center of this spiral my value 1 is that is width // 2 = 285
    - that would make row of 'source'=0 and row of '1'=285 that is half of the manhatten distance. How to get the cols
    - the '1' is easy as it is the actual center and that would make the col also  width // 2 = 285
    - which col for 'source' though
                                    21 -22- 23- 24- 25
                                     |
                                    20   7 - 8 - 9 - 10
                                     |   |           |
                                     19  6   1 - 2   11
                                     |   |       |   |
                                     18  5 - 4 - 3   12
                                     |               |
                                     17-16 -15 -14 - 13

     [1] is a square -> NxN = 1x1
     [1,2,3,4] is a square -> (N+1)x(N+1) = 2x2
     [1,2,3,4,5,6,7,8,9] is also a square ->  (N+1)x(N+1) = 3x3
     [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16] is also a square  (N+1)x(N+1) = 4x4
     [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25] is also a square (N+1)x(N+1) = 5x5
     - if odd then top right corner of a square (e.g 1x1, 3x3, ...)
       if even then bottom left corner of a square, but what does that mean? (e.g 2x2, 4,4, ...)
     - corner formulae? just observations in hope of enlightenment :-)
       top corner row 0 (value 1) -> 1  = 1x1 -> row 0 , col 0 do we count cols in both directions?
       bottom left row down 1     -> 4  = 2x2 -> row -1, col 0
       top right corner row up 1  -> 9  = 3x3 -> row 1 , col 1
       down 2                     -> 16 = 4x4 -> row -2, col -1
       up 2                       -> 25 = 5x5 -> row 3 , col 3
       down 3                     -> 36 = 6x6 -> row -3, vol -2
       up 3                       -> 49 = 7x7 -> row 4 , col 4

       but rows and cols are actually always positive (like folding them over row 0?) is 3 "the same" as 9? YES!
       top corner row 1 (value 9)-> (row * 2 + 1) ** 2 -> (1*2+1)**2 = 9
       'top' corner row 1 (value 3) -> (row * 2 + 1) ** 2 -> (1*2+1)**2 = 9

       if I can find the "center" of any row (going to nr one) than we can start calculating stuff as that is the
       turning point of a manhatten distance to start walking to the center

       25 has centers [23, 19, 15, 11] row len = 5 -> 5 //2 = 2 -> 25 - 2 = 23 -> 23 - rowlen = 18 nope damn
                 row len to the corner-> (5 // 2) * 2 = 4 -> 25 - rowlen//2 = 23 -> 23 - rowlen -> 19 - rowlen ->15...
       9 has centers [8, 6, 4, 2]
                 row len to the corner-> (3 // 2) * 2 = 2 -> 9 - rowlen//2 = 8 -> 8 - rowlen -> 6 - rowlen ->4...
       every corner of every square has 4 centers except for the first two squares

       number_to_place -> 325489
       row = int(ceil(sqrt(nr_to_place))) // 2
       corner_number (of row is row in reverse) = (row * 2 + 1) ** 2
       row_len = row * 2
       centers = [corner - row_len//2 - row_len * i for i in range(4)] I think?
       The centers are the actual number of that square so if our number falls within it we only have to
       calc the distance to between those two and then to the center
       We need to find the minimal distance from our number to place to one of the squares

       dist_to_center = min((nnr_to_place - center) for center in centers) <- almost! distances are never negative!
       then the manhatten distance is the row + dist_to_center
       lets try this shizzle

       I was way quicker in the brute force version :-)
    """
    nr_to_place = int(source)
    row = int(ceil(sqrt(nr_to_place))) // 2
    corner = (row * 2 + 1) ** 2
    row_len = row * 2
    centers = list(corner - row_len // 2 - row_len * i for i in range(4))
    dist_to_center = min(abs(nr_to_place - center) for center in centers)
    return row + dist_to_center


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(552, part_1(self.source))

    def test_part_1a(self):
        self.assertEqual(552, part_1a(self.source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
