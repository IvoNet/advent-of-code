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
from pprint import pprint

from ivonet.files import read_rows

sys.dont_write_bytecode = True


class Node:

    def __init__(self, name: str) -> None:
        self.small = True
        if name != name.lower():
            self.small = False
        self.name = name
        self.visited = 0
        self.visitable = 1

    def is_visitable(self):
        if not self.small:
            return True
        if self.small and self.visited <= self.visitable:
            return True
        return False

    def visit(self):
        self.visited += 1

    def reset(self):
        self.visited = 0

    def __str__(self) -> str:
        return f"{self.name} - {self.visitable} - {self.visited}"

    def __repr__(self) -> str:
        return repr(self.name)

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, o: object) -> bool:
        return repr(self) == repr(o)


class Route:

    def __init__(self) -> None:
        self.nodes = defaultdict(list)
        self.small_nodes = set()
        self.all_nodes = {}

    def add_small(self, node):
        if node.small and node.name not in ["start", "end"]:
            self.small_nodes.add(node.name)

    def add(self, s: str):
        a, b = s.split("-")
        aa = Node(a)
        bb = Node(b)
        self.all_nodes[a] = aa
        self.all_nodes[b] = bb
        self.nodes[a].append(b)
        self.nodes[b].append(a)
        self.add_small(aa)
        self.add_small(bb)

    def find_all_paths(self, start="start", visited=[], path=[], small_twice=None):
        path = path + [start]
        if small_twice == start:
            small_twice = None
        else:
            if self.all_nodes[start].small:
                visited = visited + [start]
        if start == "end":
            return [path]
        paths = []
        for node in self.nodes[start]:
            if node not in visited:
                self.all_nodes[start].visit()
                newpaths = self.find_all_paths(node, visited, path, small_twice)
                for newpath in newpaths:
                    paths.append(str(newpath))
        return paths

    def find_all_paths_with_one_small_twice(self):
        paths = []
        for node in self.small_nodes:
            # self.reset_nodes()
            self.all_nodes[node].visitable = 2
            newpaths = self.find_all_paths(small_twice=node)
            for x in self.all_nodes:
                print(
                    f"Node [{x}] visited [{self.all_nodes[x].visited}] visitable [{self.all_nodes[x].is_visitable()}].")

            pprint(newpaths)
            print("-" * 80)
            for newpath in newpaths:
                if newpath not in paths:
                    paths.append(newpath)

        return paths

    def reset_nodes(self):
        for x in self.small_nodes:
            self.all_nodes[x].visitable = 1
            self.all_nodes[x].visited = 0

    def __str__(self) -> str:
        return repr(self.nodes)

    def __repr__(self) -> str:
        return repr(self.nodes)


def part_1(source):
    routes = prepare(source)
    a = routes.find_all_paths()
    pprint(set(a))
    return len(set(a))


def prepare(source):
    routes = Route()
    for x in source:
        routes.add(x)
    return routes


def part_2(source):
    routes = prepare(source)
    a = routes.find_all_paths_with_one_small_twice()
    print("Small nodes:", routes.small_nodes)
    pprint(routes.nodes)
    # for x in routes.all_nodes:
    #     print(f"Node [{x}] visited [{routes.all_nodes[x].visited}] visitable [{routes.all_nodes[x].is_visitable()}].")
    # pprint(sorted(a))
    pprint(a)
    return len(a)


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

    def test_example_data_part_2(self):
        self.assertEqual(36, part_2(self.test_source_smallest))

    def test_example_data_part_2_bigger(self):
        self.assertEqual(103, part_2(self.test_source_bigger))

    def test_part_2(self):
        self.assertEqual(98796, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
