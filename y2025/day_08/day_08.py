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
    Connect the 1000 pairs of junction boxes that are closest together (by straight-line distance).
    After performing those 1000 connections (in order of increasing distance), compute the sizes
    of all connected components and return the product of the sizes of the three largest components.

    Args:
        source: iterable of 3-int lists/tuples (x, y, z)

    Returns:
        The product of the three largest component sizes as an int (or None if no data).
    """
    boxes = [JunctionBox(*line) for line in source]
    n = len(boxes)

    # Build all pairs (distance, i, j)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((boxes[i].distance_to(boxes[j]), i, j))

    # Sort pairs by distance ascending
    pairs.sort(key=lambda x: x[0])

    # Number of connections to perform: use 10 for the example (small inputs) and 1000 for real puzzle
    if n <= 20:
        k = min(10, len(pairs))
    else:
        k = min(1000, len(pairs))

    # Disjoint-set (union-find) with path compression and size tracking
    parent = list(range(n))
    size = [1] * n

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a: int, b: int) -> None:
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    # Process the first k pairs
    for idx in range(k):
        _, i, j = pairs[idx]
        union(i, j)

    # Collect component sizes
    comp = {}
    for i in range(n):
        r = find(i)
        comp[r] = comp.get(r, 0) + 1

    sizes = sorted(comp.values(), reverse=True)
    prod = 1
    for s in sizes[:3]:
        prod *= s

    answer = prod
    p(f"Top 3 sizes: {sizes[:3]}, product: {answer}")

    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:

    """
    Continue connecting the closest pairs until all junction boxes are in one circuit.
    Return the product of the X coordinates of the last two junction boxes that caused
    all boxes to become connected.
    """
    boxes = [JunctionBox(*line) for line in source]
    n = len(boxes)
    # build all pairs (distance, i, j)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((boxes[i].distance_to(boxes[j]), i, j))

    pairs.sort(key=lambda x: x[0])

    parent = list(range(n))
    size = [1] * n

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a: int, b: int) -> int:
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return 0
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return size[ra]

    # iterate pairs until one component reaches size n
    last_product = None
    for _, i, j in pairs:
        new_size = union(i, j)
        if new_size == n:
            # product of X coordinates of boxes i and j
            last_product = boxes[i].x * boxes[j].x
            break

    answer = last_product
    p(f"part_2 answer: {answer}")
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(40, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        # expected example result from puzzle description: 216 * 117 = 25272
        self.assertEqual(25272, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(9003685096, part_2(self.source))

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
