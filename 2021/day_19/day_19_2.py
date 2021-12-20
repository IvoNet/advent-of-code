#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import sys
import unittest
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


def get_rotations(x, y, z):
    return [
        (x, y, z),
        (-y, x, z),
        (-x, -y, z),
        (y, -x, z),
    ]


def get_z_orientations(x, y, z):
    return [
        (x, y, z),
        (x, z, -y),
        (x, -y, -z),
        (x, -z, y),
        (-z, y, x),
        (z, y, -x),
    ]


def get_orientations(x, y, z):
    for xi, yi, zi in get_z_orientations(x, y, z):
        yield from get_rotations(xi, yi, zi)


class Scanner:
    def __init__(self, n, positions):
        self.n = n
        self.orientations = [[] for i in range(24)]
        for x, y, z in positions:
            for p, pos in enumerate(get_orientations(x, y, z)):
                self.orientations[p].append(pos)
        self.fixed_beacons = None
        self.pos = None

    def __repr__(self):
        return f"<Scanner {self.n}>"

    def pairing_mode(self, scanners):
        if self.fixed_beacons is not None:
            return
        for scanner in scanners:
            if scanner.fixed_beacons is None:
                continue
            if self.find_overlap(scanner):
                return

    def find_overlap(self, other):
        for orientation in self.orientations:
            for fx, fy, fz in other.fixed_beacons:
                for bx, by, bz in orientation:
                    dx, dy, dz = (fx - bx, fy - by, fz - bz)
                    shifted_beacons = {(x + dx, y + dy, z + dz) for x, y, z in orientation}
                    common_beacons = shifted_beacons.intersection(other.fixed_beacons)
                    if len(common_beacons) >= 12:
                        self.fixed_beacons = shifted_beacons
                        self.pos = (dx, dy, dz)
                        return True

    def distance_to(self, other):
        ax, ay, az = self.pos
        bx, by, bz = other.pos
        return abs(ax - bx) + abs(ay - by) + abs(az - bz)


def part_1(source):
    scanners = []
    with open('day_19.txt') as f:
        for n, block in enumerate(f.read().split('\n\n')):
            lines = block.split('\n')
            positions = []
            for line in lines[1:]:
                pos = tuple(int(i) for i in line.strip().split(',') if line.strip())
                if pos:
                    positions.append(pos)
            scanners.append(Scanner(n, positions))

    s = scanners[0]
    s.fixed_beacons = set(s.orientations[0])
    s.pos = (0, 0, 0)

    while len([s for s in scanners if s.fixed_beacons is None]):
        for scanner in scanners:
            scanner.pairing_mode(scanners)

    beacons = set()
    for scanner in scanners:
        # beacons |= scanner.fixed_beacons
        beacons = beacons.union(scanner.fixed_beacons)

    print("Part 1:", len(beacons))

    print("Part 2:")
    max_dist = max(a.distance_to(b) for a, b in permutations(scanners, 2))
    print(max_dist)

    return len(beacons), max_dist


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_rows(f"day_{day}.input")

    def test_part_1(self):
        self.assertEqual(449, part_1(self.source)[0])

    def test_part_2(self):
        self.assertEqual(13128, part_1(self.source)[1])


if __name__ == '__main__':
    unittest.main()
