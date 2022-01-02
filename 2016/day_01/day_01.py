#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import sys
import unittest
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def manhattan_distance(goal: Location) -> Callable[[Location], float]:
    def distance(ml: Location) -> float:
        xdist: int = abs(ml.col - goal.col)
        ydist: int = abs(ml.row - goal.row)
        return xdist + ydist

    return distance


class Location(NamedTuple):
    row: int
    col: int


class Instruction(NamedTuple):
    direction: str
    blocks: int


def parse(source: str) -> list[Instruction]:
    return [Instruction(x[0], int(x[1:])) for x in source.strip().split(", ")]


class City:

    def __init__(self, instructions: list[Instruction],
                 start: Location = Location(0, 0),
                 start_orientation="N") -> None:
        self.instructions = instructions
        self.start = start
        self.orientation = start_orientation
        self.directions = {
            "N": {
                "L": "W",
                "R": "E"
            },
            "E": {
                "L": "N",
                "R": "S"
            },
            "S": {
                "L": "E",
                "R": "W"
            },
            "W": {
                "L": "S",
                "R": "N"
            },
        }
        self.location = defaultdict(int)
        self.distance = manhattan_distance(self.start)
        self.history: list[Location] = []
        self.col = start.col
        self.row = start.row

    def current_location(self) -> Location:
        up = abs(self.location["N"] - self.location["S"])
        right = abs(self.location["E"] - self.location["W"])
        return Location(up, right)

    def walk(self) -> int:
        for direction, blocks in self.instructions:
            self.orientation = self.directions[self.orientation][direction]
            self.location[self.orientation] += blocks
        return self.distance(self.current_location())

    def visited(self) -> int:
        """Keeps track of the places we passed and if we cross one of those places again we be done."""
        for direction, blocks in self.instructions:
            self.orientation = self.directions[self.orientation][direction]
            if self.orientation == "E":
                col = self.col
                self.col += blocks
                for i in range(col, self.col):
                    loc = Location(self.row, i)
                    if self.visit(loc):
                        return self.distance(loc)
                continue
            if self.orientation == "W":
                col = self.col
                self.col -= blocks
                for i in range(col, self.col, -1):
                    loc = Location(self.row, i)
                    if self.visit(loc):
                        return self.distance(loc)
                continue
            if self.orientation == "N":
                row = self.row
                self.row += blocks
                for i in range(row, self.row):
                    loc = Location(i, self.col)
                    if self.visit(loc):
                        return self.distance(loc)
                continue
            if self.orientation == "S":
                row = self.row
                self.row -= blocks
                for i in range(row, self.row, -1):
                    loc = Location(i, self.col)
                    if self.visit(loc):
                        return self.distance(loc)

    def visit(self, loc: Location) -> bool:
        """Adds True if the location was already visited otherwize it adds the location to the
        history and returns False"""
        if loc in self.history:
            return True
        self.history.append(loc)
        return False

def part_1(source):
    instructions = parse(source)
    return City(instructions).walk()


def part_2(source):
    instructions = parse(source)
    return City(instructions).visited()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))

    def test_example_data_part_1(self):
        self.assertEqual(12, part_1("""R5, L5, R5, R3"""))

    def test_example_data_1_part_1(self):
        self.assertEqual(2, part_1("""R2, R2, R2"""))

    def test_part_1(self):
        self.assertEqual(230, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(4, part_2("R8, R4, R4, R8"))

    def test_part_2(self):
        self.assertEqual(154, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
