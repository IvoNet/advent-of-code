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
You're already almost 1.5km (almost a mile) below the surface of the ocean, 
already so deep that you can't see any sunlight. What you can see, however, 
is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. 
Numbers are chosen at random, and the chosen number is marked on all boards on 
which it appears. (Numbers may not appear on all boards.) If all numbers in 
any row or any column of a board are marked, that board wins. 
(Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and 
the giant squid) pass the time. It automatically generates a random order 
in which to draw numbers and a random set of boards (your puzzle input). 
For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

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
 2  0 12  3  7
 
After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no 
winners, but the boards are marked as follows 
(shown here adjacent to each other to save space):
(Note == IvoNet == lost in copying...)

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), 
there are still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

At this point, the third board wins because it has at least one complete 
row or column of marked numbers (in this case, the entire top row is
marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding 
the sum of all unmarked numbers on that board; in this case, the sum is 188. 
Then, multiply that sum by the number that was just called when the 
board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board 
will win first. What will your final score be if you choose that board?

##############################################################################
# Part 2
##############################################################################

--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the 
giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so 
rather than waste time counting its arms, the safe thing to do is to figure 
out which board will win last and choose that one. That way, no matter which 
boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens 
after 13 is eventually called and its middle column is completely marked. 
If you were to keep playing until this point, the second board would have 
a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?

"""

import unittest

from ivonet import read_data

VALUE_IDX = 0
MARK_IDX = 1


def parse(data: str) -> tuple[list[int], list[list[list[list[int]]]]]:
    """Make the data usable by parsing it into the needed components"""
    source = data.split("\n\n")
    draws = [int(x) for x in source[0].strip().split(",")]
    puzzles = []
    for record in source[1:]:
        puzzle = []
        for row in record.split("\n"):
            puzzle.append([[int(x), 0] for x in row.strip().split()])
        puzzles.append(puzzle)
    return draws, puzzles


def mark(puzzle: list[list[list[int]]], draw: int) -> list[list[list[int]]]:
    """Mark your bingo chart on the draw if it is in the puzzle"""
    for row in puzzle:
        for col in row:
            if col[VALUE_IDX] == draw:
                col[MARK_IDX] = 1
    return puzzle


def sum_only_mark(puzzle: list[list[list[int]]], mark: int = 0) -> int:
    """Sum of al unmarked numbers in the puzzle."""
    return sum(col for row in puzzle for col, marked in row if marked == mark)


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


def part_1(data: str) -> int:
    """Find the first puzzle to win"""
    draws, puzzles = parse(data)
    for draw in draws:
        for puzzle in puzzles[::]:
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
    source = read_data("day_4.txt")

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
