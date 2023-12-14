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

Notes:
    This is NOT an example of the best code out there. It is just a solution to the problem.
    It took me more time to parse the "game board" than to solve the puzzle :-)
"""

import os
import sys
import unittest
from collections import defaultdict
from pathlib import Path

from ivonet.collection import Stack
from ivonet.files import read_data, read_rows
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse_stacks(source):
    """parse the gameboard
    - decide how many stacks there are (last row on the game board)
    - from the first index every 4th index is a stack entry and if not there are no more stacks in that row
    - parse every row backwards to get the stacks in the right order
    """
    rows = source.split("\n")
    no_of_stacks = max(ints(rows[-1])) * 4
    stacks = defaultdict(Stack)
    rows = rows[:-1][::-1]  # reverse without the last numbered row
    for row in rows:
        for stack, i in enumerate(rangei(1, no_of_stacks, 4), 1):
            try:
                if row[i] != " ":
                    stacks[stack].push(row[i])
            except IndexError:
                # no more stacks in this row
                break
    return stacks


def parse_moves(source):
    """As the ints are all in the same order of times, from and to we can just filter out
    all the ints and ignore the rest"""
    return [ints(x) for x in read_rows(source)]


def parse_input(source):
    """stacks and instructions are separated by a double blank line"""
    stacks, instructions = source.split("\n\n")
    return parse_stacks(stacks), parse_moves(instructions)


def part_1(source):
    stacks, moves = parse_input(source)

    for times, from_, to_ in moves:
        for _ in range(times):
            stacks[to_].push(stacks[from_].pop())

    return "".join(stacks[i].pop() for i in sorted(stacks.keys()))


def part_2(source):
    """I could have used slicing but as I already had the Stack class I used that
    and an in between stack will make it in the right order again :-)

    """
    stacks, moves = parse_input(source)

    for times, from_, to_ in moves:
        temp = Stack()
        for _ in range(times):
            temp.push(stacks[from_].pop())
        for _ in range(times):
            stacks[to_].push(temp.pop())

    return "".join(stacks[i].pop() for i in sorted(stacks.keys()))


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input", raw=True)
        self.test_source = read_data("""    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""", raw=True)

    def test_example_data_part_1(self):
        self.assertEqual("CMZ", part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual("LJSVLTWQM", part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual("MCD", part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual("BRQWDBBJM", part_2(self.source))


if __name__ == '__main__':
    unittest.main()
