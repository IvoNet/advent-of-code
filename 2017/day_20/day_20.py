#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
This one is an exercise in comparablity.
No fancy stuff just OOP :-)
I butchered the equals and lt functions to get this one working.
"""

import os
import sys
import unittest
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Counter

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def p(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


@dataclass
class Coord:
    x: int
    y: int
    z: int

    def __lt__(self, other):
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)

    def __eq__(self, other):
        return all([self.x == other.x, self.y == other.y, self.z == other.z])

    def __hash__(self):
        return hash(repr(self))


class Position(Coord):

    @property
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

    def __init__(self, pid, line) -> None:
        self.id = pid
        nrs = ints(line)
        self.p: Position = Position(*nrs[0:3])
        self.v: Velocity = Velocity(*nrs[3:6])
        self.a: Acceleration = Acceleration(*nrs[6:])

    def update(self):
        self.v.update(self.a)
        self.p.update(self.v)

    @property
    def manhatten_distance(self):
        return self.p.manhatten_distance

    def __lt__(self, other):
        return self.p < other.p

    def __eq__(self, other):
        return self.p == other.p

    def __repr__(self) -> str:
        return f"P<id={self.id}, p={repr(self.p)}, dist={self.manhatten_distance}"

    def __hash__(self):
        return hash(self.p)


def parse(source):
    return [Particle(i, line) for i, line in enumerate(source)]


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
    start_distances = [x.manhatten_distance for x in buffer]
    for _ in range(1000):
        for particle in buffer:
            particle.update()
    stop_distances = [x.manhatten_distance for x in buffer]
    combi = [a - b for a, b in zip(stop_distances, start_distances)]
    smallest = combi.index(min(combi))
    return smallest


def part_2(source):
    """Ha tried it for 10000 times but also printed the index on when I found stuff
    proved that after about 38 iterations we hit the 'end'.
    """
    buffer = parse(source)
    for idx in range(50):
        for particle in buffer:
            particle.update()
        cnt = {k: v for k, v in Counter(buffer).items() if v > 1}
        if cnt:
            p(cnt, idx)
            l = len(buffer)
            buffer = [x for x in buffer if x not in cnt]
            assert l - sum(cnt.values()) == len(buffer), "something..."
    return len(buffer)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(243, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(648, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
