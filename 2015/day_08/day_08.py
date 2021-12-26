#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source):
    code = 0
    memory = 0
    for line in source:
        code += len(line)
        memory += len(eval(line))
    return code - memory


def part_2(source):
    orig = 0
    new_code = 0
    for line in source:
        orig += len(line)
        nl = '"' + line.replace("\\", "\\\\").replace('"','\\"') + '"'
        _(nl)
        new_code += len(nl)
    return new_code - orig


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows(f"day_{day.zfill(2)}_test.input")

    def test_example_data_part_2(self):
        self.assertEqual(19, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2046, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
