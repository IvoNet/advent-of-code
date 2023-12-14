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
from ivonet.grid import DIRECTIONS, Location
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def parse_symbols(source):
    """Returns a list of all the symbols in the grid"""
    symbols = ""
    for line in source:
        for c in line:
            if c not in digits + '.':
                symbols += c
    return symbols


def symbol_matrix(source) -> defaultdict:
    """Returns a matrix of all the symbols in the grid"""
    matrix: defaultdict = defaultdict(bool)
    symbols = parse_symbols(source)
    for i, line in enumerate(source):
        for j, c in enumerate(line):
            if c in symbols:
                matrix[Location(i, j)] = True  # faster than list
    return matrix


def check_neighbor_to_symbol(positions: list[Location], matrix: defaultdict):
    """Checks if any of the neighbors of the positions are in the matrix.
    The idea is that if even one of the coordinates is next to a symbol it is a valid part number."""
    for pos in positions:
        for direction in DIRECTIONS.values():
            if matrix[pos + direction]:
                return True
    return False


def check_gear(gear: Location,
               number_with_positions: list[tuple[int, list[Location]]]):
    """Checks if the gear is next to exactly two numbers and returns the multiplication of those numbers if true"""
    options: list[int] = []
    for number, positions in number_with_positions:
        for neighbor in DIRECTIONS.values():
            if gear + neighbor in positions:
                options.append(number)
                break
    if len(options) == 2:
        return options[0] * options[1]
    return 0


def gear_coordinates(source):
    """Returns a list of all the gears with their coordinates in the grid"""
    gears: defaultdict = defaultdict(bool)
    for row, line in enumerate(source):
        for col, c in enumerate(line):
            if c == '*':
                gears[(Location(row, col))] = True  # faster than list
    return gears


def number_coordinates(source: list[str]) -> list[tuple[int, list[Location]]]:
    """Returns a list of all the numbers with their coordinates in the grid"""
    numbers_with_positions: list[tuple[int, list[Location]]] = []
    tmp_nr: str = ''
    pos: list[Location] = []
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
                pos.append(Location(row, col))
    return numbers_with_positions


def part_1(source) -> int:
    numbers_with_coordinates = number_coordinates(source)
    matrix = symbol_matrix(source)
    answer = 0
    for number, positions in numbers_with_coordinates:
        if check_neighbor_to_symbol(positions, matrix):
            answer += number
    return answer


def part_2(source) -> int:
    numbers_with_coordinates = number_coordinates(source)
    gear_locations = gear_coordinates(source)
    answer = 0
    for gear in gear_locations:
        answer += check_gear(gear, numbers_with_coordinates)
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
