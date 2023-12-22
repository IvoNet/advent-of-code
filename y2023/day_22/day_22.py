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
from dataclasses import dataclass
from pathlib import Path

import pyperclip

from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


@dataclass
class Brick:
    """
    I created this class to put the overlap logic in one place.
    maybee reusable in the future?

    - it handles the overlap logic for the x, y, and z axis
    - min and max values for each axis are calculated
    - In the end I wrote too many, more than I need so not all are proven correct :-)

    """
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

    def __repr__(self):
        return f"Brick({self.x1}, {self.y1}, {self.z1}, {self.x2}, {self.y2}, {self.z2})"

    @property
    def lowest_z(self):
        return min(self.z1, self.z2)

    @property
    def highest_z(self):
        return max(self.z1, self.z2)

    @property
    def lowest_x(self):
        return min(self.x1, self.x2)

    @property
    def highest_x(self):
        return max(self.x1, self.x2)

    @property
    def lowest_y(self):
        return min(self.y1, self.y2)

    @property
    def highest_y(self):
        return max(self.y1, self.y2)

    @property
    def volume(self):
        return (self.highest_x - self.lowest_x + 1) * (self.highest_y - self.lowest_y + 1) * (
                self.highest_z - self.lowest_z + 1)

    def overlaps_with(self, other):
        return self.overlaps_with_x(other) and self.overlaps_with_y(other) and self.overlaps_with_z(other)

    def overlaps_with_z(self, other):
        return self.lowest_z <= other.highest_z and self.highest_z >= other.lowest_z

    def overlaps_with_x(self, other):
        return self.lowest_x <= other.highest_x and self.highest_x >= other.lowest_x

    def overlaps_with_y(self, other):
        return self.lowest_y <= other.highest_y and self.highest_y >= other.lowest_y

    def overlaps_with_z_and_x(self, other):
        return self.overlaps_with_z(other) and self.overlaps_with_x(other)

    def overlaps_with_z_and_y(self, other):
        return self.overlaps_with_z(other) and self.overlaps_with_y(other)

    def overlaps_with_x_and_y(self, other):
        return self.overlaps_with_x(other) and self.overlaps_with_y(other)

    def __hash__(self):
        return hash((self.x1, self.y1, self.z1, self.x2, self.y2, self.z2))

    def __le__(self, other):
        """the z is the vertical axis so the lowest z is the lowest brick"""
        return self.lowest_z <= other.lowest_z

    def __lt__(self, other):
        return self.lowest_z < other.lowest_z

    def __gt__(self, other):
        return self.lowest_z > other.lowest_z


def parse_bricks(source) -> list[Brick]:
    """
    Parse the source into a list of bricks
    - each brick is a tuple of two tuples representing the two ends of the brick
    - each tuple represents the x, y, z coordinates of the end of the brick
    """
    bricks = []
    for line in source:
        bricks.append(Brick(*ints(line)))
    return bricks


def settle(bricks: list[Brick]) -> list[Brick]:
    """
    Simulates the settling of bricks in a 3D space.

    This method adjusts the z-coordinates of the bricks to simulate them falling down until they hit the
    ground or another brick.
    The bricks are processed in ascending order based on their lowest z-coordinate, simulating the order in
    which they would settle in a real-world scenario.

    Args:
        bricks (list[Brick]): A list of Brick objects representing the bricks in their initial positions.

    Returns:
        list[Brick]: The list of bricks with their adjusted z-coordinates after settling.
    """
    bricks = sorted(bricks)
    for idx, brick in enumerate(bricks):
        max_z = 1
        for other in bricks[:idx]:
            if brick.overlaps_with_x_and_y(other):
                max_z = max(max_z, other.highest_z + 1)
        brick.z2 -= brick.z1 - max_z
        brick.z1 = max_z
    return bricks


def brick_support_map(bricks: list[Brick]) -> tuple[dict, dict]:
    """
    Creates a double map of brick support relationships.
    It walks from top to bottom and checks if a brick is supported by another brick.
    It then creates two maps:
    - one maps a brick's index to a set of indices of bricks that it supports
      key_supports_value
    - one maps a brick's index to a set of indices of bricks that support it
      value_supports_key
    """
    key_supports_value: dict[Brick, set[Brick]] = {brick: set() for brick in bricks}
    value_supports_key: dict[Brick, set[Brick]] = {brick: set() for brick in bricks}

    for j, upper in enumerate(bricks):
        for i, lower in enumerate(bricks[:j]):
            if lower.overlaps_with_x_and_y(upper) and upper.z1 == lower.z2 + 1:
                key_supports_value[lower].add(upper)
                value_supports_key[upper].add(lower)
    return key_supports_value, value_supports_key


def part_1(source: str | list[str]) -> int | None:
    """
    Hmm, I hate 3D puzzles. My brain does not handle this well :-)
    it looks luke tetris + jenga... first tetris then jenga
    Trying to understand the problem:
    - We have a number of bricks
    - each brick represents a straight line of cubes
      note that in the digital world a cube can represent 1 unit while having no actual volume
      e.g. 2,2,2~2,2,2:
      In a traditional sense, this would mean the cube has no volume because its
      length, width, and height are all 0. But in this problem, it's specified that each brick is made up of a
      single straight line of cubes. So, even though the two ends of the brick are at the same coordinate,
      it doesn't mean the brick has no volume. Instead, it means the brick is a single cube, which occupies one
      unit of volume in the 3D space
    - note that the z axis is the vertical axis! and its minimum is 1.
    - ok I need to figure out how to compare bricks and how to determine if a brick is supported by another brick.
       -> Brick class where I only need to figure this out once!
    """
    bricks = settle(parse_bricks(source))
    key_supports_value, value_supports_key = brick_support_map(bricks)

    answer = 0
    for brick in bricks:
        for supported_brick in key_supports_value[brick]:
            if len(value_supports_key[supported_brick]) <= 1:
                break
        else:
            answer += 1
    pyperclip.copy(str(answer))
    return answer


def part_2(source: str | list[str]) -> int | None:
    """
    Calculates the total number of bricks that would fall if each brick were removed individually.

    This function first parses the input data into a list of Brick objects, then simulates the settling of the bricks.
    It then creates a double map of brick support relationships. For each brick, it performs a breadth-first search
    to find all the bricks that would fall if the current brick were removed. It counts the number of bricks that
    would fall for each brick and sums these counts to get the total number of bricks that would fall if each brick
    were removed individually.

    Args:
        source (str | list[str]): The input data, either as a string or a list of strings.

    Returns:
        int | None: The total number of bricks that would fall if each brick were removed individually, or None if
        the input data is invalid.
    """
    bricks = parse_bricks(source)
    bricks = settle(bricks)
    k_supports_v, v_supports_k = brick_support_map(bricks)

    answer = 0
    # bfs approach again but for all bricks
    # find how many bricks will fall if we remove the brick
    # do this for all the bricks
    # sum all those numbers
    # that is the answer
    for brick in bricks:
        # queue all the bricks support something which itself is only supporting itself
        q = collections.deque(j for j in k_supports_v[brick] if len(v_supports_k[j]) == 1)
        falling = set(q)
        falling.add(brick)
        while q:
            j = q.popleft()
            for k in k_supports_v[j] - falling:
                if v_supports_k[k] <= falling:
                    q.append(k)
                    falling.add(k)
        answer += len(falling) - 1

    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(5, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(499, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(7, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(95059, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
