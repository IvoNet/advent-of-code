#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from collections import defaultdict
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints, sort_dict_on_values
from ivonet.primes import is_prime

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def house_brute_force(nr: int) -> int:
    if nr == 1:
        return 10
    presents = nr * 10 + 10
    if is_prime(nr) or nr == 1:
        return presents
    half = nr // 2 + 1
    for i in range(2, half):
        if nr % i == 0:
            presents += 10 * i
    return presents


def house(nr: int, elf_cache) -> int:
    if nr == 1:
        return 10
    if elf_cache.get(nr) is not None:
        return elf_cache[nr]
    else:
        elf_cache[nr] = nr * 10
    # if is_prime(nr) or nr == 1:
    #     elf_cache[nr] = nr * 10
    #     return nr * 10
    half = nr // 2
    presents = house(nr, elf_cache)
    for i in range(1, half + 1):
        if nr % i == 0:
            presents += house(i, elf_cache)
    return presents


def presents(match):
    presents = defaultdict(int)
    max_elves = match // 10
    for elf in range(1, max_elves):
        for house in range(elf, max_elves, elf):
            presents[house] += elf * 10
    return sort_dict_on_values(presents, reverse=True).items()[0][0]


def part_1(source):
    return presents(int(source))


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(776160, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(786240, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
