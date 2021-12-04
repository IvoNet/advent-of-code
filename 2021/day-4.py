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


def parse_puzzles(data):
    puzzles = []
    for record in data:
        puzzle = []
        for row in record.split("\n"):
            puzzle.append([[int(x), 0] for x in row.strip().replace("  ", " ").replace(" ", ",").split(",")])
        puzzles.append(puzzle)
    return puzzles


def mark(puzzle, draw):
    for row in puzzle:
        for col in row:
            if col[0] == draw:
                col[1] = 1
    return puzzle


def check_horizontal(marked_puzzle):
    for row in marked_puzzle:
        if sum(x[1] for x in row) == 5:
            return True
    return False


def check_vertical(marked_puzzle):
    for i in range(len(marked_puzzle[0])):
        count = 0
        for row in marked_puzzle:
            count += row[i][1]
        if count == 5:
            return True
    return False


def sum_unmarked(puzzle):
    total = 0
    for row in puzzle:
        for col in row:
            if col[1] == 0:
                total += col[0]
    return total


def parse(data):
    source = data.split("\n\n")
    draws = [int(x) for x in source[0].strip().split(",")]
    puzzles = parse_puzzles(source[1:])
    return draws, puzzles


def part_1(data):
    draws, puzzles = parse(data)
    for draw in draws:
        for puzzle in puzzles:
            marked_puzzle = mark(puzzle, draw)
            win = check_horizontal(marked_puzzle) or check_vertical(marked_puzzle)
            if win:
                return draw * sum_unmarked(puzzle)


def part_2(data):
    draws, puzzles = parse(data)
    for draw in draws:
        for puzzle in puzzles[::]:
            marked_puzzle = mark(puzzle, draw)
            win = check_horizontal(marked_puzzle) or check_vertical(marked_puzzle)
            if win:
                puzzles.remove(puzzle)
            if not puzzles:
                return draw * sum_unmarked(puzzle)


class UnitTests(unittest.TestCase):
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
        self.assertEqual(part_1(source), 4512)
        self.assertEqual(part_2(source), 1924)


if __name__ == '__main__':
    unittest.main()
    source = read_data("day-4.txt")
    print("Part 1:", part_1(source))  #
    print("part 2:", part_2(source))  #
