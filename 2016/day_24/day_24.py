#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import sys
import unittest
from enum import Enum
from pathlib import Path
from typing import NamedTuple, TypeVar, Callable, Optional

from ivonet.files import read_rows
from ivonet.iter import ints
from ivonet.search import bfs, node_to_path, Node

sys.dont_write_bytecode = True
T = TypeVar('T')

DEBUG = True


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
        self._grid[self.start.row][self.start.col] = Cell.START
        self._grid[self.goal.row][self.goal.col] = Cell.GOAL


def parse(source):
    maze = []
    locations = {}
    for r, line in enumerate(source):
        row = []
        for c, col in enumerate(line):
            if col in "01234567":
                locations[col] = Location(r, c)
            row.append(Cell.BLOCKED if col == "#" else Cell.EMPTY)
        maze.append(row)
    return maze, locations


def manhattan_distance(goal: Location) -> Callable[[Location], float]:
    def distance(ml: Location) -> float:
        xdist: int = abs(ml.col - goal.col)
        ydist: int = abs(ml.row - goal.row)
        return (xdist + ydist)

    return distance


def max_steps(option: Optional[Node[Location]], max=50) -> bool:
    if option is None:
        return False
    return len(node_to_path(option)) - 1 <= max


def part_1(source):
    grid, locations = parse(source)
    maze = Maze(grid, locations["0"], locations["1"])
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


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
