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
from itertools import count
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def convert(data):
    a = data
    b = a[::-1].replace("1", "#").replace("0", "1").replace("#", "0")
    return f"{a}0{b}"


def checksum(data, n=2):
    ret = ""
    for p in [data[i:i + n] for i in range(0, len(data), n)]:
        if p in ["11", "00"]:
            ret += "1"
            continue
        ret += "0"
    _(ret)
    if len(ret) % 2 == 0:
        ret = checksum(ret, n)
    return ret


def part_1(source, disk_size=272):
    for _ in count():
        source = convert(source)
        if len(source) >= disk_size:
            return checksum(source[:disk_size])


def part_2(source):
    return part_1(source, disk_size=35651584)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_convert(self):
        self.assertEqual("100", convert("1"))
        self.assertEqual("001", convert("0"))
        self.assertEqual("11111000000", convert("11111"))
        self.assertEqual("1111000010100101011110000", convert("111100001010"))

    def test_checksum(self):
        self.assertEqual("100", checksum("110010110100"))

    def test_part_1(self):
        self.assertEqual("10010010110011010", part_1(self.source))

    def test_part_2(self):
        self.assertEqual("01010100101011100", part_2(self.source))


if __name__ == '__main__':
    unittest.main()
