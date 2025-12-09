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

import pyperclip
import sys
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.grid import Location, manhattan_distance
from ivonet.iter import ints
from y2018.day_06.day_06 import manhatten_distance

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


@debug
@timer
def part_1(source) -> int | None:
    # Find the largest rectangle area that can be formed using any two red tiles as opposite corners.
    coordinats = [Location(*ints(line)) for line in source]

    if not coordinats:
        pyperclip.copy(str(None))
        return None

    # Keep track of the pair with the largest Manhattan distance (for logging), but compute max area across all pairs.
    longest_manhattan_distance = 0
    corner_l = None
    corner_r = None
    max_area = 0

    # Iterate all pairs (O(n^2)); n ~ 500 so this is fine.
    for i, left in enumerate(coordinats):
        mh = manhattan_distance(left)
        for right in coordinats[i + 1:]:
            # Manhattan bookkeeping
            dist = mh(right)
            if dist > longest_manhattan_distance:
                longest_manhattan_distance = dist
                corner_l = left
                corner_r = right

            # Rectangle area: inclusive tiles between coordinates
            # Location is (row, col) but the product of deltas is symmetric so ordering doesn't matter.
            height = abs(left.row - right.row) + 1
            width = abs(left.col - right.col) + 1
            area = width * height
            if area > max_area:
                max_area = area

    p(f"Longest manhatten distance is {longest_manhattan_distance} between {corner_l} and {corner_r}")
    p(f"Maximum rectangle area found: {max_area}")

    pyperclip.copy(str(max_area))
    return max_area


@debug
@timer
def part_2(source) -> int | None:
    """
    Part 2: Find largest rectangle with red corners that only contains red/green tiles.
    Red tiles are connected by green tiles forming a closed polygon.
    Green tiles are the boundary lines AND all tiles inside the polygon.

    Optimization: Instead of checking every tile, we check if any polygon edge
    crosses into the rectangle interior. A rectangle is valid if all its tiles
    are inside or on the polygon boundary.
    """
    # Parse coordinates - these form a closed polygon in order
    coordinates = [Location(*ints(line)) for line in source]

    if not coordinates:
        pyperclip.copy(str(None))
        return None

    n = len(coordinates)
    red_tiles = set(coordinates)

    # Build edge list for the polygon (each edge is axis-aligned)
    edges = []
    for i in range(n):
        start = coordinates[i]
        end = coordinates[(i + 1) % n]
        edges.append((start, end))

    def rectangle_is_valid(r1, c1, r2, c2):
        """
        Check if rectangle from (r1,c1) to (r2,c2) contains only red/green tiles.
        This is true if:
        1. The rectangle is entirely inside or on the polygon boundary
        2. No polygon edge crosses into the rectangle's interior from outside

        Key insight: For a rectangle with red corners to be valid, every edge of
        the polygon that enters the rectangle must stay on the boundary or be
        entirely inside. We check if any edge "cuts through" the rectangle interior.
        """
        min_r, max_r = min(r1, r2), max(r1, r2)
        min_c, max_c = min(c1, c2), max(c1, c2)

        # For each polygon edge, check if it creates a "cut" through the rectangle
        # that would leave tiles outside the polygon inside the rectangle
        for (p1, p2) in edges:
            er1, ec1 = p1.row, p1.col
            er2, ec2 = p2.row, p2.col

            if er1 == er2:  # Horizontal edge
                edge_row = er1
                edge_min_c = min(ec1, ec2)
                edge_max_c = max(ec1, ec2)

                # Edge is inside rectangle's row range (strictly inside, not on boundary)
                if min_r < edge_row < max_r:
                    # Check if edge overlaps with rectangle's column range
                    if edge_min_c < max_c and edge_max_c > min_c:
                        # This edge cuts horizontally through the rectangle
                        return False

            else:  # Vertical edge (ec1 == ec2)
                edge_col = ec1
                edge_min_r = min(er1, er2)
                edge_max_r = max(er1, er2)

                # Edge is inside rectangle's column range (strictly inside)
                if min_c < edge_col < max_c:
                    # Check if edge overlaps with rectangle's row range
                    if edge_min_r < max_r and edge_max_r > min_r:
                        # This edge cuts vertically through the rectangle
                        return False

        return True

    # Now find the largest rectangle with red corners where all tiles are valid
    max_area = 0
    best_pair = None

    # Check all pairs of red tiles as opposite corners
    # Sort by potential area (descending) for early termination
    coords_list = list(coordinates)
    pairs = []
    for i, left in enumerate(coords_list):
        for j in range(i + 1, len(coords_list)):
            right = coords_list[j]
            height = abs(left.row - right.row) + 1
            width = abs(left.col - right.col) + 1
            area = width * height
            pairs.append((area, left, right))

    # Sort by area descending for potential early exit
    pairs.sort(reverse=True)

    for area, left, right in pairs:
        # Early termination: if current max area is already bigger, we can stop
        if area <= max_area:
            break

        if rectangle_is_valid(left.row, left.col, right.row, right.col):
            if area > max_area:
                max_area = area
                best_pair = (left, right)

    p(f"Maximum valid rectangle area: {max_area}")
    if best_pair:
        p(f"Best pair: {best_pair}")
    pyperclip.copy(str(max_area))
    return max_area


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(50, part_1(self.test_source))

    def test_part_1(self) -> None:
        # expected value will be filled by running the test once; keep an assertion so CI fails if it changes unexpectedly
        self.assertEqual(4748985168, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(24, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(1550760868, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
