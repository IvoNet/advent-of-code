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
from itertools import count
from pathlib import Path
from typing import NamedTuple, TypeVar, Optional

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
    EMPTY = "."
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

    def hp(self):
        return f"{self.__class__.__name__[0]}({self.hit_points})"


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
        units = sorted(self._units.copy(), key=lambda u: u.pos)
        while units:
            self.turn(units.pop(0))

    def turn(self, unit: Unit):
        """A units turn
        - if we don't have anyone to attack see if we can move and then see if we can attack
        - if we can attack immediately then do so and turn is over
        """
        if unit.hit_points <= 0:
            return
        if not self.attack(unit):
            self.move(unit)
            self.attack(unit)

    def attack(self, attacker: Unit) -> bool:
        """Attack
        - When in range
        - reading order (top down, left-right)
        - starting positions in a round
        """
        enemy = self.within_attack_range(attacker)
        if enemy:
            enemy.hit_points -= attacker.attack_power
            if enemy.hit_points <= 0:
                _(attacker.repr_long(), "killed", enemy.repr_long())
                self.clear_units()
                self._units.remove(enemy)
                self.mark_units()
            return True
        return False

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

    def bfs(self, initial: T, target: T):
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

        TODO See if this one can be rewritten to == Cell.EMPTY? without the rest
        """
        locations: list[Location] = []
        if point.col + 1 < self._columns \
                and self._grid[point.row][point.col + 1] != Cell.BLOCKED \
                and not isinstance(self._grid[point.row][point.col + 1], Unit):
            locations.append(Location(point.row, point.col + 1))
        if point.row + 1 < self._rows \
                and self._grid[point.row + 1][point.col] != Cell.BLOCKED \
                and not isinstance(self._grid[point.row + 1][point.col], Unit):
            locations.append(Location(point.row + 1, point.col))
        if point.row - 1 >= 0 \
                and self._grid[point.row - 1][point.col] != Cell.BLOCKED \
                and not isinstance(self._grid[point.row - 1][point.col], Unit):
            locations.append(Location(point.row - 1, point.col))
        if point.col - 1 >= 0 \
                and self._grid[point.row][point.col - 1] != Cell.BLOCKED \
                and not isinstance(self._grid[point.row][point.col - 1], Unit):
            locations.append(Location(point.row, point.col - 1))
        return sorted(locations)

    def within_attack_range(self, attacker: Unit) -> Optional[Unit]:
        """See if there a target in range in reading order
        - top, down, left, right
        - choose the one with the lowest HP!
        """

        def is_enemy(u: Unit):
            """Are we standing next to an enemy?"""
            return isinstance(u, Unit) and type(u) != type(attacker)

        point = attacker.pos

        potential_enemies = []

        potential_enemy = self._grid[point.row][point.col + 1]
        if point.col + 1 < self._columns and is_enemy(potential_enemy):
            potential_enemies.append(potential_enemy)
        # above
        potential_enemy = self._grid[point.row - 1][point.col]
        if point.row - 1 >= 0 and is_enemy(potential_enemy):
            potential_enemies.append(potential_enemy)
        # under
        potential_enemy = self._grid[point.row + 1][point.col]
        if point.row + 1 < self._rows and is_enemy(potential_enemy):
            potential_enemies.append(potential_enemy)
        # left
        potential_enemy = self._grid[point.row][point.col - 1]
        if point.col - 1 >= 0 and is_enemy(potential_enemy):
            potential_enemies.append(potential_enemy)
        if potential_enemies:
            return min(potential_enemies, key=lambda u: u.hit_points)
        return None

    def shortest_2_enemy(self, unit: Unit):
        """Find all shortest paths of a route to chose the reading order if there are more shortest paths'
        we actually find the shortest routes to the open spaces next to the enemy.
        """
        enemies = [enemy for enemy in self._units if type(enemy) != type(unit)]
        shortest = []
        for enemy in enemies:
            for target in self.bfs_successors(enemy.pos):
                paths = self.bfs(unit.pos, target)
                if paths and len(paths) > 0:
                    shortest.append(*paths)
        if not shortest:
            return None
        return sorted(shortest, key=lambda u: (len(u), u[0]))[0][0]

    def fight(self):
        """fight!"""
        _(f"Initially:")
        _(self.repr_state())

        for i in count(1):
            self.combat_round()
            _(f"After {i} round(s):")
            _(self.repr_state())
            goblins = [u for u in self._units if isinstance(u, Goblin)]
            elves = [u for u in self._units if isinstance(u, Elf)]
            if not goblins or not elves:
                total = sum(u.hit_points for u in self._units)
                _(i, total)
                return (i - 1) * total
        return None

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

    def repr_units(self):
        ret = ""
        for unit in self.retrieve_units():
            ret += f"\n{unit.repr_long()}"
        return ret

    def repr_state(self):
        ret = []
        for row in self._grid:
            r = "".join(str(col) for col in row) + "   "
            r += ", ".join(u.hp() for u in row if isinstance(u, Unit))
            ret.append(r)
        return "\n".join(ret)

    def __repr__(self) -> str:
        ret = "\n".join("".join(str(col) for col in row) for row in self._grid)
        return ret


def part_1(source):
    beverage_bandits = BeverageBandits(source)
    return beverage_bandits.fight()


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
        self.test_source_3 = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test_3.input")
        self.test_source_4 = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test_4.input")
        self.test_source_5 = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test_5.input")
        self.test_source_6 = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test_6.input")
        self.test_source_7 = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test_7.input")
        self.test_source_8 = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test_8.input")

    def test_attackers_in_range(self):
        bb = BeverageBandits(self.test_source_2)
        self.assertFalse(bb.within_attack_range(bb._units[0]))
        self.assertTrue(bb.within_attack_range(bb._units[1]))
        self.assertEqual("Goblin<pos=Location(row=2, col=5), hp=200, ap=3>",
                         bb.within_attack_range(bb._units[1]).repr_long())
        self.assertEqual("Elf<pos=Location(row=2, col=4), hp=200, ap=3>",
                         bb.within_attack_range(bb._units[2]).repr_long())
        self.assertFalse(bb.within_attack_range(bb._units[4]))

    def test_move_single_unit(self):
        bb = BeverageBandits(self.test_source_2)
        _(bb)
        self.assertEquals("Goblin<pos=Location(row=1, col=3), hp=200, ap=3>", bb.move(bb._units[0]).repr_long())
        _(bb)
        self.assertEquals("Goblin<pos=Location(row=1, col=4), hp=200, ap=3>", bb.move(bb._units[0]).repr_long())
        _(bb)
        self.assertEquals("Goblin<pos=Location(row=3, col=3), hp=200, ap=3>", bb.move(bb._units[4]).repr_long())
        _(bb)
        self.assertEquals("Goblin<pos=Location(row=2, col=3), hp=200, ap=3>", bb.move(bb._units[4]).repr_long())
        _(bb)

    def test_move_single_unit_test_data_3(self):
        bb = BeverageBandits(self.test_source_3)
        _(bb)
        self.assertEquals("Goblin<pos=Location(row=1, col=2), hp=200, ap=3>", bb.move(bb._units[0]).repr_long())
        _(bb)

    def test_single_combat_round(self):
        bb = BeverageBandits(self.test_source_3)
        self.assertEqual("""#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########""", repr(bb))
        bb.combat_round()
        self.assertEqual("""#########
#.G...G.#
#...G...#
#...E..G#
#.G.....#
#.......#
#G..G..G#
#.......#
#########""", repr(bb))
        _(bb)
        bb.combat_round()
        self.assertEqual("""#########
#..G.G..#
#...G...#
#.G.E.G.#
#.......#
#G..G..G#
#.......#
#.......#
#########""", repr(bb))
        _(bb)
        bb.combat_round()
        self.assertEqual("""#########
#.......#
#..GGG..#
#..GEG..#
#G..G...#
#......G#
#.......#
#.......#
#########""", repr(bb))
        _(bb)

    def test_example_data_2_part_1(self):
        self.assertEqual(27730, part_1(self.test_source_2))

    def test_example_data_4_part_1(self):
        self.assertEqual(36334, part_1(self.test_source_4))

    def test_example_data_5_part_1(self):
        self.assertEqual(39514, part_1(self.test_source_5))

    def test_example_data_6_part_1(self):
        self.assertEqual(27755, part_1(self.test_source_6))

    def test_example_data_7_part_1(self):
        self.assertEqual(28944, part_1(self.test_source_7))

    def test_example_data_8_part_1(self):
        self.assertEqual(18740, part_1(self.test_source_8))

    def test_part_1(self):
        self.assertEqual(188576, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
