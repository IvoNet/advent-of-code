#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
TODO Tried to do with my own graph module what networkx can do but failed for now

from the ivonet.graph.Graph module (non functioning)


    def single_shortest_path(self, initial: V) -> dict:
        "Compute the shortest path lengths from source to all reachable nodes."
        nextlevel = [initial]
        return dict(self._single_shortest_path_length(nextlevel))

    def _single_shortest_path_length(self, firstlevel):
        seen = {}  # level (number of hops) when seen in BFS
        level = 0  # the current level
        nextlevel = set(firstlevel)  # set of nodes to check at next level
        n = len(self.neighbors_for_vertex(firstlevel[0]))
        while nextlevel:
            thislevel = nextlevel  # advance to next level
            nextlevel = set()  # and start a new set (fringe)
            found = []
            for v in thislevel:
                if v not in seen:
                    seen[v] = level  # set the level of vertex v
                    found.append(v)
                    yield (v, level)
            if len(seen) == n:
                return
            for v in found:
                nextlevel.update(self.neighbors_for_vertex(v))
            level += 1
        del seen


"""

import os
import sys
import unittest
from pathlib import Path

from ivonet.files import read_data
from ivonet.graph import Graph
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


DIRECTIONS = {'N': 1j, 'S': -1j, 'E': 1, 'W': -1}


class ARegularMap:

    def __init__(self, source, start=0) -> None:
        self.source = list(source)
        self.graph = Graph()
        self.room_stack = []
        self.end_stack = []
        self.done = set()
        self.start = start

    def process(self, current: int, data: list[str]):
        if len(data) in self.done:
            return
        self.done.add(len(data))
        while data:
            step = data.pop(0)
            if step in "NSEW":
                self.graph.add_vertex(current)
                nxt = current + DIRECTIONS[step]
                self.graph.add_vertex(nxt)
                self.graph.add_edge_by_vertices(current, nxt)
                current = nxt
            elif step == "(":
                self.room_stack.append(current)
                self.end_stack.append([])
            elif step in "|)":
                self.end_stack[-1].append(current)
                if step == ")":
                    self.room_stack.pop()
                    ends = self.end_stack.pop()
                    for end in set(ends):
                        self.process(end, list(data))
                    return

    def map(self):
        self.process(self.start, self.source)

    def __repr__(self) -> str:
        return str(self.graph)


def part_1(source):
    a_regular_map = ARegularMap(source)
    a_regular_map.map()
    # _(a_regular_map)
    cp = a_regular_map.graph.connected_components(0)
    _(cp)
    _(len(cp))
    cg = a_regular_map.graph.connected_groups()
    _(cg)
    _(len(cg))
    sl = a_regular_map.graph.single_shortest_path(0)
    _(sl)
    _(len(sl))
    _(a_regular_map.graph.connected_components(0))
    return None


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""""")

    def test_example_data_part_1(self):
        self.assertEqual(None, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
