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


def pairs(s: str):
    return consecutive_element_pairing(s, consecutive_element=2, map_to_func=lambda x: "".join(x))


def parse(source):
    p = pairs(source[0])
    instructions = {}
    for line in source[2:]:
        key, value = words(line)
        instructions[key] = value
    return p, instructions


def part_1(source, steps=10):
    formula = ""
    couples, instructions = parse(source)
    for i in range(steps):
        first = True
        formula = ""
        for key in couples:
            if first:
                ns = key[:1] + instructions[key] + key[1:]
                first = False
            else:
                ns = instructions[key] + key[1:]
            formula += ns
        couples = pairs(formula)
        # print(formula)
    counter = defaultdict(int)
    for i in formula:
        counter[i] += 1

    return max(counter.values()) - min(counter.values())


def part_2(source):
    return part_1(source, 40)


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
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
