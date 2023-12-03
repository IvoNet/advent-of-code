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
import unittest
from collections import defaultdict
from pathlib import Path
from string import digits

import sys

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True

SYMBOLS = {'#', '$', '%', '&', '*', '+', '-', '/', '=', '@'}

NEIGHBORS = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1)
]


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def create_matrix(source, symbols=None):
    if symbols is None:
        symbols = SYMBOLS
    sd = defaultdict(bool)
    for i, line in enumerate(source):
        for j, c in enumerate(line):
            if c in symbols:
                sd[(i, j)] = True
    return sd


def check_neighbor_symbol(pos, sd):
    for x, y in pos:
        for a, b in NEIGHBORS:
            if (x + a, y + b) in sd:
                return True
    return False


def check_neighbor_gears(gear_cords, number_with_positions):
    options = []
    xg, yg = gear_cords
    for number, positions in number_with_positions:
        for row, col in NEIGHBORS:
            if (xg + row, yg + col) in positions:
                options.append(number)
                break
    if len(options) == 2:
        return options[0] * options[1]
    return 0


def gear_coordinates(source):
    gears = []
    for row, line in enumerate(source):
        for col, c in enumerate(line):
            if c == '*':
                gears.append((row, col))
    return gears


def number_coordinates(source: list[str]) -> list[tuple[int, list[tuple]]]:
    """Returns a list of tuples with the number and the coordinates of the number"""
    numbers_with_positions: list[tuple[str, list[tuple]]] = []
    tmp_nr = ''
    pos = []
    # prepare the number with positions
    for row, line in enumerate(source):
        if tmp_nr:
            numbers_with_positions.append((int(tmp_nr), pos))
            tmp_nr = ''
            pos = []
        for col, character in enumerate(line):
            if tmp_nr and character not in digits:
                numbers_with_positions.append((int(tmp_nr), pos))
                tmp_nr = ''
                pos = []
            if character in digits:
                tmp_nr += character
                pos.append((row, col))
    return numbers_with_positions


def part_1(source) -> int:
    matrix = create_matrix(source)
    numbers_with_coordinates = number_coordinates(source)
    answer = 0
    for number, positions in numbers_with_coordinates:
        if check_neighbor_symbol(positions, matrix):
            answer += number
    return answer


def part_2(source) -> int:
    numbers_with_coordinates = number_coordinates(source)
    gear_locations = gear_coordinates(source)
    answer = 0
    for gear in gear_locations:
        answer += check_neighbor_gears(gear, numbers_with_coordinates)
    return answer


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""")
        self.test_source2 = read_rows("""""")

    def test_example_data_part_1(self):
        self.assertEqual(4361, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(520019, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(467835, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(75519888, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
