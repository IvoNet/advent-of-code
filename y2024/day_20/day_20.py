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

import heapq
import unittest
from collections import defaultdict
from pathlib import Path

import pyperclip
import sys
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints
from ivonet.search import DIRECTIONS

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class CheatingRace:
    """Class to represent a race where cheating is allowed to a certain extent."""

    def __init__(self, source, save=100, exact=False):
        """Initialize the race with the given source and save parameter."""
        self.exact = exact
        self.save = save
        self.grid, self.start, self.end = self.parse(source)
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.distances_from_start = self.distances(self.start)
        self.distances_from_end = self.distances(self.end)
        self.optimal_distance = self.distances_from_start[self.end]

    @staticmethod
    def manhatten_distance(left, right) -> int:
        """Calculate the Manhattan distance between two points."""
        return abs(left[0] - right[0]) + abs(left[1] - right[1])

    @staticmethod
    def parse(source):
        """Parse the source to extract the grid, start, and end points."""
        grid = []
        start = None
        end = None
        for r, line in enumerate(source):
            grid.append(list(line))
            if "S" in line:
                start = (r, line.index("S"))
            if "E" in line:
                end = (r, line.index("E"))
        return grid, start, end

    def adjacent(self, loc):
        """Generate adjacent points for a given loc."""
        r, c = loc
        for dr, dc in DIRECTIONS:
            rr, cc = r + dr, c + dc
            if 0 <= rr < self.height and 0 <= cc < self.width and self.grid[rr][cc] in [".", "S", "E"]:
                yield 1, (rr, cc)

    def distances(self, start):
        """
        Calculate the shortest distances from the start point to all other points.

        Uses a Dijkstra-like algorithm with a priority queue to compute the shortest path distances
        from the start point to all reachable points in the grid.
        """
        queue = [(0, start)]
        dists = defaultdict(lambda: float("inf"))
        dists[start] = 0
        while queue:
            dist, current = heapq.heappop(queue)
            if dist > dists[current]:
                continue
            for d, adj in self.adjacent(current):
                new_dist = dist + d
                if new_dist < dists[adj]:
                    dists[adj] = new_dist
                    heapq.heappush(queue, (new_dist, adj))
        return dists

    def solve(self, max_cheats):
        """
        Solve the race problem with a given number of allowed cheats.

        This method calculates the number of valid paths from the start to the end point
        considering the allowed number of cheats. A cheat allows bypassing obstacles
        within a certain Manhattan distance.
        """
        answer = 0
        distances_from_start = self.distances_from_start
        distances_from_end = self.distances_from_end
        optimal_distance = self.optimal_distance - self.save

        for (rs, cs), dist_start in distances_from_start.items():
            for (re, ce), dist_end in distances_from_end.items():
                cheats_needed = self.manhatten_distance((rs, cs), (re, ce))
                if cheats_needed <= max_cheats:
                    total_distance = dist_start + cheats_needed + dist_end
                    if self.exact:  # exact solution
                        if total_distance == optimal_distance:
                            answer += 1
                    else:  # solution with less or equal to max_cheats
                        if total_distance <= optimal_distance:
                            answer += 1
        return answer


# @debug
@timer
def part_0(source):
    """
    Just a test function to see if the CheatingRace class works as expected.
    Should reproduce the example output from the problem statement.
    """
    for i in range(2, 66):
        race = CheatingRace(source, i, True)
        answer = race.solve(2)
        if answer > 0:
            print("There are %s cheats that save %s picoseconds" % ("one" if answer == 1 else answer, i))
    print(80 * "-")
    for i in range(50, 77):
        race = CheatingRace(source, i, True)
        answer = race.solve(20)
        if answer > 0:
            print("There are %s cheats that save %s picoseconds" % ("one" if answer == 1 else answer, i))
    return None


# @debug
@timer
def part_1(source) -> int | None:
    """So what to do here
    I think the cheat just means that for that specific span of time we can walk through walls or anything really as
    long as we end up on the normal path again.
    so 2 means that we can break down 1 wall but looking ahead we need to be able to walk through more walls
    I think so what would be a generic solution.
    What if I first calculate all distances from the start and from the end and then we can calculate stuff from there.
    Yup works but not really fast... Fast enough though

    First try was to brute force remove 1 wall and see of the new shortest path is more than 100 less than before.
    That worked for part 1 but not for part 2.
    Now the solution I found works for both parts.
    """
    race = CheatingRace(source)
    answer = race.solve(2)
    pyperclip.copy(str(answer))
    return answer


# @debug
@timer
def part_2(source) -> int | None:
    race = CheatingRace(source)
    answer = race.solve(20)
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(None, part_0(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(1441, part_1(self.source))

    def test_part_2(self) -> None:
        self.assertEqual(1021490, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
