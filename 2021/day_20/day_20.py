#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from collections import defaultdict, OrderedDict
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Coord(NamedTuple):
    r: int
    c: int


def parse(source) -> [dict[int, bool], dict[Coord, bool]]:
    key: [int, bool] = {}
    value: [Coord, bool] = {}

    # key
    for i, c in enumerate(source[0]):
        key[i] = c == "#"

    # grid
    for r, line in enumerate(source[2:]):
        for c, v in enumerate(line):
            value[Coord(r, c)] = v == "#"

    return key, value


def enhance(grid: dict[Coord], key: dict[int], iteration: int, orig_size=100):
    ret = defaultdict(bool)
    default_fill = False

    # Flip the fill on empty space!
    # if first char of the enhancement table is "on"
    # in infinite space that will flip the whole empty stuff on
    if key[0] and not key[511]:
        default_fill = iteration % 2 == 0

    min_pos = -2 * iteration
    max_pos = orig_size + 2 * iteration
    for r in range(min_pos, max_pos):
        for c in range(min_pos, max_pos):
            binary = ""
            for row_offset in range(-1, 2):
                for col_offset in range(-1, 2):
                    crd = Coord(r + row_offset, c + col_offset)
                    if crd in grid and grid[crd]:
                        binary += "1"
                    elif crd not in grid and default_fill:
                        binary += "1"
                    else:
                        binary += "0"
            ret[Coord(r, c)] = key[int(binary, base=2)]
    return ret


def count(grid) -> int:
    return sum(1 for x in grid if grid[x])


def visualize(grid):
    g = OrderedDict(sorted(grid.items()))
    print()
    print("-" * 100)
    row = -1000  # smaller than smallest
    for crd in g:
        if crd.y > row:
            row = crd.y
            print()
        print("#" if g[crd] else ".", end="")
    print()


def main(source):
    key, grid = parse(source)
    orig_size = len(source[2])

    grid_part_1 = None
    for i in range(1, 51):
        grid = enhance(grid, key, i, orig_size=orig_size)
        if DEBUG:
            visualize(grid)
        if i == 2:
            grid_part_1 = grid

    return count(grid_part_1), count(grid)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source = read_rows("""..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###""")

    def test_example_data(self):
        part_1, part_2 = main(self.test_source)
        self.assertEqual(35, part_1)
        self.assertEqual(3351, main(self.test_source)[1])

    def test_real_data(self):
        part_1, part_2 = main(self.source)
        self.assertEqual(5218, part_1)
        self.assertEqual(15527, part_2)


if __name__ == '__main__':
    unittest.main()
