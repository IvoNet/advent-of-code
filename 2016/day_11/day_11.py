#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import sys
import unittest
from copy import deepcopy
from itertools import combinations

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

FLOOR_PLAN = {
    1: ["SG", "SM", "PG", "PM", ],
    2: ["TG", "RG", "RM", "CG", "CM"],
    3: ["TM"],
    4: [],
}
MAX_NUM: int = 5


class State(object):

    def __init__(self, floorplan: dict[[int], list[str]], elevator: int = 1) -> None:
        self.floorplan: dict[[int], list[str]] = floorplan
        self.elevator: int = elevator

    def goal_test(self) -> bool:
        """The goal has been reached when:
        - all generators and their microchips are on the forth floor
        """
        return self.is_legal and len(self.floorplan[4]) == 10 and self.elevator == 4

    def has_generators(self, floor) -> bool:
        return len([x for x in self.floorplan[floor] if x.endswith("G")]) > 0

    def has_correct_generator(self, microchip, floor) -> bool:
        return f"{microchip[0]}G" in self.floorplan[floor]

    @property
    def is_legal(self) -> bool:
        """Rulez
        - if xM on floor then xG must be there or no other RTG
        - chips do not effect each other if there are no RTG's
        - you can only move from the floor with the elevator
        """
        if self.elevator < 1:
            return False
        if self.elevator > 4:
            return False
        for floor in self.floorplan:
            for chip in [x for x in self.floorplan[floor] if x.endswith("M")]:
                if not self.has_correct_generator(chip, floor) and self.has_generators(floor):
                    return False
        return True

    def successors(self) -> list[State]:
        """create all new states from current state"""
        sucs: list[State] = []
        if self.elevator == 1:  # can move up only
            for i in [1, 2]:
                for item in [list(x) for x in combinations(self.floorplan[self.elevator], i)]:
                    _(item)
                    fp = deepcopy(self.floorplan)
                    [fp[self.elevator].remove(x) for x in item]
                    fp[self.elevator + 1].extend(item)
                    sucs.append(State(fp, self.elevator + 1))
        elif self.elevator in [2, 3]:  # can move up and down
            for i in [1, 2]:
                for item in [list(x) for x in combinations(self.floorplan[self.elevator], i)]:
                    _(item)
                    fp = deepcopy(self.floorplan)
                    [fp[self.elevator].remove(x) for x in item]
                    fp_up = deepcopy(fp)
                    fp_down = deepcopy(fp)
                    fp_up[self.elevator + 1].extend(item)
                    sucs.append(State(fp_up, self.elevator + 1))
                    fp_down[self.elevator - 1].extend(item)
                    sucs.append(State(fp_down, self.elevator - 1))
        return [x for x in sucs if x.is_legal]
        # return list(set([x for x in sucs if x.is_legal]))

    def __str__(self) -> str:
        ret = ""
        for floor in self.floorplan:
            ret += f"Floor {floor} has the following items {sorted(self.floorplan[floor])}.\n"
        ret += f"The elevator is on floor {self.elevator}.\n"
        return ret

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other):
        if type(other) is not State:
            return False
        return self.floorplan == other.floorplan and self.elevator == other.elevator

    def __hash__(self):
        return hash(repr(self))


def part_1():
    return None


def part_2():
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()

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
        expected = {
            1: [],
            2: ["TG", "RG", "RM", "CG", "CM", "SG", "SM", "PG", "PM", ],
            3: ["TM"],
            4: [],
        }

        self.assertEquals([State(expected, 2)], State(floor_plan, 1).successors())

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
        self.assertEqual(None, part_1())

    def test_part_2(self):
        self.assertEqual(None, part_2())


if __name__ == '__main__':
    unittest.main()
