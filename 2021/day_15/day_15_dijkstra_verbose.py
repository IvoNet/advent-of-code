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
from typing import NamedTuple, TypeVar, Callable, Optional

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


class DijkstraNode(NamedTuple):
    cost: int
    x: int
    y: int


def neighbors(boundary: int) -> Callable[[DijkstraNode], list[tuple[int, int]]]:
    """Up, down, left, right
    Does take the boundaries of the grid into account
    """

    def do(dn: DijkstraNode) -> list[tuple[int, int]]:
        potential = [(dn.x - 1, dn.y),  # left
                     (dn.x + 1, dn.y),  # right
                     (dn.x, dn.y - 1),  # down
                     (dn.x, dn.y + 1)]  # up
        # remove the coords outside the boundary
        ret = []
        for x, y in potential:
            if x < 0 or y < 0 or x >= boundary or y >= boundary:
                continue
            ret.append((x, y))
        return ret

    return do


def is_goal(boundary: int) -> Callable[[DijkstraNode], bool]:
    def reached(dn: DijkstraNode) -> bool:
        return dn.x == dn.y == boundary - 1

    return reached


def cost_calculator(grid: list[list[int]]) -> Callable[[int, int], int]:
    def do(x, y) -> int:
        return grid[x][y]

    return do


def dijkstra(initial: T,
             goal: Callable[[T], bool],
             successors: Callable[[T], list[tuple[int, int]]],
             cost: Callable[[int, int], int]) -> Optional[DijkstraNode[T]]:
    priority_queue: list[DijkstraNode] = [initial]
    visited = set()

    while priority_queue:
        current = heapq.heappop(priority_queue)
        if goal(current):
            return current
        if current in visited:
            continue
        visited.add(current)
        for nx, ny in successors(current):
            if (nx, ny) in visited:
                continue
            heapq.heappush(priority_queue, DijkstraNode(current.cost + cost(nx, ny), nx, ny))

    return None


def part_1(source: list[list[int]]):
    grid, boundary = parse(source, times=1)

    start = DijkstraNode(0, 0, 0)
    finished = is_goal(boundary)
    return dijkstra(start, finished, neighbors(boundary), cost_calculator(grid)).cost


def part_2(source):
    grid, boundary = parse(source, times=5)

    start = DijkstraNode(0, 0, 0)
    finished = is_goal(boundary)
    return dijkstra(start, finished, neighbors(boundary), cost_calculator(grid)).cost


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
