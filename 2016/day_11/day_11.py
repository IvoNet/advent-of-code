#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import re
import sys
import unittest
from copy import deepcopy
from itertools import combinations
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints
from ivonet.search import bfs, node_to_path

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Item(object):
    """Item that is comparable and hashable and can represent itself"""
    def __init__(self, element):
        self.element = element

    def __repr__(self):
        return '{}<{}>'.format(self.__class__.__name__, self.element)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __lt__(self, other):
        return repr(self) < repr(other)


class Generator(Item):
    ...


class Microchip(Item):
    ...


class State(object):

    def __init__(self, floorplan: list[set], elevator: int = 0) -> None:
        self.floorplan: list[set] = floorplan
        self.elevator: int = elevator
        self._hash = hash(repr(self))

    def goal_test(self) -> bool:
        """The goal has been reached when:
        - all generators and their microchips are on the forth floor
        """
        return not any(self.floorplan[:-1])

    @property
    def is_legal(self) -> bool:
        """Rulez
        A state is not legal when:
        - a microchip is on a floor with a generator not its own
        """
        if self.elevator < 0:
            return False
        if self.elevator > 3:
            return False
        for floor in self.floorplan:
            generators = {x for x in floor if isinstance(x, Generator)}
            if not generators:
                continue
            chips = {x for x in floor if isinstance(x, Microchip)}
            if any(chip for chip in chips if not Generator(chip.element) in generators):
                return False
        return True

    def successors(self) -> list[State]:
        """create all new states from current state"""
        sucs: list[State] = []
        for delta in [-1, 1]:
            elevator = self.elevator + delta
            if not (0 <= elevator < len(self.floorplan)):
                continue
            for count in [2, 1]:
                for items in [list(x) for x in combinations(self.floorplan[self.elevator], count)]:
                    new_floor_plan = deepcopy(self.floorplan)
                    for item in items:
                        new_floor_plan[self.elevator].remove(item)
                        new_floor_plan[elevator].add(item)
                    sucs.append(State(new_floor_plan, elevator=elevator))
        return [x for x in sucs if x.is_legal]

    def __str__(self) -> str:
        ret = []
        for i, floor in enumerate(self.floorplan):
            level = ('[{}]' if self.elevator == i else ' {} ').format(i + 1)
            items = ' '.join(str(item) for item in sorted(floor))
            ret.append(f"{level} {items}")
        return "\n".join(reversed(ret))

    def __repr__(self) -> str:
        """All Pairs are interchangeble

        F3 .  .  .  .  .                    F3 .  .  .  .  .
        F2 .  .  .  LG LC                   F2 .  .  .  HG HC
        F1 .  .  HC .  .     equivalent to  F1 .  .  LC .  .
        F0 E  HG .  .  .                    F0 E  LG .  .  .

        So we need to make sure that the "visited" cache in the bfs function sees these states
        as the same. That is why we implement this in the __repr__ function as that is what we
        base our hash on.
        """
        ret = []
        for floor in self.floorplan:
            if floor:
                generators = {x for x in floor if isinstance(x, Generator)}
                chips = {x for x in floor if isinstance(x, Microchip)}
                pairs = [(x, y) for x in chips for y in generators if x.element == y.element]
                items = []
                for chip, generator in pairs:
                    items.append("P")
                    generators.remove(generator)
                    chips.remove(chip)
                for generator in generators:
                    items.append("G")
                for chip in chips:
                    items.append("C")
                ret.append(" ".join(items))
            else:
                ret.append('\xD8')
        ret.append(">")
        return f"{self.__class__.__name__}<{self.elevator}, {', '.join(ret)}>"

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return self._hash


def parse(source):
    re_object = re.compile(r'(\w+)(?:-compatible)? (generator|microchip)')
    floors = []
    for line in source:
        if not line.strip():
            continue
        floor = set()
        for element, type in re_object.findall(line):
            if type == 'generator':
                floor.add(Generator(element))
            elif type == 'microchip':
                floor.add(Microchip(element))
        floors.append(floor)
    return State(floors)


def display_solution(path: List[State]):
    if len(path) == 0:  # sanity check
        return
    old_state: State = path[0]
    print(old_state)
    for current_state in path[1:]:
        print(f"Elevator moved from floor {old_state.elevator + 1} to floor {current_state.elevator + 1}\n")
        print(current_state)
        old_state = current_state


def part_1(source):
    start = parse(source)
    solution = bfs(start, State.goal_test, State.successors)
    pad = node_to_path(solution)
    if DEBUG:
        display_solution(pad)
    return len(pad) - 1  # do not count the start state


def part_2(source):
    start: State = parse(source)
    start.floorplan[0].add(Generator("elerium"))
    start.floorplan[0].add(Microchip("elerium"))
    start.floorplan[0].add(Generator("dilithium"))
    start.floorplan[0].add(Microchip("dilithium"))
    solution = bfs(start, State.goal_test, State.successors)
    pad = node_to_path(solution)
    if DEBUG:
        display_solution(pad)
    return len(pad) - 1  # do not count the start state


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(37, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(61, part_2(self.source))

if __name__ == '__main__':
    unittest.main()
