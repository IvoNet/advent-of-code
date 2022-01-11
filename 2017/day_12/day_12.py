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
from pathlib import Path
from typing import Callable, TypeVar, Set

from ivonet.collection import Queue
from ivonet.files import read_rows
from ivonet.graph import Graph
from ivonet.iter import ints
from ivonet.search import Node

sys.dont_write_bytecode = True

DEBUG = True
V = TypeVar('V')  # type of the vertices in the graph
T = TypeVar('T')  # type of the vertices in the graph


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def process(source):
    groups = {}
    ids = []
    vertices = set()
    for line in source:
        nrs = ints(line)
        groups[nrs[0]] = nrs[1:]
        ids.append(nrs)
        next(vertices.add(x) for x in nrs)
        vertices = vertices.union(nrs)

    return groups, ids, list(vertices)


def bfs(initial: T, successors: Callable[[T], list[T]]) -> set[T]:
    """Breath first search
    for finding the longest route from an initial
    """
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    explored: Set[T] = {initial}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # Goal test here if you need it but we want to explore the whole thing
        for child in successors(current_state):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return explored


def part_1(source):
    group, ids, vertices = process(source)
    graph: Graph[int] = Graph(vertices)
    for node, neigbors in group.items():
        for n in neigbors:
            graph.add_edge_by_vertices(node, n)

    return len(bfs(0, graph.neighbors_for_vertex))


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5""")

    def test_example_data_part_1(self):
        self.assertEqual(None, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(380, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
