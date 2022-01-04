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

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


FLOOR_PLAN_BAK = [
    (1, "SG"), (1, "SM"), (1, "PG"), (1, "PM"),
    (2, "TG"), (2, "RG"), (2, "RM"), (2, "CG"), (2, "CM"),
    (3, "TM")
]

ALLOWED = {
    "SG": 1,
    "SM": 1,
    "PG": 2,
    "PM": 2,
    "TG": 3,
    "TM": 3,
    "CG": 4,
    "CM": 4,
    "RG": 5,
    "RM": 5,
}

PART_1_FLOOR_PLAN = {
    1: ["SG", "SM", "PG", "PM", ],
    2: ["TG", "RG", "RM", "CG", "CM"],
    3: ["TM"],
    4: [],
}


def display_solution(path: List[State]):
    if len(path) == 0:  # sanity check
        return
    old_state: State = path[0]
    print(old_state)
    for current_state in path[1:]:
        if current_state.boat:
            print("{} missionaries and {} cannibals moved from the east bank to the west bank.\n"
                  .format(old_state.em - current_state.em, old_state.ec - current_state.ec))
        else:
            print("{} missionaries and {} cannibals moved from the west bank to the east bank.\n"
                  .format(old_state.wm - current_state.wm, old_state.wc - current_state.wc))
        print(current_state)
        old_state = current_state


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

    def __init__(self, floorplan: list[set], elevator: int = 0) -> None:
        self.floorplan: list[set] = deepcopy(floorplan)
        self.elevator: int = elevator
        self._hash = hash(repr(self))

    def goal_test(self) -> bool:
        """The goal has been reached when:
        - all generators and their microchips are on the forth floor
        """
        return not any(self.floorplan[:-1])

    def has_generators(self, floor) -> bool:
        return len([x for x in self.floorplan[floor] if x.endswith("G")]) > 0

    def has_correct_generator(self, microchip, floor) -> bool:
        return f"{microchip[0]}G" in self.floorplan[floor]

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
                    _(items)
                    if not (0 <= self.elevator + delta < len(self.floorplan)):
                        continue
                    new_floor_plan = deepcopy(self.floorplan)
                    for item in items:
                        _(self, items)
                        new_floor_plan[self.elevator].remove(item)
                        new_floor_plan[self.elevator + delta].add(item)
                    sucs.append(State(new_floor_plan, elevator=self.elevator + delta))
        return [x for x in sucs if x.is_legal]

    def __str__(self) -> str:
        ret = []
        for i, floor in enumerate(self.floorplan):
            level = ('[{}]' if self.elevator == i else ' {} ').format(i + 1)
            items = ' '.join(str(item) for item in sorted(floor))
            ret.append(f"{level} {items}")
        return "\n".join(reversed(ret))

    def __repr__(self) -> str:
        ret = []
        for items in self.floorplan:
            if items:
                ret.append(" ".join(repr(item) for item in sorted(items)))
            else:
                ret.append("-")
        return f"State<{self.elevator} {', '.join(ret)}>"

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


def part_1(source):
    start = parse(source)
    _(start)
    solution = bfs(start, State.goal_test, State.successors)
    return len(node_to_path(solution))


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_state_1(self):
        floor_plan = {
            1: ["SG", "SM", "PG", "PM", ],
            2: ["TG", "RG", "RM", "CG", "CM"],
            3: ["TM"],
            4: [],
        }
        self.assertTrue(State(floor_plan, 1).is_legal)

    def test_state_2(self):
        floor_plan = {
            1: ["PG", "PM", ],
            2: ["SG", "SM", "TG", "RG", "RM", "CG", "CM"],
            3: ["TM"],
            4: [],
        }
        self.assertTrue(State(floor_plan, 2).is_legal)

    def test_state_3(self):
        floor_plan = {
            1: ["PG", "PM", ],
            2: ["SG", "SM", "TG", "RG", "RM", "CG"],
            3: ["TM", "CM"],
            4: [],
        }
        self.assertTrue(State(floor_plan, 3).is_legal)

    def test_state_4(self):
        floor_plan = {
            1: ["SG", "PG", "PM", ],
            2: ["TG", "RG", "RM", "CG", "CM", "SM"],
            3: ["TM"],
            4: [],
        }
        self.assertFalse(State(floor_plan, 2).is_legal)

    def test_goal_1(self):
        floor_plan = {
            1: ["SG", "PG", "PM", ],
            2: ["TG", "RG", "RM", "CG", "CM", "SM"],
            3: ["TM"],
            4: [],
        }
        self.assertFalse(State(floor_plan, 2).goal_test())

    def test_goal_2(self):
        floor_plan = {
            1: [],
            2: [],
            3: [],
            4: ["SG", "PG", "PM", "TG", "RG", "RM", "CG", "CM", "SM", "TM"],
        }
        self.assertTrue(State(floor_plan, 4).goal_test())

    def test_successors_floor_1(self):
        floor_plan = {
            1: ["PG", "PM", ],
            2: ["TG", "RG", "RM", "CG", "CM", "SG", "SM", ],
            3: ["TM"],
            4: [],
        }
        successors = State(floor_plan, 1).successors()
        _(successors)
        self.assertEquals(2, len(successors))

    def test_successors_floor_2(self):
        floor_plan = {
            1: [],
            2: ["TG", "RG", "RM", "CG", "CM", "SG", "SM", "PG", "PM", ],
            3: ["TM"],
            4: [],
        }
        successors = State(floor_plan, 2).successors()
        _(successors)
        self.assertEquals(26, len(successors))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
