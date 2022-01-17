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
from pathlib import Path
from typing import Dict

from ivonet.csp import Constraint, V, D, CSP
from ivonet.files import read_rows
from ivonet.iter import ints, flatten, multimap

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse_instruction(line):
    return re.findall(' ([A-Z]) ', line)


class StepConstraint(Constraint[str, str]):

    def __init__(self, left: str, right: str) -> None:
        super().__init__([left, right])
        self.left: str = left
        self.right: str = right

    def satisfied(self, assignment: Dict[V, D]) -> bool:
        # continue if not yet processed
        if self.left not in assignment or self.right not in assignment:
            return True

        if self.right == assignment[self.left]:
            return False

        if self.left == assignment[self.right]:
            return False
        return True

        return False

    def __repr__(self) -> str:
        return f"StepConstraint<{self.left}, {self.right}>"


def part_1(source):
    steps = {tuple(parse_instruction(line)) for line in source}
    _(steps)
    variables = sorted(list(set(flatten(steps))))
    _(variables)
    domain = multimap((b, a) for a, b in steps)
    # domain = multimap(steps)
    for key in variables:
        if key not in domain:
            domain[key] = []
    # _(domain)
    # domain = {}
    # for key in variables:
    #     domain[key] = variables
    csp = CSP(variables, domain)
    for step in steps:
        csp.add_constraint(StepConstraint(*step))
    sol = csp.backtracking_search()
    _("!!", sol)
    return None


def part_2(source):
    ...


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""Step C must be finished before step A can begin.
Step A must be finished before step B can begin.""")

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
