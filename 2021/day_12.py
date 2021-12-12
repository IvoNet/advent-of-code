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


class Graph:
    def __init__(self, vertices):
        # No. of vertices
        self.V = vertices

        # default dictionary to store graph
        self.graph = defaultdict(list)

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    def printAllPathsUtil(self, u, d, visited, path):
        """A recursive function to print all paths from 'u' to 'd'.
         visited[] keeps track of vertices in current path.
         path[] stores actual vertices and path_index is current
         index in path[]"""

        # Mark the current node as visited and store in path
        visited[u] = True
        path.append(u)

        # If current vertex is same as destination, then print
        # current path[]
        if u == d:
            print
            path
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.graph[u]:
                if visited[i] == False:
                    self.printAllPathsUtil(i, d, visited, path)

        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u] = False

    # Prints all paths from 's' to 'd'
    def printAllPaths(self, s, d):

        # Mark all the vertices as not visited
        visited = [False] * (self.V)

        # Create an array to store paths
        path = []

        # Call the recursive helper function to print all paths
        self.printAllPathsUtil(s, d, visited, path)


class Node:

    def __init__(self, name: str) -> None:
        self.small = True
        if name != name.lower():
            self.small = False
        self.name = name
        self.visited = 0
        self.visitable = 1

    def __str__(self) -> str:
        return repr(self.name)

    def __repr__(self) -> str:
        return repr(self.name)

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, o: object) -> bool:
        return repr(self) == repr(o)


class Route:

    def __init__(self) -> None:
        self.nodes = defaultdict(list)
        self.small = []

    def add(self, s: str):
        a, b = s.split("-")
        aa = Node(a)
        bb = Node(b)
        self.nodes[aa].append(bb)
        self.nodes[bb].append(aa)
        if aa.small:
            self.small.append(aa)
        if bb.small:
            self.small.append(bb)

    def find_all_paths(self, start=Node("start"), end=Node("end"), visited=[], path=[]):
        path = path + [start]
        if start.small:
            visited = visited + [start]
        if start == end:
            return [path]
        if start not in self.nodes:
            return []
        paths = []
        for node in self.nodes[start]:
            if node not in visited:
                newpaths = self.find_all_paths(node, end, visited, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_all_paths_with_one_small_twice(self, start=Node("start"), end=Node("end"), visited=[], path=[]):
        paths = []
        for node in self.small:
            node.visitable = 2
            new_paths = self.find_all_paths(node, end)

    def __str__(self) -> str:
        return repr(self.nodes)

    def __repr__(self) -> str:
        return repr(self.nodes)


def part_1(source):
    routes = Route()
    for x in source:
        routes.add(x)
    a = routes.find_all_paths()
    print(a)
    return len(a)


def part_2(source):
    pass


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

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
