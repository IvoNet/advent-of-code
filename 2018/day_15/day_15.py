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
from typing import NamedTuple, TypeVar

from ivonet import infinite
from ivonet.collection import Queue
from ivonet.files import read_rows
from ivonet.iter import ints
from ivonet.search import Node

sys.dont_write_bytecode = True
T = TypeVar('T')
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

    def repr_long(self):
        return f"{self.__class__.__name__}<pos={self.pos}, hp={self.hit_points}, ap={self.attack_power}>"


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


def manhatten_distance(left: Location, right: Location) -> int:
    return abs(left.row - right.row) + abs(left.col - right.col)


def node_to_path(node: Node[T]) -> list[T]:
    """This version removes the first state from the path as it is ourselves"""
    path: list[T] = [node.state]
    # work backwards from end to front
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path[1:]


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

    def attack(self, attacker: Unit, enemy: Unit):
        """Attack
        - When in range
        - reading order (top down, left-right)
        - starting positions in a round
        """
        enemy.hit_points -= attacker.attack_power

    def move(self, unit: Unit):
        """Move
        - get all open neighbors of targets
        - find the shortest route (bfs) (goal test
        - if tied in length choose the first in reading order
        - take 1 step towards the chosen goal
            - first clear the board of units
            - move
            - mark the board again with new state of units
        """
        step = self.shortest_2_enemy(unit)
        if step:
            self.clear_units()
            unit.pos = step
            self.mark_units()
        return unit

    def bfs(self, initial: T, target: T, max_dist=infinite):
        """Breath first search
        This bfs searches for all the shortest paths given a target
        """
        frontier: Queue[Node[T]] = Queue()
        frontier.push(Node(initial, None))
        explored: set[T] = {initial}
        all_paths = []
        while not frontier.empty:
            current_node: Node[T] = frontier.pop()
            current_state: T = current_node.state
            if target == current_state:
                path = tuple(node_to_path(current_node))
                if len(path) > max_dist:
                    return None
                all_paths.append(path)
            for child in self.bfs_successors(current_state):
                if child in explored:
                    continue
                explored.add(child)
                frontier.push(Node(child, current_node))
        return tuple(all_paths)

    def bfs_successors(self, point: Location):
        """See if there is a path to the target
        - find the successors
        - this function assumes that the Units have been marked on the board
        """
        locations: list[Location] = []
        if point.row + 1 < self._rows \
                and self._grid[point.row + 1][point.col] != Cell.BLOCKED \
                and not isinstance(self._grid[point.row + 1][point.col], Unit):
            locations.append(Location(point.row + 1, point.col))
        if point.row - 1 >= 0 \
                and self._grid[point.row - 1][point.col] != Cell.BLOCKED \
                and not isinstance(self._grid[point.row - 1][point.col], Unit):
            locations.append(Location(point.row - 1, point.col))
        if point.col + 1 < self._columns \
                and self._grid[point.row][point.col + 1] != Cell.BLOCKED \
                and not isinstance(self._grid[point.row][point.col + 1], Unit):
            locations.append(Location(point.row, point.col + 1))
        if point.col - 1 >= 0 \
                and self._grid[point.row][point.col - 1] != Cell.BLOCKED \
                and not isinstance(self._grid[point.row][point.col - 1], Unit):
            locations.append(Location(point.row, point.col - 1))
        return locations

    def shortest_2_enemy(self, unit: Unit):
        """Find all shortest paths of a route to chose the reading order if there are more shortests
        """
        _(unit.repr_long())
        # enemies = sorted([enemy for enemy in self._units if type(enemy) != type(unit)], key=lambda e: manhatten_distance(e.pos, unit.pos))
        enemies = [enemy for enemy in self._units if type(enemy) != type(unit)]
        shortest = []
        max_dist = infinite
        for enemy in enemies:
            # get the open neighbors of the enemy
            for target in self.bfs_successors(enemy.pos):
                if shortest:
                    max_dist = len(min(shortest))
                bfs = self.bfs(unit.pos, target, max_dist=max_dist)
                if bfs and len(bfs) > 0:
                    shortest.append(*bfs)
        if not shortest:
            return None
        return sorted(shortest)[0][0]

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

    def retrieve_units(self):
        self._units = [unit for r, row in enumerate(self._grid) for c, unit in enumerate(row) if isinstance(unit, Unit)]
        return self._units

    def parse(self, source) -> None:
        for r, line in enumerate(source):
            row = []
            for c, value in enumerate(line):
                loc = Location(r, c)
                if value in "GE":
                    unit = Goblin(loc) if value == "G" else Elf(loc)
                    self._units.append(unit)
                row.append(Cell.BLOCKED if value == "#" else Cell.EMPTY)
            self._grid.append(row)
        self.mark_units()

    def __repr__(self) -> str:
        ret = "\n".join("".join(str(col) for col in row) for row in self._grid)
        for unit in self.retrieve_units():
            ret += f"\n{unit.repr_long()}"
        return ret


def part_1(source):
    war = BeverageBandits(source)
    print(war)
    # war.mark_units()
    # print(war)
    # war.clear_units()
    # print(war)
    war.move(war._units[4])
    print(war)
    war.move(war._units[3])
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
        self.test_source_1 = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test_1.input")
        self.test_source_2 = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test_2.input")

    def test_example_data_1_part_1(self):
        self.assertEqual(None, part_1(self.test_source_1))

    def test_example_data_2_part_1(self):
        self.assertEqual(None, part_1(self.test_source_2))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
