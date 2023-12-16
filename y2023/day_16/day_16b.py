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
from collections import deque
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True

# Define movements using imaginary numbers
move_right = 1j  # Move one unit to the right
move_up = -1  # Move one unit up
move_left = -1j  # Move one unit to the left
move_down = 1  # Move one unit down


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def bfs(source: list[str], start: complex, direction: complex) -> int:
    grid = [list(row) for row in source]
    start: complex = 0 - 1j
    explored: set[tuple[complex, complex]] = set()
    queue: deque[tuple[complex, complex]] = deque()
    queue.append((start, direction))

    while queue:
        pos, direction = queue.popleft()
        pos += direction

        row, col = int(pos.real), int(pos.imag)

        if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]):
            _(f"Out of bounds: {row}, {col}")
            continue

        tile = grid[row][col]
        _(f"Tile: {tile} - ({row}, {col}) - {direction}")
        if tile == "|" and direction in [move_left, move_right]:
            d: complex
            for d in [move_up, move_down]:
                p: tuple[complex, complex] = (pos, d)
                if p not in explored:
                    explored.add(p)
                    queue.append(p)
            continue
        if tile == "-" and direction in [move_up, move_down]:
            for d in [move_left, move_right]:
                p = (pos, d)
                if p not in explored:
                    explored.add(p)
                    queue.append(p)
            continue

        if tile == "/" and direction in [move_up, move_down] or tile == "\\" and direction in [move_left, move_right]:
            direction *= -1j
        elif tile == "/" and direction in [move_left, move_right] or tile == "\\" and direction in [move_up, move_down]:
            direction *= 1j

        if (pos, direction) not in explored:
            explored.add((pos, direction))
            queue.append((pos, direction))

    return len({p for p, _ in explored})


def part_1(source: list[str]) -> int:
    return bfs(source, 0 - 1j, move_right)


def part_2(grid: list[str]) -> int:
    max_energized = 0
    width = len(grid[0])
    height = len(grid)
    for row in range(width):
        max_energized = max(max_energized, bfs(grid, row + 0j, move_right))
        max_energized = max(max_energized, bfs(grid, row + width * 1j, move_left))
    for col in range(height):
        max_energized = max(max_energized, bfs(grid, col * 1j, move_down))
        max_energized = max(max_energized, bfs(grid, col + height * 1j, move_up))
    return move_right


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(46, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(6795, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(51, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(7154, part_2(self.source))

    def setUp(self) -> None:
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
