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

    MIRROR_REFLECTIONS = {
        (RIGHT, FORE_MIRROR): UP,
        (UP, FORE_MIRROR): RIGHT,
        (LEFT, FORE_MIRROR): DOWN,
        (DOWN, FORE_MIRROR): LEFT,
        (RIGHT, BACK_MIRROR): DOWN,
        (UP, BACK_MIRROR): LEFT,
        (LEFT, BACK_MIRROR): UP,
        (DOWN, BACK_MIRROR): RIGHT,
    }

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
        """
        Performs a breadth-first search (bfs) from a given starting position and direction on the grid.

        The bfs takes into account the different types of tiles (empty, fore mirror, back mirror, vertical splitter,
        horizontal splitter) and their effects on the direction of the bfs. The bfs continues until all reachable tiles
        from the starting position have been explored.

        Args:
           start (tuple[int, int], optional): The starting position for the bfs. Defaults to (0, -1)
              Note that the starting point is just outside the grid as we first do a step and then continue..
           start_direction (str, optional): The initial direction of the bfs. Defaults to "right".

        Returns:
           int: The number of tiles that can be energized from the starting position.
       """
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

            if current_tile in [self.FORE_MIRROR, self.BACK_MIRROR]:
                direction = self.MIRROR_REFLECTIONS[(direction, current_tile)]

            if (row, col, direction) not in explored:
                explored.add((row, col, direction))
                queue.append((row, col, direction))

        return len({(row, col) for row, col, _ in explored})

    def energize(self) -> int:
        """
        Initiates the process of energizing the tiles on the grid.

        The method starts a breadth-first search (bfs) from the top-left corner of the grid (position (0, -1))
        with the initial direction being towards the right. The bfs takes into account the different types of
        tiles (empty, fore mirror, back mirror, vertical splitter, horizontal splitter) and their effects on
        the direction of the bfs.

        Returns:
            int: The number of tiles that can be energized from the starting position.
        """
        return self.bfs(start=(0, -1), start_direction=self.RIGHT)

    def best_config(self):
        """
        Calculates the maximum number of tiles that can be energized from any starting position on the grid's perimeter.

        The method iterates over all possible starting positions on the perimeter of the grid (top, bottom, left, right)
        and performs a breadth-first search (bfs) from each position. The direction of the bfs is always towards the center
        of the grid. The bfs takes into account the different types of tiles (empty, fore mirror, back mirror, vertical splitter,
        horizontal splitter) and their effects on the direction of the bfs.

        Returns:
            int: The maximum number of tiles that can be energized from any starting position on the grid's perimeter.
        """
        max_val = 0

        for c in range(self.width):
            max_val = max(max_val, self.bfs((-1, c), self.DOWN))
            max_val = max(max_val, self.bfs((self.height, c), self.UP))

        for r in range(self.height):
            max_val = max(max_val, self.bfs((r, -1), self.RIGHT))
            max_val = max(max_val, self.bfs((r, self.width), self.LEFT))
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
