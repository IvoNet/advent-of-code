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
        self.first_last = self.start_polymer[0] + self.start_polymer[-1:]
        self.couples = defaultdict(str)
        self.rules = defaultdict(str)
        self.result = defaultdict(int)
        self.__initialize()

    def get_pair(self, key):
        letter = self.rules[key]
        return key[0] + letter, letter + key[1]

    def go(self, steps=40):
        """Iterate the number of steps over the polymer:
        - initialize the result dict by giving the original couples from the start polymer a value of 1
        - __step the given amount of time extending the polymer (see doc of __step)
        - count all occurrences of a letter by summing the values for a pair if the letter exists in a pair
        - divide all the occurrences by two ignoring any fraction by int division
        - now we have the actual value except for the first and last letter they need to get 1 extra
        """
        for key in self.couples:
            self.result[key] += 1

        for _ in range(steps):
            self.__step()

        occurrences = defaultdict(int)
        for key, value in [x for x in self.result.items() if x[1] > 0]:
            occurrences[key[0]] += value
            occurrences[key[1]] += value

        for key, value in occurrences.items():
            occurrences[key] = value // 2 + (1 if key in self.first_last else 0)

        return max(occurrences.values()) - min(occurrences.values())

    def __step(self):
        """A __step consists of:
        - a new state
        - all the pairs in the result dict with a positive value actually exist in the polymer. The others can be
          ignored.
        - iterate over the keys with a positive value and follow the following rules:
            - retrieve the keys the current key will become
            - in the temp state do
                - decrease the current key as it will become two other keys by value as all the occurrences of
                  this key will change to other keys.
                - Increase the children found in new state by the value as all occurrences of the original
                  key will fall apart into these new ones
        - Update the result dict with the temp state by key and value

        NOTE 1: that all letters of the keys will be counted twice as the keys consist of 2 letter pairs.
                This will be fixed at the end.
        NOTE 2: the beginning and end letter of the polymer will be counted 1 less than they should be.
                Also fixed at the end.
        """
        temp = defaultdict(int)
        all_keys_with_a_positive_value = [x for x in self.result.items() if x[1] > 0]
        for key, value in all_keys_with_a_positive_value:
            children = self.get_pair(key)
            temp[key] -= value
            for child in children:
                temp[child] += value

        for key, value in temp.items():
            self.result[key] += value

    def __initialize(self):
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

    #
    # NNCB                 NN NC CB
    #
    #   #                  S i= 0             1
    #
    # CH -> B   # CH -> 0      *1*            0 CB BH
    # HH -> N   # HH -> 0
    # CB -> H   # CB -> 0  1   *0* CH* HB*    2
    # NH -> C   # NH -> 0
    # HB -> C   # HB -> 0      *1*            0 HC CB
    # HC -> B   # HC -> 0                     1
    # HN -> C   # HN -> 0
    # NN -> C   # NN -> 0  1   *0* NC* CN*    0
    # BH -> H   # BH -> 0                     1
    # NC -> B   # NC -> 0  1   *1* NB* BC*    0 NB BC
    # NB -> B   # NB -> 0      *1*            3 NB BB
    # BN -> B   # BN -> 0
    # BB -> N   # BB -> 0                     2
    # BC -> B   # BC -> 0      *1*            3 BB BC
    # CC -> N   # CC -> 0                     1
    # CN -> C   # CN -> 0      *1*            2 CC CN
    # if start key not in subset then key -> -1
    # after 1 steps it should be: B=2, C=2, H=1, N=2
    # after 1 steps             : B=3, C=4, H=2, N=3,
    # after 2 steps it should be: B=6, C=4, H=1, N=2
    # after 2 steps             : B=13, C=10, H=2, N=5
