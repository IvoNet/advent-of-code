#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

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
        self.template = source[0]
        self.first_last = self.template[0] + self.template[-1:]
        self.pair = defaultdict(str)
        self.insertion = defaultdict(str)
        self.result = defaultdict(int)
        self.__initialize()

    def elements_from(self, key: str) -> tuple[str, str]:
        """Create the two new keys based on the given key"""
        letter = self.insertion[key]
        return key[0] + letter, letter + key[1]

    def go(self, steps: int = 40) -> int:
        """Iterate the number of steps over the polymer:
        - initialize the result dict by giving the original couples from the start polymer a value of 1
        - step the given amount of time extending the polymer (see doc of __step)
        - count all occurrences of a letter by summing the values for a pair if the letter exists in a pair
        - divide all the occurrences by two ignoring any fraction by int division
        - now we have the actual value except for the first and last letter they need to get 1 extra
        """
        for key in self.pair:
            self.result[key] += 1

        for _ in range(steps):
            self.__step()

        occurrences = defaultdict(int)
        for key, value in self.__all_result_keys_with_a_positive_value():
            occurrences[key[0]] += value
            occurrences[key[1]] += value

        for key, value in occurrences.items():
            occurrences[key] = value // 2 + (1 if key in self.first_last else 0)

        return max(occurrences.values()) - min(occurrences.values())

    def __step(self) -> None:
        """A __step consists of:
        - a new temp state
        - all the pairs in the result dict with a positive value actually exist in the polymer. The others can be
          ignored.
        - iterate over the keys with a positive value and follow the following rules:
            - retrieve the keys (elements) the current key will become
            - in the temp state do
                - decrease the current key as it will become two other keys by value as all the occurrences of
                  this key will change to other keys.
                - Increase the elements found by the value as all occurrences of the original key will fall
                  apart into these new ones
        - update the result dict with the temp state by key and value

        NOTE 1: that all letters of the keys will be counted twice as the keys consist of 2 letter pairs.
                This will be fixed at the end.
        NOTE 2: the beginning and end letter of the polymer will be counted 1 less than they should be.
                Also fixed at the end.
        """
        temp = defaultdict(int)
        for key, value in self.__all_result_keys_with_a_positive_value():
            elements = self.elements_from(key)

            temp[key] -= value

            for child in elements:
                temp[child] += value

        for key, value in temp.items():
            self.result[key] += value

    def __all_result_keys_with_a_positive_value(self):
        return [x for x in self.result.items() if x[1] > 0]

    def __initialize(self) -> None:
        self.pair = consecutive_element_pairing(self.template, elements=2,
                                                map_to_func=lambda x: "".join(x))
        for line in self.source[2:]:
            key, value = words(line)
            self.insertion[key] = value


def part_1(source):
    return Polymer(source).go(10)


def part_2(source):
    return Polymer(source).go(40)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
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
