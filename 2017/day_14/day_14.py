#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import sys
import unittest
from functools import reduce
from pathlib import Path

from ivonet.files import read_data
from ivonet.graph import Graph
from ivonet.grid import neighbors
from ivonet.iter import ints, chunkify

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


HEX_BIN = {hex(i)[2:]: bin(i)[2:].zfill(4) for i in range(16)}


def hexbin(data: str):
    return "".join(HEX_BIN[c] for c in data)


class Knotter:
    """Circular knot-tying hasher
    A class to be able to remember state between actions.
    Proved to be handy.
    """

    def __init__(self, sequence: list[int], circle: int = 256, extra=[17, 31, 73, 47, 23]) -> None:
        self.sequence: list[int] = [ord(x) for x in sequence] + extra
        self.knot_circle: list[int] = list(range(circle))
        self.size: int = len(self.knot_circle)
        self.skip: int = 0
        self.head: int = 0

    def step(self):
        """Generator for yielding the steps one at the time.
        This way it is clear when to update the head and skip step
        Took me a while to see that it had to be updated after
        and skip at the end
        """
        for step in self.sequence:
            # _("step", step, "head", self.head, "skip", self.skip)
            yield self._next(step)
            self.head = (self.head + step + self.skip) % self.size
            self.skip += 1

    def _next(self, step):
        """Does the actual flipping.
        Had a bit of trouble finding the correct +1 -1 stuff as always :-)

        - copy the current knot_circle to change it
        - we know our head position and how many steps to take
        - so change in the new array the position from the circle in reverse
          keeping the size of the list in mind by doing the modulo thing to wrap
        - assing the changed list to the state
        """
        new = self.knot_circle.copy()
        for i in range(step):
            new[(self.head + i) % self.size] = self.knot_circle[(self.head + step - i - 1) % self.size]
        self.knot_circle = new
        return self.knot_circle

    def hash_1(self):
        """Simple hash (version 1)
        as we are not actially doing anything with the results of the for loop but only
        with the end state I made it a debug print statement :-)
        """
        for i, c in enumerate(self.step()):
            # _(i, c)
            pass
        return self.knot_circle[0] * self.knot_circle[1]

    def sparce_hash(self, cycles=64):
        for _ in range(cycles):
            self.hash_1()

    def dence_hash(self):
        """Dence hash
        - the chunkify function I had already figured out another time
        - I tried the reduce and that worked just fone so no only the zfill and voila
        """
        return "".join(hex(x)[2:].zfill(2) for x in
                       [reduce(lambda x, y: x ^ y, chunk) for chunk in chunkify(self.knot_circle, 16)])

    def hash_2(self):
        self.sparce_hash()
        return self.dence_hash()



def part_1(source):
    total = 0
    for row in range(128):
        knot_hasher = Knotter(f"{source}-{row}").hash_2()
        total += hexbin(knot_hasher).count("1")
    return total


def part_2(source):
    """A Graph puzzle!
    first pass
    - greate the graph
    - initialize a grid with bools default false 128x128 for the edges later
    - hash the rows with the knotter function of day 10
    - hexlify the hash
    - flip the grid coordinates to True of the col of that row is "1"
    - if "1" then add a vertex to the graph (row, col)
    second pass
    - add the edges by looking at the neigbors of a coordinate
      I have a function for that so that I do not have to figure that out every time :-)
    - Only use the neigbors if their respective coordinates in the grid are True
    - create an edge in the graph from the current coordinate to the neigbor
    Lastly:
    - do the dfs search for all the vertices and get the length of the connected_components (groups)
    """
    graph: Graph[tuple] = Graph()
    grid = [[False for _ in range(128)] for _ in range(128)]
    for row in range(128):
        knot_hasher = Knotter(f"{source}-{row}").hash_2()
        hb = hexbin(knot_hasher)
        for col, ch in enumerate(hb):
            if ch == "1":
                graph.add_vertex((row, col))
                grid[row][col] = True

    for row in range(128):
        for col in range(128):
            if grid[row][col]:
                for coord in [(r, c) for r, c in neighbors(grid, (row, col), diagonal=False) if grid[r][c]]:
                    graph.add_edge_by_vertices((row, col), coord)

    return graph.number_connected_groups()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""flqrgnkx""")

    def test_example_data_part_1(self):
        self.assertEqual(8108, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(8106, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(1242, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(1164, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
