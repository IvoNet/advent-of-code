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

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    ret = []
    for line in source:
        l, h = ints(line.replace("-", " "))
        ret.append(range(l, h + 1))
    return ret


def part_1(source):
    ranges = parse(source)
    srted = sorted(ranges, key=lambda r: r.start, reverse=True)
    print(srted)
    ret = []
    lowest = 0
    while srted:
        current = srted.pop()
        if current.start == 0:
            ret.append(current)
            lowest = current.stop
            _(f"Start: {lowest}")
            continue
        if current.start <= lowest:
            if current.stop <= lowest:
                # just ignore as it fully falls in another range
                _(f"Ignoring range: {current}")
                continue
            if current.stop > lowest:
                ret.append(current)
                lowest = current.stop
                _(current)
                _(f"New lowest: {lowest}")
                continue
        if current.start - 1 == lowest:
            lowest = current.stop
            _(current)
            _(f"Just one higher. New lowest: {lowest}")
            continue
        _(f"Other: {current}")
        break

    #
    #
    # for i, r in enumerate(srted[:-1]):
    #     print(r.start, r.stop, srted[i+1].start, srted[i+1].start)
    #     if r.stop > srted[i+1].stop:
    #         return r.stop
    # print(srted)
    # return None


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""5-8
0-2
4-7""")

    def test_example_data_part_1(self):
        self.assertEqual(3, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
