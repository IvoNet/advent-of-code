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

    def __init__(self, floorplan: list[set], elevator: int = 0, name_cache={}) -> None:
        self.floorplan: list[set] = deepcopy(floorplan)
        self.elevator: int = elevator
        self._hash = hash(repr(self))
        self.name_cache = name_cache

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
            for count in [1, 2]:
                for items in [list(x) for x in combinations(self.floorplan[self.elevator], count)]:
                    elevator = self.elevator + delta
                    if not (0 <= elevator < len(self.floorplan)):
                        break
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

        """
        ret = []
        ret.append(self.__class__.__name__)
        ret.append("<")
        ret.append(str(self.elevator))
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
                ret.append('<empty>')
        ret.append(">")
        return f"{self.__class__.__name__}<{self.elevator}, {', '.join(ret)}>"

    # def __repr__(self) -> str:
    #     """Works but is very slow as the ordering and names are seen as different things
    #     runs on my computer in about 379 seconds
    #     """
    #     ret = []
    #     for items in self.floorplan:
    #         if items:
    #             ret.append(" ".join(repr(item) for item in sorted(items)))
    #         else:
    #             ret.append("<empty>")
    #     return f"State<{self.elevator} {', '.join(ret)}>"

    # def __repr__(self):
    #     '''Simple output for repr that doesn't include steps (since this is used by hash).
    #     idea gotten from here:
    #     https://blog.jverkamp.com/2016/12/11/aoc-2016-day-11-radiation-avoider/
    #     This one runs in about 90 seconds on my compyter
    #     '''
    #
    #     # Optimization: Parts are interchangeable, rewrite them by order
    #     # This will assign an index the first time it sees a name and use that any more
    #     # So parts will always be ordered from lowest to highest, ties broken alphabetically
    #     def ordered_rewrite(m, cache={}):
    #         klazz, name = m.groups()
    #
    #         if name not in cache:
    #             cache[name] = str(len(cache))
    #
    #         return '{}{}'.format(klazz[0], cache[name])
    #
    #     ret = []
    #     for items in self.floorplan:
    #         if items:
    #             ret.append(' '.join(repr(item) for item in sorted(items)))
    #         else:
    #             ret.append('<empty>')
    #
    #     return re.sub(r'(Microchip|Generator)<([^<>]+)>',
    #                   ordered_rewrite,
    #                   'State<{}, {}>'.format(self.elevator, ', '.join(ret)),
    #                   )

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
    display_solution(pad)
    return len(pad) - 1


def part_2(source):
    start: State = parse(source)
    start.floorplan[0].add(Generator("elerium"))
    start.floorplan[0].add(Microchip("elerium"))
    start.floorplan[0].add(Generator("dilithium"))
    start.floorplan[0].add(Microchip("dilithium"))
    solution = bfs(start, State.goal_test, State.successors)
    pad = node_to_path(solution)
    display_solution(pad)
    return len(pad) - 1


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
