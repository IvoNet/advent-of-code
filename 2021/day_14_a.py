#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
See other solution
"""

import sys
import unittest
from collections import Counter
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints, words

sys.dont_write_bytecode = True


class Polymer:

    def __init__(self, source) -> None:
        self.template = source[0]
        self.inserts = dict([words(x) for x in source[2:] if x])
        self.cache = {}
        self.occurrences = Counter()

    def insert(self, pair, step, stop):
        try:
            return self.cache[(pair, step)]
        except KeyError:
            if step < stop:
                left, right = self.leaves(pair)
                left_letter = self.insert(left, step + 1, stop)
                right_letter = self.insert(right, step + 1, stop)
                self.cache[(pair, step)] = left_letter + right_letter
                return left_letter + right_letter
            else:
                self.cache[(pair, step)] = Counter(pair[0])
                return Counter(pair[0])

    def leaves(self, pair):
        left = pair[0] + self.inserts[pair]
        right = self.inserts[pair] + pair[1]
        return left, right

    def go(self, stop):
        self.occurrences = Counter(self.template[-1])
        for i in range(len(self.template) - 1):
            self.occurrences = self.occurrences + self.insert(self.template[i:i + 2], 0, stop)
        return max(self.occurrences.values()) - min(self.occurrences.values())


def part_1(source):
    return Polymer(source).go(10)


def part_2(source):
    return Polymer(source).go(40)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_rows(f"day_{day}.txt")
        self.test_source = read_rows("""NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""")

    def test_example_data_part_1(self):
        self.assertEqual(1588, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(3009, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(2188189693529, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(3459822539451, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
