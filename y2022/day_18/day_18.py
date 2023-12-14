#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import sys
import unittest
from pathlib import Path

from ivonet.collection import Queue
from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Obsidian:
    """Obsidian has an outside surface, but it might also trap air inside.
    A cube has 6 sides, but if it is surrounded by cubes it has 0 outside surface.
    as it is one big obsidian cube some side(s) should always connect and those are the inside surface.
    keeping track of outside and inside surface areas is a good idea.
    """

    def __init__(self, source) -> None:
        self.outside = set()
        self.inside = set()
        self.cubes = self.parse(source)

    @staticmethod
    def parse(source) -> set[tuple[int, int, int]]:
        coordinates = set()
        for line in source:
            x, y, z = ints(line)
            coordinates.add((x, y, z))
        return coordinates

    @staticmethod
    def sides(x, y, z):
        return {
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1)
        }

    def has_outside(self, cube, flood_size=1500, optimize=True):
        """this one is for part 2 of the puzzle.
        - it is a flood fill algorithm.
        - it is a breadth first search algorithm.
        - added a bit of memoization to speed it up a lot I solved it without the "optimize" though.
        - note that the flood_size is a bit of a hack to prevent infinite loops.
        - I had to find this out by trial and error (took me 3 tries to get it big enough)
        - the assumption is that a flood fill on the outside can continue indefinitely,
          but on the inside it will be finite.
        - in the end I just made it a very large number.
        - I had time to tune it a bit more and 1500 proved to be enough for my input.
        - I think I can adopt this algorithm to solve it for both parts of the puzzle,
          but I don't wanna :-)
        """
        if optimize:
            if cube in self.outside:
                return True
            if cube in self.inside:
                return False
        explored = set()
        frontier = Queue()
        frontier.push(cube)
        while not frontier.empty:
            cube = frontier.pop()
            if cube in explored or cube in self.cubes:
                continue
            explored.add(cube)
            if len(explored) > flood_size:
                for cube in explored:
                    self.outside.add(cube)
                return True
            for successor in self.sides(*cube):
                if successor not in explored:
                    frontier.push(successor)
        if optimize:
            # hmm all 3 below work but the last one is the most efficient, why is that?
            # self.inside = self.inside & explored
            # self.inside.union(explored)
            for cube in explored:
                self.inside.add(cube)
        return False

    def outside_surface_area(self):
        """gives the answer to part 1 of the puzzle:
        just iterate over all cubes get all its sides (6) and check if they are already in the cube list.
        """
        surface_area = 0
        for cube in self.cubes:
            for side in self.sides(*cube):
                if side not in self.cubes:
                    surface_area += 1
        return surface_area

    def calc_outside_surface_area(self, optimize=True):
        surface_area = 0
        for cube in self.cubes:
            for side in self.sides(*cube):
                if self.has_outside(side, optimize=optimize):
                    surface_area += 1
        return surface_area


def part_1(source):
    return Obsidian(source).outside_surface_area()


def part_2(source):
    return Obsidian(source).calc_outside_surface_area(optimize=True)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""")

    def test_example_data_part_1(self):
        self.assertEqual(64, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(3374, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(58, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2010, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
