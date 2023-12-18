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
from typing import Generator

from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


DIRECTIONS = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (1, 0),
    "D": (-1, 0),
}


@dataclass
class Instruction:
    """
    Class representing an instruction.
    dr -> direction row
    dc -> direction column
    steps -> number of steps to take in that direction
    """
    dr: int
    dc: int
    steps: int


def instruction_generator_1(source: list[str]) -> Generator[Instruction, None, None]:
    """
    Parse the instructions from the source list for part 1 of the problem.

    Each line in the source list should be in the format "DIRECTION STEPS COLOR", where:
    - DIRECTION is a single character representing the direction (R, L, U, D).
    - STEPS is an integer representing the number of steps to take in that direction.
    - COLOR is a string representing the color of the line (not used in part 1).

    Parameters:
    - source: A list of strings, each representing an instruction.

    Returns:
    - A list of Instruction objects, each representing an instruction.
    """
    for line in source:
        direction, steps, _ = line.strip().split(" ")
        dr, dc = DIRECTIONS[direction]
        yield Instruction(dr, dc, int(steps))


def instruction_generator_2(source: list[str]) -> Generator[Instruction, None, None]:
    """
    Parse the instructions from the source list for part 2 of the problem.

    Each line in the source list should be in the format "DIRECTION STEPS COLOR", where:
    - DIRECTION not used in part 2.
    - STEPS not used in part 2.
    - COLOR is a string representing the direction and the steps:
      - The last character of the COLOR determines the direction
        (0 means R, 1 means D, 2 means L, and 3 means U)
      - the first 5 chars if the color (excluding the #) represent the hexadecimal value of the steps.

    Parameters:
    - source: A list of strings, each representing an instruction.

    Returns:
    - A list of Instruction objects, each representing an instruction.
    """
    for line in source:
        _, _, c = line.strip().split()
        tmp = c[2:-1]
        # last char of tmp: 0 means R, 1 means D, 2 means L, and 3 means U
        dr, dc = DIRECTIONS["RDLU"[int(tmp[-1])]]
        steps = int(tmp[:-1], 16)  # first 5 chars of tmp represent the hexadecimal value of the steps
        yield Instruction(dr, dc, steps)


def shoelace_theorem(coords: list[tuple[int, int]]) -> float:
    """
    Calculate the area of a polygon using the Shoelace Theorem.
    https://en.wikipedia.org/wiki/Shoelace_formula

    Parameters:
    - coords: List of (row, column) pairs representing the vertices.

    Returns:
    - Area of the polygon.
    """
    n = len(coords)

    # Ensure the polygon is closed
    if coords[0] != coords[-1]:
        coords.append(coords[0])

    # Calculate the area using the Shoelace Theorem
    area = 0.0
    for i in range(n - 1):
        left_row, left_col = coords[i]
        right_row, right_col = coords[i + 1]
        area += left_row * right_col - right_row * left_col
    area = abs(area) // 2

    return area


def picks_theorem(area: float, boundary_points: int) -> float:
    """
    Calculate the number of interior points of a simple lattice polygon using Pick's Theorem.
    https://en.wikipedia.org/wiki/Pick%27s_theorem
    I changed this one to give the interior points instead of the area as I can get the area
    from the shoelace theorem, and I am missing the interior points.

    Parameters:
    - area: Area of the polygon.
    - boundary_points: Number of lattice points on the boundary.

    Returns:
    - Number of interior points.
    """
    interior_points = area - boundary_points // 2 + 1
    return interior_points


def calculate_cubic_meters(instructions):
    """
    Calculate the total number of cubic meters in a polygon.

    The method first creates a list of points that represent the vertices of the polygon based on the given
    instructions.
    Each instruction contains the direction and the number of steps to take in that direction.

    It then calculates the number of boundary points, which is the sum of the steps in all instructions.

    Next, it calculates the area of the polygon using the Shoelace Theorem, which is a formula for calculating the
    area of a polygon when the coordinates of its vertices are known.

    After that, it calculates the number of interior points using Pick's Theorem. Pick's Theorem states that the area
    of a simple lattice polygon is equal to the number of interior points plus half the number of boundary points
    minus 1. By rearranging this formula, we can solve for the number of interior points.

    Finally, it returns the sum of the boundary points and the interior points, which represents the total number
    of cubic meters in the polygon.

    Parameters:
    - instructions: A list of Instruction objects, each containing the direction and the number of steps to take in
      that direction.

    Returns:
    - The total number of cubic meters in the polygon.
    """
    points = [(0, 0)]
    boundary_points = 0
    for instruction in instructions:
        r, c = points[-1]
        boundary_points += instruction.steps
        points.append((r + instruction.dr * instruction.steps, c + instruction.dc * instruction.steps))
    p(f"boundary_points = {boundary_points}")
    area = shoelace_theorem(points)
    p(f"area = {area}")
    interior_points = picks_theorem(area, boundary_points)
    p(f"interior_points = {interior_points}")
    return boundary_points + interior_points


def part_1(source: list[str]) -> int:
    return int(calculate_cubic_meters(instruction_generator_1(source)))


def part_2(source: list[str]) -> int:
    return int(calculate_cubic_meters(instruction_generator_2(source)))


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(62, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(50603, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(952408144115, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(96556251590677, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
