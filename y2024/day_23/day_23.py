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

import collections
import unittest
from collections import abc
from pathlib import Path

import pyperclip
import sys

from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.graph import Graph
from ivonet.iter import ints

collections.Callable = abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class LanParty:

    def __init__(self, source):
        self.source = source
        self.graph = Graph()
        self.search_results = set()
        self.longest_set = set()
        self.parse(self.source)

    def parse(self, source):
        edges = [line.strip().split("-") for line in source]
        vertices = set()
        for left, right in edges:
            vertices.add(left)
            vertices.add(right)
        for vertex in vertices:
            self.graph.add_vertex(vertex)
        for left, right in edges:
            self.graph.add_edge_by_vertices(left, right)

    @property
    def sets_of_three(self) -> set:
        ret = set()
        for x in self.graph.vertices:
            for y in self.graph.neighbors_for_vertex(x):
                for z in self.graph.neighbors_for_vertex(y):
                    if x != z and x in self.graph.neighbors_for_vertex(z):
                        ret.add(tuple(sorted([x, y, z])))
        return ret

    def search(self, node: str, req: set) -> None:
        stack = [(node, req)]
        while stack:
            current_node, current_req = stack.pop()
            key = tuple(sorted(current_req))
            if key in self.search_results:
                continue
            self.search_results.add(key)
            if len(current_req) > len(self.longest_set):
                self.longest_set = current_req
            for neighbor in self.graph.neighbors_for_vertex(current_node):
                if neighbor in current_req:
                    continue
                if not set(current_req).issubset(self.graph.neighbors_for_vertex(neighbor)):
                    continue
                stack.append((neighbor, {*current_req, neighbor}))
        self.longest_set = sorted(self.longest_set)

    def part_1(self):
        return len([s for s in self.sets_of_three if any(connection.startswith("t") for connection in s)])

    def part_2(self):
        for node in self.graph._vertices:
            self.search(node, {node})
        return ",".join(self.longest_set)


@debug
@timer
def part_1(source) -> int | None:
    lp = LanParty(source)
    answer = lp.part_1()

    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> str | None:
    lp = LanParty(source)
    answer = lp.part_2()
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(7, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(1227, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual("co,de,ka,ta", part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual("cl,df,ft,ir,iy,ny,qp,rb,sh,sl,sw,wm,wy", part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
