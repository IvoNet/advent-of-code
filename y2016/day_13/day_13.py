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
from queue import Queue
from typing import NamedTuple, TypeVar, Callable, Optional, Set

from ivonet.collection import Queue
from ivonet.files import read_data
from ivonet.iter import ints
from ivonet.search import bfs, node_to_path, Node

sys.dont_write_bytecode = True

DEBUG = False

T = TypeVar('T')


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


def create_maze(height, width, nr=10) -> list[list[Cell]]:
    maze = []
    for h in range(height):
        row = []
        for w in range(width):
            if bin(w * w + 3 * w + 2 * w * h + h + h * h + nr)[2:].count("1") % 2 == 0:
                row.append(Cell.EMPTY)
            else:
                row.append(Cell.BLOCKED)
        maze.append(row)
    return maze


def repr_maze(maze):
    return "\n".join("".join(row) for row in maze)


class Location(NamedTuple):
    row: int
    col: int


class Maze:

    def __init__(self, start: Location, goal: Location | int, favorite_number, rows: int = 50,
                 columns: int = 50) -> None:
        self._rows: int = rows
        self._columns: int = columns
        self.start: Location = start
        self.goal: Location = goal
        self._grid: list[list[Cell]] = create_maze(rows, columns, favorite_number)
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


def bfs_part2(initial: T, goal_test: int, successors: Callable[[T], list[T]]) -> Optional[Node[T]] | int:
    # frontier is where we've yet to go
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored is where we've been
    explored: Set[T] = {initial}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if len(node_to_path(current_node)) > goal_test:
            return len(explored)
        # check where we can go next and haven't explored
        for child in successors(current_state):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # went through everything and never found goal


def part_1(source, goal: Location = Location(39, 31)):
    maze = Maze(Location(1, 1), goal, int(source), rows=goal.row + 5, columns=goal.col + 5)
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
    maze = Maze(Location(1, 1), 50, int(source), rows=200, columns=200)
    return bfs_part2(maze.start, 50, maze.successors)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""10""")

    def test_generate_maze(self):
        expected = """ # #### ##
  #  #   #
#    ##   
### # ### 
 ##  #  # 
  ##    # 
#   ## ###"""
        self.assertEqual(expected, repr_maze(create_maze(7, 10, 10)))

    def test_example_data_part_1(self):
        self.assertEqual(11, part_1(self.test_source, Location(4, 7)))

    def test_part_1(self):
        self.assertEqual(82, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(138, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
