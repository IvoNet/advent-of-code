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
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def repr_maze(maze):
    return "\n".join("".join(row) for row in maze)


class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "#"
    ELF = "E"
    GOBLIN = "G"
    PATH = "*"

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return repr(self)


class Location(NamedTuple):
    row: int
    col: int


@dataclass
class Unit:
    pos: Location
    hit_points: int = 200
    attack_power: int = 3


class Elf(Unit):
    def __repr__(self) -> str:
        return Cell.ELF

    def __str__(self) -> str:
        return repr(self)


class Goblin(Unit):
    def __repr__(self) -> str:
        return Cell.GOBLIN

    def __str__(self) -> str:
        return repr(self)


class BeverageBandits:

    def __init__(self, source) -> None:
        self._grid: list[list[Cell | Unit]] = []
        self._units: list[Unit] = []
        self.parse(source)
        self._rows = len(self._grid)
        self._columns = len(self._grid[0])

    def combat_round(self):
        """A round gives all units a turn"""
        ...

    def turn(self, unit):
        """A units turn
        - identify its enemy units
        - identify open space around targets (u,d,l,r)
            - if none end turn
        - if already in range:
            - attack
          else move
        """

    def move(self):
        """Move
        - get all open neighbors of targets
        - find the shortest route (bfs) (goal test
        - if tied in length choose the first in reading order
        - take 1 step towards the chosen goal
        """
        ...

    def attack(self):
        """Attack
        - When in range
        - reading order (top down, left-right)
        - starting positions in a round
        """
        ...

    def bfs_goal(self):
        """Test if goal has been reached"""
        ...

    def bfs_successors(self, point: Location):
        """See if there is a path to the target"""
        locations: list[Location] = []
        if point.row + 1 < self._rows and self._grid[point.row + 1][point.col] != Cell.BLOCKED:
            locations.append(Location(point.row + 1, point.col))
        if point.row - 1 >= 0 and self._grid[point.row - 1][point.col] != Cell.BLOCKED:
            locations.append(Location(point.row - 1, point.col))
        if point.col + 1 < self._columns and self._grid[point.row][point.col + 1] != Cell.BLOCKED:
            locations.append(Location(point.row, point.col + 1))
        if point.col - 1 >= 0 and self._grid[point.row][point.col - 1] != Cell.BLOCKED:
            locations.append(Location(point.row, point.col - 1))
        return locations

    def bfs(self):
        """Yup the breath-first-search function"""
        ...

    def shortest_paths(self):
        """Find all shortest paths of a route to chose the reading order if there are more shortests
        - or maybe give more weight to moving down then right? astar / dijkstra iso bfs?
        """
        ...

    def fight(self):
        """Let's fight!"""
        ...

    def mark(self, path: list[Location], start: Location, goal: Location):
        for loc in path:
            self._grid[loc.row][loc.col] = Cell.PATH
        self._grid[start.row][start.col] = Cell.START
        self._grid[goal.row][goal.col] = Cell.GOAL

    def clear(self, path: list[Location], start: Location, goal: Location):
        for loc in path:
            self._grid[loc.row][loc.col] = Cell.EMPTY
        self._grid[start.row][start.col] = Cell.EMPTY
        self._grid[goal.row][goal.col] = Cell.EMPTY

    def mark_units(self):
        for unit in self._units:
            self._grid[unit.pos.row][unit.pos.col] = unit

    def clear_units(self):
        for unit in self._units:
            self._grid[unit.pos.row][unit.pos.col] = Cell.EMPTY

    def parse(self, source) -> None:
        for r, line in enumerate(source):
            row = []
            for c, value in enumerate(line):
                loc = Location(r, c)
                if value in "GE":
                    unit = Goblin(loc) if value == "G" else Elf(loc)
                    self._units.append(unit)
                    # row.append(unit)
                # else:
                #     row.append(Cell.BLOCKED if value == "#" else Cell.EMPTY)
                row.append(Cell.BLOCKED if value == "#" else Cell.EMPTY)
            self._grid.append(row)

    def __repr__(self) -> str:
        return "\n".join("".join(str(col) for col in row) for row in self._grid)


def part_1(source):
    war = BeverageBandits(source)
    print(war)
    war.mark_units()
    print(war)
    war.clear_units()
    print(war)
    return None


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""""")

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
