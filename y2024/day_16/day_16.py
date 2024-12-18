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
import heapq
import os
import sys
import unittest
from collections import abc, namedtuple
from pathlib import Path

import pyperclip
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.grid import Location
from ivonet.iter import ints

collections.Callable = abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


DIRECTIONS = [
    Location(-1, 0),  # north
    Location(0, 1),  # east
    Location(1, 0),  # south
    Location(0, -1)  # west
]  # north (0), east (1), south (2), west (3)

Node = namedtuple('Node', ['cost', 'location', 'direction'])


def dijkstra(grid, start, goal):
    queue = []
    seen = set()
    distances = {}
    heapq.heappush(queue, (0, start, 1))
    while queue:
        cost, loc, direction = heapq.heappop(queue)
        if (loc, direction) not in distances:
            distances[(loc, direction)] = cost
        if loc.row == goal.row and loc.col == goal.col:
            return cost
        if (loc, direction) in seen:
            continue
        seen.add((loc, direction))
        current_direction = DIRECTIONS[direction]
        new_loc = loc + current_direction
        if 0 <= new_loc.row < len(grid) and 0 <= new_loc.col < len(grid[0]) and grid[new_loc.row][new_loc.col] != '#':
            heapq.heappush(queue, (cost + 1, new_loc, direction))
        heapq.heappush(queue, (cost + 1000, loc, (direction + 1) % 4))
        heapq.heappush(queue, (cost + 1000, loc, (direction + 3) % 4))


def parse(source):
    grid = []
    start = None
    end = None
    for r, row in enumerate(source):
        grid.append(list(row))
        if "S" in row:
            start = Location(r, row.index("S"))
        if "E" in row:
            end = Location(r, row.index("E"))
    return grid, start, end


@debug
@timer
def part_1(source) -> int | None:
    grid, start, end = parse(source)
    p(grid, start, end)
    answer = dijkstra(grid, start, end)
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0

    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(7036, part_1(self.test_source))

    def test_example_data_part_1a(self) -> None:
        self.assertEqual(11048, part_1(self.test_source_1))

    def test_part_1(self) -> None:
        self.assertEqual(92432, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(45, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")
        self.test_source_1 = read_rows(f"{folder}/test_{day}_1.input")


if __name__ == '__main__':
    unittest.main()
