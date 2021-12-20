#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
--- Day 9: Smoke Basin ---
These caves seem to be lava tubes. Parts are even still volcanically active; 
small hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid 
it and be that much safer. The submarine generates a heightmap of the floor of 
the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the 
following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678

Each number corresponds to the height of a particular location, where 9 is 
the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than 
any of its adjacent locations. Most locations have four adjacent locations 
(up, down, left, and right); locations on the edge or corner of the map have three 
or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in 
the first row (a 1 and a 0), one is in the third row (a 5), and one is in the 
bottom row (also a 5). All other locations on the heightmap have some lower 
adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, 
the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk 
levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk 
levels of all low points on your heightmap?


--- Part Two ---
Next, you need to find the largest basins so you know what areas are most 
important to avoid.

A basin is all locations that eventually flow downward to a single low point. 
Therefore, every low point has a basin, although some basins are very small. 
Locations of height 9 do not count as being in any basin, and all other locations 
will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including 
the low point. The example above has four basins.

(Ivo: replaced all 9s with X for visibility here for real they are still 9)

The top-left basin, size 3:

21XXX43210
3X878X4X21
X85678X8X2
87678X678X
X8XXX65678

The top-right basin, size 9:

21XXX43210
3X878X4X21
X85678X8X2
87678X678X
X8XXX65678

The middle basin, size 14:

21XXX43210
3X878X4X21
X85678X8X2
87678X678X
X8XXX65678

The bottom-right basin, size 9:

21XXX43210
3X878X4X21
X85678X8X2
87678X678X
X8XXX65678

Find the three largest basins and multiply their sizes together. 
In the above example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?
"""

import sys
import unittest

from ivonet.calc import prod
from ivonet.files import read_int_matrix
from ivonet.grid import neighbors, neighbor_values

BOUNDARY = 9

BOUNDARY = 9

sys.dont_write_bytecode = True


def part_1(matrix):
    som = 0
    smallest_points = []
    for h, row in enumerate(matrix):
        for w, x in enumerate(row):
            nb = neighbors(matrix, (h, w), diagonal=False)
            smallest = True
            for a, b in nb:
                if matrix[a][b] <= x:
                    smallest = False
            if smallest:
                som += 1 + x
                smallest_points.append((h, w))
    return som, smallest_points


def part_1a(matrix):
    points = 0
    smallest_points = []
    for h in range(len(matrix)):
        for w in range(len(matrix[0])):
            me = matrix[h][w]
            nb = neighbor_values(matrix, (h, w), diagonal=False)
            if me < min(nb):
                points += 1 + me
                smallest_points.append((h, w))
    return points, smallest_points


def part_2(matrix):
    cache = []
    smallest_points = part_1a(matrix)[1]
    for coord in smallest_points:
        queue = neighbors(matrix, coord, diagonal=False)
        basin = [coord, ]
        running = True
        while running:
            try:
                h, w = queue.pop()
                if matrix[h][w] != BOUNDARY and (h, w) not in basin:
                    basin.append((h, w))
                    nb2 = neighbors(matrix, (h, w), diagonal=False)
                    [queue.append(n) for n in nb2 if n not in queue and n not in basin]
            except IndexError:
                running = False
            if basin not in cache:
                cache.append(basin)
    return prod(len(x) for x in sorted(cache, key=len, reverse=True)[0:3])


class UnitTests(unittest.TestCase):
    source = read_int_matrix("day_9.input")
    test_source = read_int_matrix("""2199943210
3987894921
9856789892
8767896789
9899965678""")

    def test_example_data_part_1(self):
        self.assertEqual(15, part_1(self.test_source)[0])

    def test_example_data_part_2(self):
        self.assertEqual(1134, part_2(self.test_source))

    def test_part_1(self):
        self.assertEqual(500, part_1(self.source)[0])

    def test_part_1a(self):
        self.assertEqual(500, part_1a(self.source)[0])

    def test_part_1a2(self):
        self.assertEqual(part_1(self.source)[1], part_1a(self.source)[1])

    def test_part_2(self):
        self.assertEqual(970200, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
