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
from pathlib import Path
from typing import NamedTuple

import pyperclip

from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.grid import Location
from ivonet.iter import ints
from ivonet.search import astar

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


DIRECTIONS = [Location(-1, 0), Location(0, 1), Location(1, 0),
              Location(0, -1)]  # north (0), east (1), south (2), west (3)


class Node(NamedTuple):
    cost: int
    location: Location
    direction: int


class Maze:

    def __init__(self, source):
        self.source = source
        self.grid = []
        self.start: Location
        self.end: Location
        self.direction = 1
        self.cost = 0
        self.parse_grid()

    def parse_grid(self):
        for r, line in enumerate(self.source):
            for c, ch in enumerate(line):
                if ch == 'S':
                    self.start = Location(r, c)
                if ch == 'E':
                    self.end = Location(r, c)
            self.grid.append(list(line))

    def is_goal(self, given: Location):
        return given == self.end

    def successors(self, given: Node) -> list[Node]:
        result = []
        for nd in DIRECTIONS:
            nloc = given + nd
            if 0 <= nloc.row < len(self.grid) and 0 <= nloc.col < len(self.grid[0]) and self.grid[nloc.row][
                nloc.col] != '#':
                result.append(Node(nloc, given, ))
        return

    def dijkstra(self):
        # initial: [int, int],
        #          goal: Callable[[int, int], bool],
        #          successors: Callable[[int, int], list[tuple[int, int]]],
        #          cost: Callable[[int, int], int],
        #          initial_cost: int = 0) -> int:
        distance = {}
        priority_queue = [Node(0, self.start, self.direction)]
        visited = set()
        best = None

        while priority_queue:
            node: Node = heapq.heappop(priority_queue)
            if self.is_goal(node.location):
                return node.cost
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for nx, ny in successors(x, y):
                if (nx, ny) in visited:
                    continue
                heapq.heappush(priority_queue, (current_cost + cost(nx, ny), nx, ny))

        return -1





@debug
@timer
def part_1(source) -> int | None:
    maze = Maze(source)
    answer = 0
    solution = astar(maze.start,
                     maze.goal_test,
                     maze.successors,
                     maze.manhatten_distance,
                     maze.cost)
    pyperclip.copy(str(answer))


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
