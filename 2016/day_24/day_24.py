#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Used the same code as for day 13 of 2016. Very handy
"""

import os
import sys
import unittest
from enum import Enum
from itertools import combinations
from pathlib import Path
from typing import NamedTuple, TypeVar, Optional

from ivonet.files import read_rows
from ivonet.iter import ints, consecutive_element_pairing, combinations
from ivonet.search import bfs, node_to_path, Node

sys.dont_write_bytecode = True
T = TypeVar('T')

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "#"
    START = "S"
    GOAL = "G"
    PATH = "*"


def repr_maze(maze):
    return "\n".join("".join(row) for row in maze)


class Location(NamedTuple):
    row: int
    col: int


def parse(source: str) -> [list[list[Cell], dict[[str], Location]]]:
    maze: list[list[Cell]] = []
    locations: dict[[str], Location] = {}
    for r, line in enumerate(source):
        row = []
        for c, col in enumerate(line):
            if col in "01234567":
                locations[col] = Location(r, c)
            row.append(Cell.BLOCKED if col == "#" else Cell.EMPTY)
        maze.append(row)
    return maze, locations


class Maze:

    def __init__(self, maze: list[list[Cell]], start: Location, goal: Location) -> None:
        self._rows: int = len(maze)
        self._columns: int = len(maze[0])
        self.start: Location = start
        self.goal: Location = goal
        self._grid: list[list[Cell]] = maze
        self._grid[start.row][start.col] = Cell.START
        if isinstance(goal, Location):
            self._grid[goal.row][goal.col] = Cell.GOAL

    def __str__(self) -> str:
        return repr_maze(self._grid)

    def is_goal(self, loc: Location) -> bool:
        return self.goal == loc

    def successors(self, ml: Location) -> list[Location]:
        locations: list[Location] = []
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.col] != Cell.BLOCKED:
            locations.append(Location(ml.row + 1, ml.col))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.col] != Cell.BLOCKED:
            locations.append(Location(ml.row - 1, ml.col))
        if ml.col + 1 < self._columns and self._grid[ml.row][ml.col + 1] != Cell.BLOCKED:
            locations.append(Location(ml.row, ml.col + 1))
        if ml.col - 1 >= 0 and self._grid[ml.row][ml.col - 1] != Cell.BLOCKED:
            locations.append(Location(ml.row, ml.col - 1))
        return locations

    def mark(self, path: list[Location]):
        for loc in path:
            self._grid[loc.row][loc.col] = Cell.PATH
        self._grid[self.start.row][self.start.col] = Cell.START
        self._grid[self.goal.row][self.goal.col] = Cell.GOAL

    def clear(self, path: list[Location]):
        for loc in path:
            self._grid[loc.row][loc.col] = Cell.EMPTY
        self._grid[self.start.row][self.start.col] = Cell.EMPTY
        self._grid[self.goal.row][self.goal.col] = Cell.EMPTY


def breath_first_search(grid: list[list[Cell]], start: Location, goal: Location) -> int:
    """Do the search and then give back the shortest found."""
    maze = Maze(grid, start, goal)
    solution_dfs: Optional[Node[Location]] = bfs(maze.start, maze.is_goal, maze.successors)
    if solution_dfs is None:
        raise ValueError("No solution found using depth-first search!")
    else:
        path: list[Location] = node_to_path(solution_dfs)
    if DEBUG:
        maze.mark(path)
        print(maze)
        maze.clear(path)
    return len(path) - 1


def find_shortest(source: str, return_to_start=False):
    """Shortest path finder.
    - Because there are more than 1 start and end points we need to find the
      best combination of in order to get the shortest path.
    - there are 7 exposed wire locations to visit
    - startpoint is always "0", so in order to find the shortest path we need to try all combinations
      starting with 0 and then every combination of 1..7 in steps of start,goal combinations
      goal of first path will become start for next with new goal, etc. these are represented in the 'combi' variable
    - in order to speed things up significantly it is useful to remember combinations already processed
      just return the distance in that case.
    - return the min(paths) voila
    - if we need to return to our original starting point we just add "0" to the last step too.
    - visualize by setting DEBUG to True :-)
    """
    grid, locations = parse(source)
    paths = {}
    visited = {}
    if return_to_start:
        combi = [("0", *x, "0") for x in combinations(list("1234567"), 7)]
    else:
        combi = [("0", *x) for x in combinations(list("1234567"), 7)]
    for pad in combi:
        pad_tot = 0
        for start, goal in consecutive_element_pairing(pad, 2):
            if distance := visited.get((start, goal), None):
                pad_tot += distance
            else:
                try:
                    distance = breath_first_search(grid, locations[start], locations[goal])
                    pad_tot += distance
                    visited[(start, goal)] = distance
                except ValueError:
                    visited[(start, goal)] = float("inf")
        _(" -> ".join(pad), "distance:", pad_tot)
        paths[pad] = pad_tot
    shortest_pad, shortest = min(paths.items(), key=lambda x: x[1])[:2]
    print("Shortest path:", " -> ".join(shortest_pad), "distance:", shortest)
    return shortest


def part_1(source):
    return find_shortest(source, return_to_start=False)


def part_2(source):
    return find_shortest(source, return_to_start=True)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(464, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(652, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
