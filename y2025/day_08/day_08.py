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
import unittest
from pathlib import Path
from typing import NamedTuple

import pyperclip
import sys
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_int_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class JunctionBox(NamedTuple):
    x: int
    y: int
    z: int

    def __repr__(self):
        return f"JunctionBox(X: {self.x}, Y: {self.y}, Z: {self.z})"

    # rely on the auto-generated constructor from NamedTuple

    def distance_to(self, other: "JunctionBox") -> float:
        """Return the straight-line (Euclidean) distance to another 3D point.

        Args:
            other: Another JunctionBox representing the target point.

        Returns:
            The Euclidean distance as a float.
        """
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return (dx * dx + dy * dy + dz * dz) ** 0.5


@debug
@timer
def part_1(source) -> int | None:
    """

    """
    answer = 0
    closest_left = None
    closest_right = None
    boxes = [JunctionBox(*line) for line in source]
    min_dist = float('inf')
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            # find the closest two boxes (left, right)
            dist = boxes[i].distance_to(boxes[j])
            if min_dist > dist:
                min_dist = dist
                closest_left = boxes[i]
                closest_right = boxes[j]

    p(f"The closest boxes are {closest_left} and {closest_right} with a distance of {min_dist:.2f}")


    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    answer = 0
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(40, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def test_distance(self) -> None:
        a = JunctionBox(0, 0, 0)
        b = JunctionBox(1, 2, 2)
        # sqrt(1^2 + 2^2 + 2^2) == 3.0
        self.assertAlmostEqual(3.0, a.distance_to(b))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_int_rows(f"{folder}/day_{day}.input")
        self.test_source = read_int_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
