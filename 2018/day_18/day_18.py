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
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.grid import neighbor_values
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    return [list(line) for line in source]


class Location(NamedTuple):
    row: int
    col: int


class LumberConstructionProject:

    def __init__(self, source) -> None:
        self.matrix = parse(source)
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])
        self.size = self.rows * self.cols
        self.fn = {
            ".": self.open_to_tree,
            "|": self.tree_to_lumber,
            "#": self.lumber_to_open
        }
        self.states = []

    def open_to_tree(self, loc: Location):
        nbv = neighbor_values(self.matrix, loc)
        if nbv.count("|") >= 3:
            return "|"
        return "."

    def tree_to_lumber(self, loc: Location):
        nbv = neighbor_values(self.matrix, loc)
        if nbv.count("#") >= 3:
            return "#"
        return "|"

    def lumber_to_open(self, loc: Location):
        nbv = neighbor_values(self.matrix, loc)
        if nbv.count("#") >= 1 and nbv.count("|") >= 1:
            return "#"
        return "."

    def minute(self, cache=False):
        nm = []
        for r, row in enumerate(self.matrix):
            nr = []
            for c, acre in enumerate(row):
                nr.append(self.fn[acre](Location(r, c)))  # convenience funcion calling :-)
            nm.append(nr)
        if cache:
            self.states.append(self.matrix)
        self.matrix = nm

    def elapse(self, minutes) -> LumberConstructionProject:
        for _ in range(minutes):
            self.minute()
        return self

    def sustainable_after(self, minutes):
        for i in rangei(1, minutes):
            self.minute(cache=True)
            if self.matrix in self.states:
                start_rep = self.states.index(self.matrix)
                rep = i - start_rep
                _(rep, start_rep, minutes)
                state = start_rep + ((minutes - start_rep) % rep)
                _(state)
                self.matrix = self.states[state]
                _(self)
                return self.resource_value()

    def count(self, s: str):
        return sum(row.count(s) for row in self.matrix)

    def resource_value(self):
        return self.count("|") * self.count("#")

    def __repr__(self) -> str:
        return "\n".join("".join(row) for row in self.matrix)


def part_1(source):
    lcp = LumberConstructionProject(source)
    lcp.elapse(10)
    _(lcp)
    return lcp.resource_value()


def part_2(source):
    """Yeah this take way to long
    So start printing and look for a pattern.
    - Yup it happens so start collecting states
    - in my case after 426 steps a state is repeated every 28 seconds and that repeats for ever
      second after that
    - so something like... count the state 426 + ((1000000000 - 426) % 28) ?
    - so count the state resulting from that equation should do it
    """
    lcp = LumberConstructionProject(source)
    return lcp.sustainable_after(1000000000)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows(""".#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.""")

    def test_example_data_part_1(self):
        self.assertEqual(1147, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(594712, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(203138, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
