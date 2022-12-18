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
import re
import sys
import unittest
from pathlib import Path

from ivonet import infinite
from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Tunnelator:

    def __init__(self, source) -> None:
        self.source = source
        self.lines = [re.split('[\\s=;,]+', line) for line in self.source]
        self.groups = self.__define_groups()
        self.high_pressure_valves = self.__extract_high_pressure_valves()
        self.cost = self.__calc_cost()
        self.floyd_warhall = self.__floyd_warhall()

    def __define_groups(self) -> dict[str, list[str]]:
        """Define the groups of nodes that are connected to each other."""
        groups = {}
        for line in self.lines:
            name = line[1]
            neighbours = line[10:]
            groups[name] = neighbours
        return groups

    def __calc_cost(self) -> dict[str, int]:
        """Took me ages to come up with a working cost function."""
        cost = {}
        for i, node in enumerate(self.high_pressure_valves):
            cost[node] = 2 ** i
        return cost

    def __extract_high_pressure_valves(self) -> dict[str, int]:
        """Extract the high pressure valves from the input."""
        hpv = {}
        for line in self.lines:
            node = line[1]
            rate = int(line[5])
            if rate > 0:
                hpv[node] = rate
        return hpv

    def __floyd_warhall(self) -> dict[str, dict[str, int]]:
        """https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
        https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/
        Found the hint for this algorithm on reddit. Not sure If I had figured it out otherwise.
        Once you know the algorithm, though it is not that hard to implement "ahum" took me ages.
        to initialize the matrix I need to:
        - create a matrix initialized with either 1 or infinite
        - if a node exists in a group (neighbors) then set the distance to 1
        - else set the distance to infinite
        - then do the triple loop from the algorithm
        the result is a matrix with the shortest distances between all nodes.
        """
        floyd_warhall = {}
        for x in self.groups:
            floyd_warhall[x] = {}
            for y in self.groups:
                if y in self.groups[x]:
                    floyd_warhall[x][y] = 1
                else:
                    floyd_warhall[x][y] = infinite
        for k in floyd_warhall:
            for i in floyd_warhall:
                for j in floyd_warhall:
                    floyd_warhall[i][j] = min(floyd_warhall[i][j], floyd_warhall[i][k] + floyd_warhall[k][j])
        return floyd_warhall

    def traverse(self, start: str, states: dict, time: int = 30, state: int = 0, pressure_released: int = 0) -> \
            dict[int, int]:
        """Traverse all the high pressure valves and calculate the pressure release for all of them
        within the given time frame.
        """
        states[state] = max(states.get(state, 0), pressure_released)
        for valve in self.high_pressure_valves:
            # _(valve, states)
            time_left = time - self.floyd_warhall[start][valve] - 1
            if time_left <= 0:
                continue
            if self.cost[valve] & state:
                continue
            self.traverse(valve,
                          states,
                          time_left,
                          state | self.cost[valve],
                          pressure_released + time_left * self.high_pressure_valves[valve])
        return states

    def find_highest_pressure_release(self, start: str = 'AA', time: int = 30) -> int:
        explored = self.traverse(start, {}, time=time)
        # _(explored)
        return max(explored.values())

    def find_highest_pressure_release2(self, start: str = 'AA', time: int = 26) -> int:
        explored = self.traverse(start, {}, time=time)
        value = 0
        for key1, value1 in explored.items():
            for key2, value2 in explored.items():
                if not key1 & key2:  # no overlap
                    if value >= value1 + value2:  # no improvement
                        continue
                    value = value1 + value2
        return value


def part_1(source, time=30):
    return Tunnelator(source).find_highest_pressure_release(time=time)


def part_2(source):
    return Tunnelator(source).find_highest_pressure_release2()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""")

    def test_example_data_part_1(self):
        self.assertEqual(1651, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(2320, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(1707, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2967, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
