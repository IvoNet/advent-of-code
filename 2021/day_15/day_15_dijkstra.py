#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
https://www.youtube.com/watch?v=pJwXTHcfaAs
"""

import heapq
import sys
import unittest
from pathlib import Path

from ivonet.files import read_int_matrix
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source, times=5):
    side = len(source[0])
    grid = [[0] * side * times for _ in range(side * times)]
    for i in range(side * times):
        for j in range(side * times):
            grid[i][j] = (source[i % side][j % side] + (i // side) + (j // side) - 1) % 9 + 1
    return grid, side * times


def dijkstra(source, times=1):
    grid, boundary = parse(source, times=times)
    priority_queue = [(0, 0, 0)]
    visited = set()

    while priority_queue:
        cost, x, y = heapq.heappop(priority_queue)
        if x == y == boundary - 1:
            # done
            return cost
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if nx < 0 or ny < 0 or nx >= boundary or ny >= boundary:
                continue  # outside scope
            if (nx, ny) in visited:
                continue
            heapq.heappush(priority_queue, (cost + grid[nx][ny], nx, ny))

    return -1  # not found


def part_1(source):
    return dijkstra(source, 1)


def part_2(source):
    return dijkstra(source, 5)


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
