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
from copy import deepcopy
from pathlib import Path
from typing import Callable, TypeVar, Set

from ivonet.collection import Queue
from ivonet.files import read_rows
from ivonet.graph import Graph
from ivonet.iter import ints
from ivonet.search import Node

sys.dont_write_bytecode = True
T = TypeVar('T')

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    """Parse the source
    As this is a Graph related problem it is easy to prepare the code
    in such a way that it returns a dict with group/neighbors and a
    set of all id's (vertices)
    makes creating the Graph easier
    """
    groups = {}
    vertices = set()
    for line in source:
        nrs = ints(line)
        groups[nrs[0]] = nrs[1:]
        next(vertices.add(x) for x in nrs)
        vertices = vertices.union(nrs)
    return groups, list(vertices)


def build_graph(groups, vertices) -> Graph[int]:
    """Builds a graph"""
    graph: Graph[int] = Graph(vertices)
    for node, neighbors in groups.items():
        for edge in neighbors:
            graph.add_edge_by_vertices(node, edge)
    return graph


def bfs(initial: T, successors: Callable[[T], list[T]]) -> set[T]:
    """Breath first search
    This one is adjusted so that it does not have a 'goal' per se except
    for exploring all the connections to 'initial'.
    """
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    explored: Set[T] = {initial}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # removed goal test here
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    # we explored as much as we could so this should be the whole set connected to 'initial'
    return explored


def part_1(source):
    groups, vertices = parse(source)
    graph: Graph[int] = build_graph(groups, vertices)
    return len(bfs(0, graph.neighbors_for_vertex))


def part_2(source):
    groups, vertices = parse(source)
    _(groups, vertices)
    graph: Graph[int] = build_graph(groups, vertices)
    todo = deepcopy(vertices)
    total_groups = 0
    start = 0
    while todo:
        explored = bfs(start, graph.neighbors_for_vertex)
        total_groups += 1
        todo = [x for x in todo if x not in explored]
        start = todo.pop()
        _(todo)

    return total_groups + 1  # last item is not counted anymore (pop)


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
        self.assertEqual(6, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(380, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(2, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(181, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
