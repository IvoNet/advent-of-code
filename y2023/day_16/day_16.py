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


DIRECTIONS: dict[str, tuple[int, int]] = {
    "right": (0, 1),  # right
    "up": (-1, 0),  # up
    "left": (0, -1),  # left
    "down": (1, 0),  # down
}


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class FloorWillBeLava(object):
    EMPTY = "."
    FORE_MIRROR = "/"
    BACK_MIRROR = "\\"
    V_SPLITTER = "|"
    H_SPLITTER = "-"
    RIGHT = "right"
    UP = "up"
    LEFT = "left"
    DOWN = "down"

    def __init__(self, source: list[str]) -> None:
        self.source: list[str] = source
        self.grid: list[str] = source
        self.height: int = len(self.grid)
        self.width: int = len(self.grid[0])

    def __is_valid(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width

    def _is_out_of_bounds(self, row: int, col: int) -> bool:
        return not self.__is_valid(row, col)

    def bfs(self, start: tuple[int, int] = (0, -1), start_direction: str = "right") -> int:
        queue: deque = deque()
        explored: set[tuple[int, int, str]] = set()
        row, col = start
        direction = start_direction

        queue.append((row, col, direction))

        while queue:
            row, col, direction = queue.popleft()
            row += DIRECTIONS[direction][0]
            col += DIRECTIONS[direction][1]

            if self._is_out_of_bounds(row, col):
                continue

            current_tile = self.grid[row][col]



            if current_tile == self.V_SPLITTER and direction in [self.LEFT, self.RIGHT]:
                for nd in [self.UP, self.DOWN]:
                    if (row, col, nd) not in explored:
                        explored.add((row, col, nd))
                        queue.append((row, col, nd))
                continue

            if current_tile == self.H_SPLITTER and direction in [self.UP, self.DOWN]:
                for nd in [self.LEFT, self.RIGHT]:
                    if (row, col, nd) not in explored:
                        explored.add((row, col, nd))
                        queue.append((row, col, nd))
                continue

            if current_tile == self.FORE_MIRROR:
                if direction == self.RIGHT:
                    direction = self.UP
                elif direction == self.UP:
                    direction = self.RIGHT
                elif direction == self.LEFT:
                    direction = self.DOWN
                else:
                    direction = self.LEFT

            if current_tile == self.BACK_MIRROR:
                if direction == self.RIGHT:
                    direction = self.DOWN
                elif direction == self.UP:
                    direction = self.LEFT
                elif direction == self.LEFT:
                    direction = self.UP
                else:
                    direction = self.RIGHT

            if (row, col, direction) not in explored:
                explored.add((row, col, direction))
                queue.append((row, col, direction))

        return len({(row, col) for row, col, _ in explored})

    def energize(self) -> int:
        return self.bfs(start=(0, -1), start_direction=self.RIGHT)

    def best_config(self):
        max_val = 0

        for r in range(self.height):
            max_val = max(max_val, self.bfs((r, -1), self.RIGHT))
            max_val = max(max_val, self.bfs((r, self.width), self.LEFT))

        for c in range(self.width):
            max_val = max(max_val, self.bfs((-1, c), self.DOWN))
            max_val = max(max_val, self.bfs((self.height, c), self.UP))

        return max_val

    def __str__(self) -> str:
        return "\n".join(self.grid)


def part_1(grid: list[str]) -> int:
    return FloorWillBeLava(grid).energize()


def part_2(grid: list[str]) -> int:
    return FloorWillBeLava(grid).best_config()


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
        _()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
