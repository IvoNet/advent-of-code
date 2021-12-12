#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import sys
import unittest
from collections import defaultdict

from ivonet.files import read_rows

sys.dont_write_bytecode = True


def prepare(source):
    graph = Graph()
    for x in source:
        graph.add(x)
    return graph


class Graph:

    def __init__(self) -> None:
        self.nodes = defaultdict(list)
        self.small_nodes = set()

    def add_small(self, node: str):
        if node == node.lower() and node not in ["start", "end"]:
            self.small_nodes.add(node)

    def add(self, s: str):
        a, b = s.split("-")
        self.nodes[a].append(b)
        self.nodes[b].append(a)
        self.add_small(a)
        self.add_small(b)

    def find_all_paths(self, start="start", visited=[], path=[], small_twice=None):
        path = path + [start]
        if small_twice == start:
            small_twice = None
        else:
            if start == start.lower():
                visited = visited + [start]
        if start == "end":
            return [path]
        paths = []
        for node in self.nodes[start]:
            if node not in visited:
                newpaths = self.find_all_paths(node, visited, path, small_twice)
                for newpath in newpaths:
                    np = str(newpath)
                    paths.append(np)
        return paths

    def find_all_paths_with_one_small_twice(self):
        paths = []
        for node in self.small_nodes:
            newpaths = self.find_all_paths(small_twice=node)
            for newpath in newpaths:
                if newpath not in paths:
                    paths.append(newpath)

        return paths

    def __str__(self) -> str:
        return repr(self.nodes)

    def __repr__(self) -> str:
        return repr(self.nodes)


def part_1(source):
    graph = prepare(source)
    return len(graph.find_all_paths())


def part_2(source):
    graph = prepare(source)
    return len(graph.find_all_paths_with_one_small_twice())


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        self.source = read_rows("day_12.txt")
        self.test_source_smallest = read_rows("""start-A
start-b
A-c
A-b
b-d
A-end
b-end""")
        self.test_source_bigger = read_rows("""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""")
        self.test_source = read_rows("""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""")

    def test_example_data_part_1_smallest(self):
        self.assertEqual(10, part_1(self.test_source_smallest))

    def test_example_data_part_1_biggerl(self):
        self.assertEqual(19, part_1(self.test_source_bigger))

    def test_example_data_part_1(self):
        self.assertEqual(226, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(3410, part_1(self.source))

    def test_example_data_part_2_smallest(self):
        self.assertEqual(36, part_2(self.test_source_smallest))

    def test_example_data_part_2_bigger(self):
        self.assertEqual(103, part_2(self.test_source_bigger))

    def test_example_data_part_2(self):
        self.assertEqual(3509, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(98796, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
