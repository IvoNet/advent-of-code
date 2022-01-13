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
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


@dataclass
class Coord:
    x: int
    y: int
    z: int


class Position(Coord):

    def manhatten_distance(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def update(self, velocity: Velocity):
        self.x += velocity.x
        self.y += velocity.y
        self.z += velocity.z


class Velocity(Coord):

    def update(self, accelerate: Acceleration):
        self.x += accelerate.x
        self.y += accelerate.y
        self.z += accelerate.z


class Acceleration(Coord):
    ...


class Particle:

    def __init__(self, line) -> None:
        nrs = ints(line)
        self.p: Position = Position(*nrs[0:3])
        self.v: Velocity = Velocity(*nrs[3:6])
        self.a: Acceleration = Acceleration(*nrs[6:])

    def update(self):
        self.v.update(self.a)
        self.p.update(self.v)

    def manhatten_distance(self):
        return self.p.manhatten_distance()

    def __lt__(self, other):

    def __eq__(self, other):
        return self.p == other.p


def parse(source):
    return [Particle(line) for line in source]


def part_1(source):
    """So a bit of just do it :-)
    No real science here
    - get the start manhatten distance
    - iterate a couple of times
    - get the dist again
    - calc the diff
    - find the smallest
    - look that smallest up in the same diff list (same order as the buffer)
    - get the index where it lives... done
    """
    buffer = parse(source)
    start_distances = [x.manhatten_distance() for x in buffer]
    for _ in range(1000):
        for particle in buffer:
            particle.update()
    stop_distances = [x.manhatten_distance() for x in buffer]
    combi = [a - b for a, b in zip(stop_distances, start_distances)]
    smallest = combi.index(min(combi))
    return smallest


def part_2(source):
    buffer = parse(source)
    start_distances = [x.manhatten_distance() for x in buffer]
    for _ in range(1000):
        for particle in buffer:
            particle.update()
    stop_distances = [x.manhatten_distance() for x in buffer]
    combi = [a - b for a, b in zip(stop_distances, start_distances)]
    smallest = combi.index(min(combi))
    return smallest


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(243, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
