#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import sys
import unittest
from heapq import heappush, heappop
from pathlib import Path
from pprint import pprint
from typing import Generic, TypeVar, List, NamedTuple

from ivonet.files import read_int_matrix
from ivonet.iter import ints

sys.dont_write_bytecode = True

T = TypeVar('T')
DX = [-1, 0, 1, 0]
DY = [0, 1, 0, -1]


class Cell(NamedTuple):
    row: int
    column: int
    distance: int

    def __lt__(self, right: Cell) -> bool:
        return self.distance < right.distance

    def __gt__(self, right: Cell) -> bool:
        return self.distance > right.distance

    def __eq__(self, right: Cell) -> bool:
        return self.distance == right.distance

    def __repr__(self) -> str:
        return f""


# def distance_comparator(left: Cell, right: Cell):
#     if left.distance < right.distance:
#         return -1
#     elif left.distance > right.distance:
#         return 1
#     return 0


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def push(self, item: T) -> None:
        heappush(self._container, item)  # in by priority

    def pop(self) -> T:
        return heappop(self._container)  # out by priority

    def remove(self, item: T):
        self._container.remove(item)

    def __repr__(self) -> str:
        return repr(self._container)


class Cavern:

    def __init__(self, grid) -> None:
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def in_grid(self, row, col) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def shortest_path(self):
        dist = []
        for _ in range(self.rows):
            dist.append([sys.maxsize for _ in range(self.cols)])

        pq = PriorityQueue()
        pq.push(Cell(0, 0, dist[0][0]))
        while not pq.empty:
            current: Cell = pq.pop()
            for i in range(3):
                rows = current.row + DX[i]
                cols = current.column + DY[i]
                if self.in_grid(rows, cols):
                    if dist[rows][cols] > dist[current.row][current.column] + self.grid[rows][cols]:
                        if dist[rows][cols] != sys.maxsize:
                            adj = Cell(rows, cols, dist[rows][cols])
                            pq.remove(adj)
                        dist[rows][cols] = dist[current.row][current.column] + self.grid[rows][cols]
                        pq.push(Cell(rows, cols, dist[rows][cols]))
        pprint(dist)
        return dist[self.rows - 1][self.cols - 1]

    def __repr__(self) -> str:
        return repr(self.grid)


def part_1(grid):
    cavern = Cavern(grid)
    total = cavern.shortest_path()
    print(cavern)
    return total


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_int_matrix(f"day_{day}.txt")
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
        self.assertEqual(None, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
