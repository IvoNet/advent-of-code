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
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def trap(left, center, right):
    if "^" == left == center and "." == right:
        return True
    if "^" == center == right and "." == left:
        return True
    if "^" == right and "." == left == center:
        return True
    if "^" == left and "." == right == center:
        return True
    return False


def part_1_2(source, rows=40):
    ret = [source]
    for _ in range(rows - 1):
        new_row = ""
        last_row = ret[-1]
        for i in range(len(last_row)):
            if i == 0:
                new_row += "^" if trap(".", last_row[i], last_row[i + 1]) else "."
            elif i == len(source) - 1:
                new_row += "^" if trap(last_row[i - 1], last_row[i], ".") else "."
            else:
                new_row += "^" if trap(last_row[i - 1], last_row[i], last_row[i + 1]) else "."
        ret.append(new_row)
    return "".join(ret).count(".")


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""..^^.""")

    def test_trap(self):
        self.assertTrue(trap(".", "^", "^"))
        self.assertTrue(trap("^", "^", "."))
        self.assertTrue(trap("^", ".", "."))
        self.assertTrue(trap(".", ".", "^"))

    def test_not_trap(self):
        self.assertFalse(trap(".", ".", "."))
        self.assertFalse(trap("^", "^", "^"))
        self.assertFalse(trap(".", "^", "."))

    def test_example_data_part_1(self):
        self.assertEqual(6, part_1_2(self.test_source, rows=3))

    def test_part_1(self):
        self.assertEqual(1961, part_1_2(self.source, rows=40))

    def test_part_2(self):
        self.assertEqual(20000795, part_1_2(self.source, rows=400000))


if __name__ == '__main__':
    unittest.main()
