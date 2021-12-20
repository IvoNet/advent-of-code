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
from ivonet.iter import ints, words, consecutive_element_pairing

sys.dont_write_bytecode = True


class Polymer:
    """Polymer day 14 exercise:
    e.g. as in example the template is NNCB:
    - first initialize the template (first line of the source)
    - get all the consecutive pairs from the template
    - go...
    - first insert pass called with: pair = NN, step = 0, stop = 10
    - No cache entries yet so lets do some work
    - get the leaves (NC, CN) left and right and start the descent parsing of the left leaf CN
    - no cache hit and not at stop yet (1) so again go... this happends 10 steps on the left leaf
    - now the else is hit and because the second element of one pair is the first element of the next pair
      we calculate the left one here and in the right hand the other letter otherwise we would count them twice
    - this way the last letter in the template will never be counted (is right side) we we need to
      initialise the counter with it, which happens in the go function
    - now we cache this pair with its count in the cache for later retrieval
    - return the count (1) of the left letter to the last recursive call on the left side
    - now the right side is calling itself and the left descent starts immediately again, and so on
    - eventually we climb out of all the recursive descents and we return all we have gatherd of the left
      and right side back to go, which will immediately start on the second pair (NC) and repeat all this again

                                          NN
                                        /   \
                                       NC    CN
                                      /  \     ...
                                     NB   BC
                                    / \     ...
                                   NB BB
                                 ... and so on
    - eventually we have a cumulated Counter for all the letters and we can ask the max - min of those values.

    """

    def __init__(self, source, verbose=False) -> None:
        self.template = source[0]
        self.inserts = dict([words(x) for x in source[2:] if x])
        self.pairs = consecutive_element_pairing(self.template,
                                                 consecutive_element=2,
                                                 map_to_func=lambda x: "".join(x))
        self.cache = {}
        self.occurrences = Counter()
        self.verbose = verbose

    def pp(self, *args):
        if self.verbose:
            print(" ".join([str(x) for x in args]))

    def insert(self, pair: str, step: int, stop: int) -> Counter:
        if (pair, step) in self.cache:
            self.pp("Cache hit on:", (pair, step), self.cache[(pair, step)])
            return self.cache[(pair, step)]
        self.pp("Entry:", pair)
        if step < stop:
            left, right = self.leaves(pair)
            self.pp(f"left[{left}], right[{right}]")
            self.pp("left descend:", left)
            left_letter = self.insert(left, step + 1, stop)
            self.pp(f"Left back from:", left, left_letter)
            self.pp("right descend:", right)
            right_letter = self.insert(right, step + 1, stop)
            self.pp(f"Right back from:", right, right_letter)
            self.cache[(pair, step)] = left_letter + right_letter
            return left_letter + right_letter
        else:
            self.cache[(pair, step)] = Counter(pair[0])
            self.pp("Iterations done on", pair, "at step:", step, "counting left letter")
            return Counter(pair[0])

    def leaves(self, pair) -> tuple[str, str]:
        left = pair[0] + self.inserts[pair]
        right = self.inserts[pair] + pair[1]
        return left, right

    def go(self, stop) -> int:
        self.occurrences = Counter(self.template[-1])
        for pair in self.pairs:
            self.occurrences += self.insert(pair, 0, stop)
        return max(self.occurrences.values()) - min(self.occurrences.values())


def part_1(source):
    return Polymer(source).go(10)


def part_2(source):
    return Polymer(source).go(40)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_rows(f"day_{day}.input")
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

    def test_example_data_part_1a(self):
        """Put verbose on True to see what happens"""
        self.assertEqual(1588, Polymer(self.test_source, verbose=False).go(10))

    def test_part_1(self):
        self.assertEqual(3009, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(2188189693529, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(3459822539451, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
