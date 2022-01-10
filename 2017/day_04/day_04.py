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

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source: str, sorting=False) -> list[list[str]]:
    pfs = [x.split() for x in source]
    if sorting:
        return [["".join(sorted(item)) for item in row] for row in pfs]
    return pfs


def part_1(source, sorting=False):
    passphrases: list[list[str]] = parse(source, sorting=sorting)
    _(passphrases)
    total = 0
    for pf in passphrases:
        valid = True
        check = pf.pop()
        while pf:
            if check in pf:
                valid = False
                break
            check = pf.pop()
        total += 1 if valid else 0
    return total


def part_2(source):
    return part_1(source, sorting=True)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(455, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(186, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
