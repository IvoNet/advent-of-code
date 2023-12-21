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
import os
import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def parse(source):
    grid = [list(row) for row in source]
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == "S":
                return (r, c), grid
    raise ValueError("No start found")


def bfs(start, grid, max_steps):
    queue = collections.deque([(start, max_steps)])  # Add step count to queue
    visited = {start}
    answer = set()
    while queue:
        (r, c), steps = queue.popleft()

        if steps % 2 == 0:  # even steps are always possible to do in even steps (64)
            answer.add((r, c))
        if steps == 0:
            continue

        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[0]) or grid[nr][nc] == "#" or (nr, nc) in visited:
                continue
            visited.add((nr, nc))
            queue.append(((nr, nc), steps - 1))
    return len(answer)


def part_1(source: str | list[str], steps=64) -> int | None:
    start, grid = parse(source)
    return bfs(start, grid, steps)


def part_2(source: str | list[str]) -> int | None:
    return None


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(16, part_1(self.test_source, 6))

    def test_part_1(self) -> None:
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
