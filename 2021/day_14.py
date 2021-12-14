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
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints, consecutive_element_pairing, words

sys.dont_write_bytecode = True


class Polymer(object):

    def __init__(self, source) -> None:
        self.source = source
        self.start_polymer = source[0]
        self.first = self.start_polymer[0]
        self.last = self.start_polymer[-1:]
        self.couples = defaultdict(str)
        self.rules = defaultdict(str)
        self.result = defaultdict(int)
        self.total = defaultdict(int)
        self.parse()

    def go(self, steps=40):
        for key in self.couples:
            self.result[key] += 1
        for _ in range(steps):
            temp = defaultdict(int)
            for key, value in [x for x in self.result.items() if x[1] > 0]:
                children = self.get_pair(key)
                temp[key] -= value
                for child in children:
                    temp[child] += value

            for key, value in temp.items():
                self.result[key] += value
            print(temp)
            print(self.result)

        for key, value in [x for x in self.result.items() if x[1] > 0]:
            print(key, end="")
            self.total[key[0]] += value
            self.total[key[1]] += value
        print()
        for key, value in self.total.items():
            val = value
            val /= 2
            self.total[key] = int(val)
            if key in [self.first, self.last]:
                self.total[key] += 1
        print("Total:")
        print(self.total)
        return max(self.total.values()) - min(self.total.values())

    def get_pair(self, key):
        letter = self.rules[key]
        return key[0] + letter, letter + key[1]

    def parse(self):
        self.couples = consecutive_element_pairing(self.start_polymer, consecutive_element=2,
                                                   map_to_func=lambda x: "".join(x))
        for line in self.source[2:]:
            key, value = words(line)
            self.rules[key] = value


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
