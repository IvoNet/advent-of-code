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
from itertools import permutations
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints, chunkify
from ivonet.str import rotate_right

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def flip(key):
    ret = key.split("/")
    ret = list(permutations(ret, 2 + len(ret) % 2))
    result = []
    for r in ret:
        result.append("/".join(r))
    return result


def rotate(key, steps=1):
    ret = "".join(key.split("/"))
    ret = rotate_right(ret, steps)
    ret = chunkify(ret, 2 + len(ret) % 2)
    ret = "/".join(ret)
    return ret


def parse(source):
    """Parse the source and
    - add all the flipped and rotated combinations of the same key to the rules
      with its value
    """
    rules = {}
    for line in source:
        line = line.replace("/", "").replace(".", "0").replace("#", "1")
        key, value = line.split(" => ")
        rules[ints(key)] = value
        for c in flip(key):
            rules[c] = value
            for i in range(len(key) - 2):
                rules[rotate(c, i)] = value
    _(rules)
    return rules


class ArtProgram:

    def __init__(self, rules, base=".#./..#/###") -> None:
        self.rules = rules
        self.base = base.split("/")

    def enhance(self, key):
        if (len(key) - 2) % 3 == 0:
            return self.enhance_odd(key)
        else:
            return self.enhance_even(key)

    def enhance_odd(self, key):
        if len(key.replace("/", "")) == 9:
            return self.rules[key]

        # TODO real enhance here
        return None

    def enhance_even(self, key):
        _("!!!")
        return key


def part_1(source, base=".#./..#/###", times=2):
    rules = parse(source)
    a = base
    for i in range(times):
        a = enhance(a)
        print("\n".join(rules[a].split("/")))

    return None


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#                           """)

    def test_example_data_part_1(self):
        self.assertEqual(None, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
