#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def step(position: tuple[int, int], trajectory: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    px, py = position
    tx, ty = trajectory
    px += tx
    py += ty
    if tx != 0:
        tx += -1 if tx > 0 else 1
    ty -= 1
    return (px, py), (tx, ty)


def target_area(s: str) -> tuple[tuple[int, int], tuple[int, int]]:
    sx, ex, sy, ey = ints(s)
    return (sx, ey), (ex, sy)


def area_contains(area: tuple[tuple[int, int], tuple[int, int]], point: tuple[int, int]) -> bool:
    top_left, bottom_right = area
    tx, ty = top_left
    bx, by = bottom_right
    px, py = point
    return tx <= px <= bx and by <= py <= ty  # <= because boundary is inclusive


def beyond_area(area: tuple[tuple[int, int], tuple[int, int]], point: tuple[int, int]) -> bool:
    top_left, bottom_right = area
    bx, by = bottom_right
    px, py = point
    return px > bx or py < by


def trace(area, position, trajectory):
    print(f"start[{position}], trajectory[{trajectory}]")
    if area_contains(area, position):
        print("Hit!")
        return
    if beyond_area(area, position):
        print("Fail!")
        return
    position, trajectory = step(position, trajectory)
    return trace(area, position, trajectory)


def part_1(source):  # 6,9
    target = target_area(source)
    top_left, bottom_right = target
    current = (0, 0)
    best = (0, 0)
    highest = (0, 0)
    total_steps = 0
    for x in range(0, bottom_right[0] + 1):
        for y in range(bottom_right[1] - 1, 100):
            current = (x, y)
            steps = 0
            hpoint = (0, 0)
            position = (0, 0)
            trajectory = (x, y)
            while not beyond_area(target, position):
                position, trajectory = step(position, trajectory)
                if position[1] > hpoint[1]:
                    hpoint = position
                steps += 1
                _(steps, position)
                if area_contains(target, position):
                    _(f"start[{current}], position[{position}], steps[{steps}], highest[{hpoint}]")
                    if hpoint[1] > highest[1]:
                        highest = hpoint
                        best = (x, y)
                        total_steps = steps
                        _(hpoint, end=' ')
                        break

    _()
    _(total_steps, highest, best, current)
    return highest[1]


def part_2(source):
    target = target_area(source)
    top_left, bottom_right = target
    good_start_velocities = set()
    for x in range(0, bottom_right[0] + 1):
        for y in range(bottom_right[1] - 1, 100):
            current = (x, y)
            position = (0, 0)
            trajectory = (x, y)
            while not beyond_area(target, position):
                position, trajectory = step(position, trajectory)
                if area_contains(target, position):
                    good_start_velocities.add(current)
                    break

    return len(good_start_velocities), good_start_velocities


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source = read_data("""target area: x=20..30, y=-10..-5""")
        self.test_velocities = (
            (23, -10), (25, -9), (27, -5), (29, -6), (22, -6), (21, -7), (9, 0), (27, -7), (24, -5),
            (25, -7), (26, -6), (25, -5), (6, 8), (11, -2), (20, -5), (29, -10), (6, 3), (28, -7),
            (8, 0), (30, -6), (29, -8), (20, -10), (6, 7), (6, 4), (6, 1), (14, -4), (21, -6),
            (26, -10), (7, -1), (7, 7), (8, -1), (21, -9), (6, 2), (20, -7), (30, -10), (14, -3),
            (20, -8), (13, -2), (7, 3), (28, -8), (29, -9), (15, -3), (22, -5), (26, -8), (25, -8),
            (25, -6), (15, -4), (9, -2), (15, -2), (12, -2), (28, -9), (12, -3), (24, -6), (23, -7),
            (25, -10), (7, 8), (11, -3), (26, -7), (7, 1), (23, -9), (6, 0), (22, -10), (27, -6),
            (8, 1), (22, -8), (13, -4), (7, 6), (28, -6), (11, -4), (12, -4), (26, -9), (7, 4),
            (24, -10), (23, -8), (30, -8), (7, 0), (9, -1), (10, -1), (26, -5), (22, -9), (6, 5),
            (7, 5), (23, -6), (28, -10), (10, -2), (11, -1), (20, -9), (14, -2), (29, -7), (13, -3),
            (23, -5), (24, -8), (27, -9), (30, -7), (28, -5), (21, -10), (7, 9), (6, 6), (21, -5),
            (27, -10), (7, 2), (30, -9), (21, -8), (22, -7), (24, -9), (20, -6), (6, 9), (29, -5),
            (8, -2), (27, -8), (30, -5), (24, -7),
        )

    def test_example_data_part_1(self):
        self.assertEqual(45, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(4186, part_1(self.source))

    def test_example_data_part_2(self):
        count, initial_velocities = part_2(self.test_source)
        self.assertEqual(112, count)
        self.assertEqual(sorted(self.test_velocities), sorted(initial_velocities))

    def test_part_2(self):
        self.assertEqual(2709, part_2(self.source)[0])


if __name__ == '__main__':
    unittest.main()
