#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import sys
import unittest
from itertools import islice
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    plants = {i for i, c in enumerate(source[0].split()[-1]) if c == "#"}
    notes = {k: v for k, v in [line.strip().split(" => ") for line in source[2:]]}
    _(plants, notes)
    return plants, notes


def lives(plants, i, notes):
    """Determine if a plant lives, dies or spaws.
    - As the c in llcrr is the one in focus for the notes we need to add two to the beginning and end of the list
      and let them return "." when called for.
    - then see if we need to grow from the notes
    """
    llcrr = "".join(".#"[j in plants] for j in rangei(i - 2, i + 2))
    return notes.get(llcrr, ".") == "#"


def next_gen(plants, notes):
    """Generates the new generation based on the notes"""
    while True:
        yield plants
        expand = rangei(min(plants) - 3, max(plants) + 3)
        plants = {i for i in expand if lives(plants, i, notes)}


def part_1(source, generations=20):
    plants, notes = parse(source)
    _(plants, notes)
    grow = next_gen(plants, notes)
    for i in rangei(0, generations):
        plants = next(grow)
        _(i, ":", "".join(".#"[j in plants] for j in range(min(plants), max(plants))))
    return sum(plants)


def nth_generation(grow, nth, constant_genertion=100):
    """The sum of plants in the nth generation.
    The assuming is that linear growth after constant_genertion generations mark
    This you have to find out by increasing the part 1 generations to say 200 and print
    the results. You will se the pattern then."""
    plant_count_below_stable, first_stable_count = map(sum, islice(grow, constant_genertion, constant_genertion + 2))
    return plant_count_below_stable + (nth - constant_genertion) * (first_stable_count - plant_count_below_stable)


def part_2(source, generations=100):
    """Ok 50 bilion gens is a bit much to brute forse
    Observations:
    - by increasing the number of generations (playing a bit) you notice that at about 100 gens
      the groth becomes steady.
    - in my case an increase of 80 every gen after that so I guess:
    - (50_000_000_000 - 100) * 80 + gen(100)
    - Now lets put that into a function to generify
    """
    plants, notes = parse(source)
    return nth_generation(next_gen(plants, notes), 50 * 10 ** 9)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #""")

    def test_example_data_part_1(self):
        self.assertEqual(325, part_1(self.test_source, generations=20))

    def test_part_1(self):
        self.assertEqual(3248, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(4000000000000, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
