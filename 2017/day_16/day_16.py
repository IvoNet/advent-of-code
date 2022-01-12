#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Used day_21 of 2016 for some string rotation and swapping
"""

import os
import sys
import unittest
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints
from ivonet.str import swap_position, rotate_right, swap_letter

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    instructions = source.split(",")
    ret = []
    for instruction in instructions:
        if instruction.startswith("p"):
            ret.append((instruction[0], instruction[1], instruction[-1]))
        else:
            ret.append((instruction[0], *ints(instruction)))
    return ret


def dance(instructions, dancers="abcdefghijklmnop"):
    """Generified the instructions created 2016/day_21 and used them here"""
    d = dancers
    for cmd, *param in instructions:
        if cmd == "s":
            d = rotate_right(d, *param)
        elif cmd == "x":
            d = list(swap_position(d, *param))
        elif cmd == "p":
            d = swap_letter(d, *param)
    return d


def part_1(source, dancers="abcdefghijklmnop"):
    instructions = parse(source)
    return dance(instructions, dancers)


def part_2(source):
    """I Bilion is a lot and more combinations that 16 dancers can make!
    lets first find out how many combainations they have before comming
    back to the same starting position with these dance instructions.
    """
    instructions = parse(source)
    dancers = "abcdefghijklmnop"
    check_dancers = "abcdefghijklmnop"
    combinations = 0
    while True:
        combinations += 1
        check_dancers = dance(instructions, check_dancers)
        if check_dancers == dancers:
            break
    for _ in range(1_000_000_000 % combinations):
        dancers = dance(instructions, dancers=dancers)
    return dancers


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""s1,x3/4,pe/b""")

    def test_example_data_part_1(self):
        self.assertEqual("baedc", part_1(self.test_source, dancers="abcde"))

    def test_part_1(self):
        self.assertEqual("hmefajngplkidocb", part_1(self.source))

    def test_part_2(self):
        self.assertEqual("fbidepghmjklcnoa", part_2(self.source))


if __name__ == '__main__':
    unittest.main()
