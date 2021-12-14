#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
--- Day 14: Extended Polymerization ---

The incredible pressures at this depth are starting to put a strain on your 
submarine. The submarine has polymerization equipment that would produce 
suitable materials to reinforce the submarine, and the nearby 
volcanically-active caves should even have the necessary input elements in 
sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer 
formula; specifically, it offers a polymer template and a list of pair 
insertion rules (your puzzle input). You just need to work out what 
polymer would result after repeating the pair insertion process a few times.

For example:

NNCB

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
CN -> C

The first line is the polymer template - this is the starting point of the 
process.

The following section defines the pair insertion rules. A rule like AB -> C 
means that when elements A and B are immediately adjacent, element C should 
be inserted between them. These insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously 
considers all three pairs:

- The first pair (NN) matches the rule NN -> C, so element C is inserted between the 
  first N and the second N.
- The second pair (NC) matches the rule NC -> B, so element B is inserted between the 
  N and the C.
- The third pair (CB) matches the rule CB -> H, so element H is inserted between the 
  C and the B.

Note that these pairs overlap: the second element of one pair is the first element of 
the next pair. Also, because all pairs are considered simultaneously, inserted elements 
are not considered to be part of a pair until the next step.

After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB

This polymer grows quickly. After step 5, it has length 97; After step 10, 
it has length 3073. After step 10, B occurs 1749 times, C occurs 298 times, 
H occurs 161 times, and N occurs 865 times; taking the quantity of the most 
common element (B, 1749) and subtracting the quantity of the least common 
element (H, 161) produces 1749 - 161 = 1588.

Apply 10 steps of pair insertion to the polymer template and find the most and 
least common elements in the result. What do you get if you take the quantity 
of the most common element and subtract the quantity of the least common element?


--- Part Two ---

The resulting polymer isn't nearly strong enough to reinforce the submarine. 
You'll need to run more steps of the pair insertion process; 
a total of 40 steps should do it.

In the above example, the most common element is B (occurring 2192039569602 times) 
and the least common element is H (occurring 3849876073 times); 
subtracting these produces 2188189693529.

Apply 40 steps of pair insertion to the polymer template and find the most and 
least common elements in the result. What do you get if you take the quantity 
of the most common element and subtract the quantity of the least common element?

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

    def elements_from(self, key: str) -> tuple[str, str]:
        """Create the two new keys based on the given key"""
        letter = self.rules[key]
        return key[0] + letter, letter + key[1]

    def go(self, steps: int = 40) -> int:
        """Iterate the number of steps over the polymer:
        - initialize the result dict by giving the original couples from the start polymer a value of 1
        - step the given amount of time extending the polymer (see doc of __step)
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
        - Update the result dict with the temp state by key and value

        NOTE 1: that all letters of the keys will be counted twice as the keys consist of 2 letter pairs.
                This will be fixed at the end.
        NOTE 2: the beginning and end letter of the polymer will be counted 1 less than they should be.
                Also fixed at the end.
        """
        temp = defaultdict(int)
        all_keys_with_a_positive_value = [x for x in self.result.items() if x[1] > 0]
        for key, value in all_keys_with_a_positive_value:
            elements = self.elements_from(key)

            temp[key] -= value

            for child in elements:
                temp[child] += value

        for key, value in temp.items():
            self.result[key] += value

    def __initialize(self) -> None:
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
