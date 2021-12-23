#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import heapq
import sys
import unittest
from pathlib import Path
from typing import TypeVar, Callable

from ivonet.files import read_int_matrix
from ivonet.iter import ints

sys.dont_write_bytecode = True

T = TypeVar('T')

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source: list[list[int]], times: int = 5) -> (list[list[int]], int):
    """Parse the input to a grid of the needed size.
    The times multiplies the original grid according the rules
    of day 15 exercise
    :param source: a list of list of ints
    :param times: nr of times the grid has to be expanded
    :return: grid and boundary
    """
    side = len(source[0])
    grid = [[0] * side * times for _ in range(side * times)]
    for i in range(side * times):
        for j in range(side * times):
            grid[i][j] = (source[i % side][j % side] + (i // side) + (j // side) - 1) % 9 + 1
    return grid, side * times


def neighbors(boundary: int) -> Callable[[T], list[tuple[int, int]]]:
    """Up, down, left, right
    Does take the boundaries of the grid into account
    """

    def do(x, y) -> list[tuple[int, int]]:
        potential = [(x - 1, y),  # left
                     (x + 1, y),  # right
                     (x, y - 1),  # down
                     (x, y + 1)]  # up
        # remove the coords outside the boundary
        return [(x, y) for x, y in potential if 0 <= x < boundary and 0 <= y < boundary]

    return do


def is_goal(boundary: int) -> Callable[[T], bool]:
    def reached(x, y) -> bool:
        return x == y == boundary - 1

    return reached


def cost_calculator(grid: list[list[int]]) -> Callable[[T], int]:
    def do(x, y) -> int:
        return grid[x][y]

    return do


def dijkstra(initial: [int, int],
             goal: Callable[[int, int], bool],
             successors: Callable[[int, int], list[tuple[int, int]]],
             cost: Callable[[int, int], int],
             initial_cost: int = 0) -> int:
    priority_queue = [(initial_cost, initial[0], initial[1])]
    visited = set()

    while priority_queue:
        current_cost, x, y = heapq.heappop(priority_queue)
        if goal(x, y):
            return current_cost
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for nx, ny in successors(x, y):
            if (nx, ny) in visited:
                continue
            heapq.heappush(priority_queue, (current_cost + cost(nx, ny), nx, ny))

    return -1


def part_1(source: list[list[int]]):
    grid, boundary = parse(source, times=1)
    return dijkstra((0, 0), is_goal(boundary), neighbors(boundary), cost_calculator(grid))


def part_2(source):
    grid, boundary = parse(source, times=5)
    return dijkstra((0, 0), is_goal(boundary), neighbors(boundary), cost_calculator(grid))


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_int_matrix(f"day_{day.zfill(2)}.input")
        self.test_source = read_int_matrix("""1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""")

    def test_example_data_part_1(self):
        self.assertEqual(40, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(458, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(315, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2800, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
