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
from collections import defaultdict
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

Node = namedtuple('Node', ['cost', 'location', 'direction', 'path'])


def visualize(grid, path):
    if DEBUG:
        for r, c in path:
            grid[r][c] = "O"
        for row in grid:
            print("".join(row))


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


def dijkstra_with_bfs(grid, start, goal):
    """
    Modified Dijkstra to find all the paths with the lowest cost and not just the first one.

    """
    queue = []
    lowest_cost = defaultdict(lambda: float("inf"))
    best_cost = float("inf")
    best_paths = []
    heapq.heappush(queue, Node(0, start, 1, [start]))
    while queue:
        cost, loc, direction, path = heapq.heappop(queue)
        if cost > lowest_cost[(loc, direction)]:  # if we have a better path to this location
            continue
        if loc == goal:
            if cost > best_cost:
                break
            best_cost = cost
            best_paths.append(path)
        for new_cost, new_loc, new_direction in [(cost + 1, loc + DIRECTIONS[direction], direction),  # forward
                                                 (cost + 1000, loc, (direction + 1) % 4),  # right
                                                 (cost + 1000, loc, (direction + 3) % 4)  # left
                                                 ]:
            if (0 <= new_loc.row < len(grid)
                    and 0 <= new_loc.col < len(grid[0])
                    and grid[new_loc.row][new_loc.col] != '#'):
                lowest = lowest_cost[(new_loc, new_direction)]
                if new_cost > lowest:
                    continue
                if new_cost < lowest:
                    lowest_cost[(new_loc, new_direction)] = new_cost
                heapq.heappush(queue, Node(new_cost, new_loc, new_direction, path + [new_loc]))

    # at this point we should have found all the paths with the lowest cost
    # now we just have to make all the locations in these paths unique
    # we could also iterate over all the paths and set an "O" in the grid and then count the "O"s in the grid
    # Which is what i did at first but that is not necessary
    all_coords = {loc for path in best_paths for loc in path}
    visualize(grid, all_coords)
    return best_cost, len(all_coords)


@debug
@timer
def part_1(source) -> int | None:
    grid, start, end = parse(source)
    answer, _ = dijkstra_with_bfs(grid, start, end)
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    grid, start, end = parse(source)
    _, answer = dijkstra_with_bfs(grid, start, end)
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

    def test_example_data_part_2a(self) -> None:
        self.assertEqual(64, part_2(self.test_source_1))

    def test_part_2(self) -> None:
        self.assertEqual(458, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")
        self.test_source_1 = read_rows(f"{folder}/test_{day}_1.input")


if __name__ == '__main__':
    unittest.main()
