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
from collections import abc, defaultdict
import unittest
from pathlib import Path

import pyperclip
import sys
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def init_grid(source) -> tuple[list[list[str]], int, int, int, int]:
    rows: list[str] = list(source)
    height = len(rows)
    width = len(rows[0])

    # Build grid as list of list for indexing, keep original row lengths
    grid: list[list[str]] = [list(r) for r in rows]

    # Find start position 'S'
    start_col, start_row = find_start(rows)
    return grid, height, start_col, start_row, width


def find_start(rows: list[str]) -> tuple[int, int]:
    start_row = None
    start_col = None
    for ridx, line in enumerate(rows):
        if 'S' in line:
            start_row = ridx
            start_col = line.index('S')
            break
    if start_row is None or start_col is None:
        raise ValueError("Start position 'S' not found in input")
    return start_col, start_row


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
    grid, height, start_col, start_row, width = init_grid(source)

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
    """Part 2: many-worlds quantum splitting.
    Instead of counting split events, a single particle takes both left and right
    paths at every splitter, creating timelines. We need to count the total number
    of timelines after the particle completes all possible journeys.

    Implementation: keep a counter per column for the active timelines at that
    row. When a splitter is encountered at column c with count n, those n timelines
    branch into left and right (if in bounds). Otherwise, timelines at column c
    continue downward.
    """
    grid, height, start_col, start_row, width = init_grid(source)

    # active timelines per column (start one row below S)
    active: dict[int, int] = {start_col: 1}
    # Process each row downward; after the last row the remaining timelines are final
    for r in range(start_row + 1, height):
        next_active: dict[int, int] = defaultdict(int)
        for c, count in active.items():
            if c < 0 or c >= width:
                # out of horizontal bounds -> timelines are lost
                continue
            cell = grid[r][c]
            if cell == '^':
                left = c - 1
                right = c + 1
                if 0 <= left < width:
                    next_active[left] += count
                if 0 <= right < width:
                    next_active[right] += count
            else:
                next_active[c] += count
        active = next_active
        if not active:
            break

    # total timelines is the sum of counts remaining after processing the last row
    answer = sum(active.values())
    # Copy to clipboard for convenience
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
        self.assertEqual(9897897326778, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
