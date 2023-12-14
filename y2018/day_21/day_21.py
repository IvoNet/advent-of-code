#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
assembly
asm
"""

import os
import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def asm():
    """Just rewritten the same thing in python
    This is a "my version" specific implementation
    Did not want to make it generic as I did not like the puzzle all that much
    """
    reg_5_values = []
    reg_e = 0
    seen_reg_d = set()
    while True:
        reg_d = reg_e | 65536
        if reg_d in seen_reg_d:
            break
        seen_reg_d.add(reg_d)
        reg_e = 13159625
        while True:
            reg_c = reg_d & 255
            reg_e = reg_c + reg_e
            reg_e &= 16777215
            reg_e *= 65899
            reg_e &= 16777215
            if 256 > reg_d:
                reg_5_values.append(reg_e)
                break
            else:
                reg_d //= 256
    return reg_5_values


def part_1(source):
    return asm()[0]


def part_2(source):
    return asm()[-1]


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(3941014, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(13775890, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
