#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import os
import pickle
import sys
import unittest
from collections import defaultdict
from itertools import permutations
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def roll(v):
    """
    Roll is over X
    then
    - x stays the same (Using the Right-hand rule)
    - y becomes negative z
    - z becomes y
    """
    return v[0], v[2], -v[1]


def turn(v):
    return -v[1], v[0], v[2]


def parse(source: list[str]) -> dict[int, list[list[int, int, int]]]:
    ret = defaultdict(list)
    scanner = -1
    for line in source:
        if line.startswith("---"):
            scanner = ints(line)[0]
            continue
        xyz = ints(line)
        if len(xyz) != 3:
            continue
        ret[scanner].append(tuple(xyz))
    _("parse:", ret)
    return ret


def parse_scanners(source: list[str]) -> list[Scanner]:
    relative_beacon_positions = parse(source)
    scanners = []
    for k, v in relative_beacon_positions.items():
        scanners.append(Scanner(k, v))
    return scanners


class Scanner:

    def __init__(self, id: int, beacons: list[list[int, int, int]]) -> None:
        self.id = id
        self.orig = beacons.copy()
        self.current = beacons.copy()
        self.length = len(beacons)
        self.fixed_beacons = None
        self.locked = False
        self.pos = None

    def roll(self):
        ret = []
        for c in self.current:
            ret.append(roll(c))
        self.current = ret

    def turn(self):
        ret = []
        for c in self.current:
            ret.append(turn(c))
        self.current = ret

    def all(self):
        """https://stackoverflow.com/questions/16452383/how-to-get-all-24-rotations-of-a-3-dimensional-array
        """
        for _ in range(2):
            for action in "RTTTRTTTRTTT":
                if self.locked:
                    return
                if action == "R":
                    self.roll()
                    yield self.current
                else:
                    self.turn()
                    yield self.current
            # reorient to do the other 12 positions
            self.roll()
            self.turn()
            self.roll()

    def lock(self, beacons, position):
        self.locked = True
        self.fixed_beacons = beacons
        self.pos = position

    def find_overlap(self, other: Scanner) -> bool:
        if other.fixed_beacons is None:
            return False
        for current_orientation in self.all():
            for fx, fy, fz in other.fixed_beacons:
                for bx, by, bz in current_orientation:
                    dx, dy, dz = (fx - bx, fy - by, fz - bz)
                    shifted_beacons = {(x + dx, y + dy, z + dz) for x, y, z in current_orientation}
                    common_beacons = shifted_beacons.intersection(other.fixed_beacons)
                    if len(common_beacons) >= 12:
                        self.lock(shifted_beacons, (dx, dy, dz))
                        return True
        return False

    def manhattan_distance(self, other: Scanner):
        return abs(self.pos[0] - other.pos[0]) + abs(self.pos[1] - other.pos[1]) + abs(self.pos[2] - other.pos[2])

    def __repr__(self) -> str:
        return f"Scanner[{self.id}]"


def part_1(source):
    """
    scanner:
        - detect all units within 1000 units all axis
        - beacons relative to scanner (scanner as 0,0,0)
        - does not detect other scanners
        - does not know its own position
    beacon:
        - motionless
    region:
        - overlapping 12 beacons
    - finding pairs of scanners that have at least 12 overlapping beacons
    - reconstruct beacon map 1 scanner at the time

    https://www.euclideanspace.com/maths/geometry/rotations/axisAngle/examples/index.htm
    https://www.euclideanspace.com/maths/geometry/rotations/conversions/eulerToMatrix/examples/index.htm
    https://stackoverflow.com/questions/44073594/how-to-rotate-a-3d-matrix-along-x-y-or-z-axial-plane
    https://numpy.org/doc/stable/reference/generated/numpy.rot90.html
    https://matplotlib.org/stable/tutorials/toolkits/mplot3d.html#scatter-plots

    """
    scanners: list[Scanner] = parse_scanners(source)
    start_scanner = scanners.pop(0)
    start_scanner.fixed_beacons = set(start_scanner.current)
    start_scanner.locked = True
    start_scanner.pos = (0, 0, 0)
    matched = [start_scanner, ]

    try:
        with open(f"{os.path.dirname(__file__)}/day_19_matched.pickle", 'rb') as fi:
            matched = pickle.load(fi)
    except IOError:
        while len(scanners) != 0:
            for fixed in matched:
                for scanner in scanners:
                    if scanner.find_overlap(fixed):
                        print("Overlap found: ", scanner)
                        matched.append(scanner)
                        scanners.remove(scanner)
                        break

    beacons = set()
    for scanner in matched:
        beacons = beacons.union(scanner.fixed_beacons)
    part_1 = len(beacons)

    with open(f"{os.path.dirname(__file__)}/day_19_matched.pickle", "wb") as fo:
        pickle.dump(matched, fo, protocol=pickle.HIGHEST_PROTOCOL)

    return part_1


def part_2(source):
    scanners: list[Scanner] = parse_scanners(source)
    start_scanner = scanners.pop(0)
    start_scanner.fixed_beacons = set(start_scanner.current)
    start_scanner.locked = True
    start_scanner.pos = (0, 0, 0)
    matched = [start_scanner, ]

    try:
        with open(f"{os.path.dirname(__file__)}/day_19_matched.pickle", 'rb') as fi:
            matched = pickle.load(fi)
    except IOError:
        while len(scanners) != 0:
            for fixed in matched:
                for scanner in scanners:
                    if scanner.find_overlap(fixed):
                        print("Overlap found: ", scanner)
                        matched.append(scanner)
                        scanners.remove(scanner)
                        break

    with open(f"{os.path.dirname(__file__)}/day_19_matched.pickle", "wb") as fo:
        pickle.dump(matched, fo, protocol=pickle.HIGHEST_PROTOCOL)

    max_dist = max(a.manhattan_distance(b) for a, b in permutations(matched, 2))
    print(max_dist)

    return max_dist


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source_2 = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}_2.input")))

    def test_rotation(self):
        """All the orientations in this set of scanners should be
        found in the first scanner rotations"""
        scanners = parse_scanners(self.test_source_2)
        scanner = scanners.pop()
        for scnr in scanners:
            found = False
            for orientation in scanner.all():
                if orientation == scnr.current:
                    found = True
                    break
            self.assertTrue(found)

    def test_part_1(self):
        self.assertEqual(449, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(13128, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
