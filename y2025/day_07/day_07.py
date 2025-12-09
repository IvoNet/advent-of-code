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
import unittest
from pathlib import Path

import pyperclip
import sys
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


@debug
@timer
def part_1(source) -> int | None:
    """Part 1:
    S = start of beam
    Beams always move down one row at a time in free space (.)
    ^ is a beam splitter that stops the current beam and splits them to beams starting on the left and right of the split (^).
    Find the number of times a split occurs until the beam reaches the bottom of the grid.
    Do not count beams that are started by other splits.
    """
    # Normalize source to a list of strings and determine dimensions
    rows: list[str] = list(source)
    height = len(rows)
    width = len(rows[0])

    # Build grid as list of list for indexing, keep original row lengths
    grid: list[list[str]] = [list(r) for r in rows]

    # Find start position 'S'
    start_row = None
    start_col = None
    for ridx, line in enumerate(rows):
        if 'S' in line:
            start_row = ridx
            start_col = line.index('S')
            break
    if start_row is None or start_col is None:
        raise ValueError("Start position 'S' not found in input")

    # Set of active beam columns at the current row (start one row below S)
    active_cols: set[int] = {start_col}
    split_count = 0

    # Process rows from the row below S to the bottom
    for r in range(start_row + 1, height):
        next_cols: set[int] = set()
        for c in active_cols:
            # out of horizontal bounds -> beam is gone
            if c < 0 or c >= width:
                continue
            cell = grid[r][c]
            if cell == '^':
                split_count += 1
                left = c - 1
                right = c + 1
                if 0 <= left < width:
                    next_cols.add(left)
                if 0 <= right < width:
                    next_cols.add(right)
            else:
                # any other char -> beam continues downwards
                next_cols.add(c)
        active_cols = next_cols
        if not active_cols:
            break

    pyperclip.copy(str(split_count))
    return split_count


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(21, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(1550, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(40, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
