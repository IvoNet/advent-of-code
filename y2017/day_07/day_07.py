#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

Try this one in a terminal :-)

grep -o -E '[a-z]+' day_07.input | sort | uniq -c | sort -n | head -1 | awk '{print $2}'

"""

import os
import sys
import unittest
from collections import Counter
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    data = source.replace("(", "").replace(")", "").replace(",", "").replace("-> ", "")
    data = data.splitlines(keepends=False)
    weights = {}
    children = {}
    for line in data:
        node, weight, *kids = line.split()
        weights[node] = int(weight)
        children[node] = kids

    return weights, children


def find_root(children):
    """All the keys minus the children"""
    return (set(children) - {kid for kids in children.values() for kid in kids}).pop()


def find_weight(weights, children, node):
    """Recursively add the weight of the node to the weight its children"""
    return weights[node] + sum([find_weight(weights, children, kid) for kid in children[node]])


def find_and_correct_unbalanced_weight(weights, children, node):
    """Find the imbalance recursively at the deepest level
    Rulez:
    - if there are no children there is nothing to do
    - if all the children have the same total weight there is no imbalance
    - if there is an imbalance then all the children except 1 has a different total weight
    - if the imbalance is found we need to see if we can go deeper into the imbalanced child
      to see if the imbalance lies deeper. (took me forever to find this one)
    """
    kids = children[node]
    if not kids:  # Nothing to do here
        return
    child_weights = [find_weight(weights, children, child) for child in kids]
    weight_counts = Counter(child_weights)
    if len(weight_counts) <= 1:
        return
    (good_weight, _), (unbalanced_weight, _) = weight_counts.most_common()
    imbalanced_child_node = kids[child_weights.index(unbalanced_weight)]
    deeper_imbalance = find_and_correct_unbalanced_weight(weights, children, imbalanced_child_node)
    if deeper_imbalance:
        return deeper_imbalance
    else:
        imbalance = unbalanced_weight - good_weight
        return weights[imbalanced_child_node] - imbalance


def part_1(source):
    weights, children = parse(source)
    return find_root(children)


def part_2(source):
    weights, children = parse(source)
    return find_and_correct_unbalanced_weight(weights, children, find_root(children))


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)""")

    def test_example_data_part_1(self):
        self.assertEqual("tknk", part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual("fbgguv", part_1(self.source))

    def test_part_2(self):
        self.assertEqual(1864, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
