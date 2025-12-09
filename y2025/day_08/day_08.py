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


def compute_both(source):
    """Compute both part1 and part2 in a single pass over sorted pair distances.

    Returns a tuple (part1_answer, part2_answer).
    part1_answer: product of top-three component sizes after k connections (k=10 for small inputs, else 1000)
    part2_answer: product of X coordinates of the last two boxes that caused full connectivity (or None)
    """
    boxes = [JunctionBox(*line) for line in source]
    n = len(boxes)
    if n == 0:
        return None, None

    # Build and sort all pairs by distance using combinations for clarity
    import itertools
    pairs = [(boxes[i].distance_to(boxes[j]), i, j)
             for i, j in itertools.combinations(range(n), 2)]
    pairs.sort(key=lambda x: x[0])

    # Determine k for part1 ;-)
    if n <= 20:
        k = min(10, len(pairs))
    else:
        k = min(1000, len(pairs))

    # union-find
    parent = list(range(n))
    size = [1] * n

    def find(a: int) -> int:
        # path-compressing find
        root = a
        while parent[root] != root:
            root = parent[root]
        while parent[a] != root:
            nxt = parent[a]
            parent[a] = root
            a = nxt
        return root

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

    part1_answer = None
    part2_answer = None

    # iterate pairs, process in order
    for idx, (_d, i, j) in enumerate(pairs):
        union(i, j)

        # after processing k pairs (counting index from 0), record part1
        if idx + 1 == k:
            # compute component sizes using Counter for brevity
            roots = [find(v) for v in range(n)]
            sizes = sorted(collections.Counter(roots).values(), reverse=True)
            prod = 1
            for s in sizes[:3]:
                prod *= s
            part1_answer = prod

        # check if union made all connected
        if size[find(i)] == n:
            # product of X coordinates of the two boxes whose connection completed connectivity
            part2_answer = boxes[i].x * boxes[j].x
            break

    return part1_answer, part2_answer


@debug
@timer
def part_1(source) -> int | None:
    """
    Connect the 1000 pairs of junction boxes that are closest together (by straight-line distance).
    After performing those 1000 connections (in order of increasing distance), compute the sizes
    of all connected components and return the product of the sizes of the three largest components.

    Returns:
        The product of the three largest component sizes as an int (or None if no data).
    """
    # delegate to combined computation and return first result
    answer, _ = compute_both(source)
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
    # delegate to combined computation and return second result
    _, answer = compute_both(source)
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(40, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(97384, part_1(self.source))

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
