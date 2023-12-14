#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Look back at the history of this file in git to see the first implementations.

I liked my solution a lot because I actually used what I had just refreshed from 
'Classic Computer Science Problems' that I added my adjustments to the Graph code

Later I found out that you can do this just as easily with the networkx component
but my goal with these solutions is to use as much standard library and plain Python.

It is for my understanding and fun :-)
"""

import os
import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.graph import Graph
from ivonet.iter import ints

sys.dont_write_bytecode = True

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
        vertices = vertices.union(nrs)
    return groups, list(vertices)


def build_graph(source) -> Graph[int]:
    """Builds a graph
    - First initialise with the set of unique ids.
    - then add edges to the graph based on the key values from the groups dict
    """
    groups, vertices = parse(source)
    graph: Graph[int] = Graph(vertices)
    for node, neighbors in groups.items():
        for edge in neighbors:
            graph.add_edge_by_vertices(node, edge)
    return graph


def part_1(source):
    graph: Graph[int] = build_graph(source)
    return len(graph.connected_components(0))


def part_2(source):
    graph: Graph[int] = build_graph(source)
    return len(graph.connected_groups())


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
