#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from itertools import permutations
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False
first_debug_print = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    global first_debug_print
    if DEBUG:
        if first_debug_print:
            first_debug_print = False
            print()
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    persons = set()
    happiness = {}
    for line in source:
        s = line[:-1].split()
        persons.add(s[0])
        persons.add(s[-1])
        happiness[s[0], s[-1]] = int(s[3]) if s[2] == "gain" else -int(s[3])
    return persons, happiness


def best_seating_arrangement(persons, happiness):
    """Check for all permutations of the persons the best happiness table seating
    - check both ways
    - don't forget to "loop" around and compare the first and the last member
      (also both ways)
    """
    happiest = float("-inf")
    for i, seating in enumerate(permutations(persons)):
        scale = 0
        for i in range(len(persons) - 1):
            scale += happiness[seating[i], seating[i + 1]]
            scale += happiness[seating[i + 1], seating[i]]
        scale += happiness[seating[-1], seating[0]]
        scale += happiness[seating[0], seating[-1]]
        happiest = max(happiest, scale)
    return happiest


def part_1(source):
    persons, happiness = parse(source)
    return best_seating_arrangement(persons, happiness)


def part_2(source):
    persons, happiness = parse(source)
    for person in persons:
        happiness["Ivo", person] = 0
        happiness[person, "Ivo"] = 0
    persons.add("Ivo")
    return best_seating_arrangement(persons, happiness)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.test_source = read_rows("""Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.""")

    def test_example_data_part_1(self):
        self.assertEqual(330, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(618, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(601, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
