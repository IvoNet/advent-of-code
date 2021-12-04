#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
##############################################################################
# Part 1
##############################################################################

##############################################################################
# Part 2
##############################################################################

"""

import unittest

from ivonet import read_data

VALUE_IDX = 0
MARK_IDX = 1


def parse(data: str):
    """Make the data usable by parsing it into the needed components"""
    source = data.split("\n\n")
    draws = [int(x) for x in source[0].strip().split(",")]
    data1 = source[1:]
    puzzles1 = []
    for record in data1:
        puzzle = []
        for row in record.split("\n"):
            puzzle.append([[int(x1), 0] for x1 in row.strip().replace("  ", " ").replace(" ", ",").split(",")])
        puzzles1.append(puzzle)
    puzzles = puzzles1
    return draws, puzzles


def mark(puzzle: list[list[list[int]]], draw: int) -> list[list[list[int]]]:
    """Mark your bingo chart on the draw if it is in the puzzle"""
    for row in puzzle:
        for col in row:
            if col[VALUE_IDX] == draw:
                col[MARK_IDX] = 1
    return puzzle


def check_horizontal(puzzle: list[list[list[int]]]) -> bool:
    """If the sum of all marks per row is equal to the length
    of the row all are marked and we have a winner.
    """
    for row in puzzle:
        if sum(x[MARK_IDX] for x in row) == len(row):
            return True
    return False


def check_vertical(puzzle: list[list[list[int]]]) -> bool:
    """If the sum of marked position per index per row is equal to the number of rows in the puzzle
    we have a winner in the vertical way.
    """
    for i in range(len(puzzle)):
        if sum(row[i][MARK_IDX] for row in puzzle) == len(puzzle):
            return True
    return False


def sum_only_mark(puzzle: list[list[list[int]]], mark: int = 0) -> int:
    """Sum of al unmarked numbers in the puzzle."""
    return sum(col for row in puzzle for col, marked in row if marked == mark)


def part_1(data: str) -> int:
    """Find the first puzzle to win"""
    draws, puzzles = parse(data)
    for draw in draws:
        for puzzle in puzzles:
            marked_puzzle = mark(puzzle, draw)
            if check_horizontal(marked_puzzle) or check_vertical(marked_puzzle):
                return draw * sum_only_mark(puzzle)


def part_2(data: str) -> int:
    """Find the last puzzle to complete"""
    draws, puzzles = parse(data)
    for draw in draws:
        for puzzle in puzzles[::]:
            marked_puzzle = mark(puzzle, draw)
            if check_horizontal(marked_puzzle) or check_vertical(marked_puzzle):
                puzzles.remove(puzzle)
            if not puzzles:
                return draw * sum_only_mark(puzzle)


class UnitTests(unittest.TestCase):
    source = read_data("day-4.txt")

    def test_example_data(self):
        source = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""
        self.assertEqual(4512, part_1(source))
        self.assertEqual(1924, part_2(source))

    def test_part_1(self):
        self.assertEqual(58838, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(6256, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
