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
import os
import sys
import unittest
from pathlib import Path

import networkx as nx
import pyperclip
from matplotlib import pyplot as plt
from networkx import Graph, minimum_edge_cut, connected_components

from ivonet.calc import prod
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def part_1(source) -> int | None:
    """
    Sry didn't feel like doing this one in pure python.
    I will though at a later time I think if I have time left.
    https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.flow.minimum_cut.html
    """
    graph = Graph()

    for line in source:
        node, connections = line.split(": ")
        for connection in connections.split(" "):
            graph.add_edge(node, connection)

    nx.draw(graph, with_labels=True)
    plt.show()

    graph.remove_edges_from(minimum_edge_cut(graph))

    answer = prod(len(c) for c in connected_components(graph))
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(54, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(571753, part_1(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
