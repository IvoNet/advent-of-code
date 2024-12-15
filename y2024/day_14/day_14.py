#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2023 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import collections
import os
import sys
import unittest
from collections import abc, defaultdict
from pathlib import Path

import pyperclip

from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Robot:

    def __init__(self, position: tuple[int, int], velocity: tuple[int, int], boundary: tuple[int, int] = (101, 103)):
        self.position: tuple[int, int] = position
        self.velocity: tuple[int, int] = velocity
        self.boundary: tuple[int, int] = boundary

    def px(self) -> int:
        return self.position[0]

    def py(self) -> int:
        return self.position[1]

    def vx(self) -> int:
        return self.velocity[0]

    def vy(self) -> int:
        return self.velocity[1]

    def bx(self) -> int:
        return self.boundary[0]

    def by(self) -> int:
        return self.boundary[1]

    def move(self, steps: int = 1):
        """moves the robot according to its velocity for the given number of steps,
        making sure to teleport when it reaches the boundary"""
        for _ in range(steps):
            self.position = ((self.px() + self.vx()) % self.boundary[0], (self.py() + self.vy()) % self.boundary[1])

    def quadrant(self) -> int:
        """
        To determine the safest area, count the number of robots in each quadrant after 100 seconds.
        Robots that are exactly in the middle (horizontally or vertically) don't count as being in any quadrant
        """
        if self.px() == self.boundary[0] // 2 or self.py() == self.boundary[1] // 2:  # middle
            return 0
        if self.px() < self.boundary[0] // 2 and self.py() < self.boundary[1] // 2:  # top left
            return 1
        if self.px() > self.boundary[0] // 2 and self.py() < self.boundary[1] // 2:  # top right
            return 2
        if self.px() > self.boundary[0] // 2 and self.py() > self.boundary[1] // 2:  # bottom right
            return 3
        if self.px() < self.boundary[0] // 2 and self.py() > self.boundary[1] // 2:  # bottom left
            return 4

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        return f"Robot({self.px()},{self.py()}) -> ({self.vx()},{self.vy()})"


def parse(source, boundary) -> list[Robot]:
    robots: list[Robot] = []
    for line in source:
        coords = ints(line)
        robots.append(Robot((coords[0], coords[1]), (coords[2], coords[3]), boundary))
    return robots


def print_robots(robots: list[Robot]):
    if DEBUG:
        boundary = robots[0].boundary
        d = [["." for _ in range(boundary[0])] for _ in range(boundary[1])]
        for robot in robots:
            d[robot.py()][robot.px()] = "#"
        for row in d:
            print("".join(row))

@debug
@timer
def part_1(source, boundary=(101, 103), seconds=100) -> int | None:
    robots: list[Robot] = parse(source, boundary)
    for i in range(seconds):
        for robot in robots:
            robot.move()
        print_robots(robots)

    grid = [[0 for _ in range(boundary[0])] for _ in range(boundary[1])]
    for robot in robots:
        grid[robot.py()][robot.px()] += 1

    if DEBUG:
        for row in grid:
            print(row)

    d = defaultdict(int)
    for robot in robots:
        d[robot.quadrant()] += 1

    answer = d[1] * d[2] * d[3] * d[4]

    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source, boundary=(101, 103), seconds=10001) -> int | None:
    answer = 0
    robots: list[Robot] = parse(source, boundary)

    seen = {}
    while True:
        answer += 1
        d = [[" " for _ in range(boundary[0])] for _ in range(boundary[1])]
        for r in robots:
            r.move()
            d[r.py()][r.px()] = "#"
        picture = "\n".join(["".join(r) for r in d])
        if picture in seen:
            print(f"image seen before at {seen[picture]} stopping...")
            break
        seen[picture] = answer
        if "##########" in picture:  # this is hopefully part of the tree
            print(f"Step {answer}\n")
            print(picture)
            print("\n\n")
            break

    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(12, part_1(self.test_source, boundary=(11, 7)))

    def test_part_1(self) -> None:
        self.assertEqual(222062148, part_1(self.source))

    def test_part_2(self) -> None:
        self.assertEqual(7520, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
