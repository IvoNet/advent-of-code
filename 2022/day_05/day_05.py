#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2023 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the gist it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
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

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse_stacks(source):
    rows = source.split("\n")
    no_stacks = max(ints(rows[-1]))
    stacks = defaultdict(Stack)
    rows = rows[:-1][::-1]
    for row in rows:
        for s, i in enumerate(rangei(1, no_stacks * 4, 4)):
            try:
                if row[i] != " ":
                    stacks[s + 1].push(row[i])
            except IndexError:
                _(i, "no more stacks")
                break
    return stacks


def parse_moves(source):
    return [ints(x) for x in read_rows(source)]


def parse_input(source):
    stacks, instructions = source.split("\n\n")
    return parse_stacks(stacks), parse_moves(instructions)


def part_1(source):
    stacks, moves = parse_input(source)

    for times, from_, to_ in moves:
        for _ in range(times):
            stacks[to_].push(stacks[from_].pop())

    ret = ""
    for i in sorted(stacks.keys()):
        ret += stacks[i].pop()

    return ret


def part_2(source):
    stacks, moves = parse_input(source)

    for times, from_, to_ in moves:
        temp = Stack()
        for _ in range(times):
            temp.push(stacks[from_].pop())
        for _ in range(times):
            stacks[to_].push(temp.pop())

    ret = ""
    for i in sorted(stacks.keys()):
        ret += stacks[i].pop()

    return ret


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
