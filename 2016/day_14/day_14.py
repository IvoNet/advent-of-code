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
from hashlib import md5
from itertools import groupby, count
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Potential(NamedTuple):
    key: str
    idx: int
    rep: str


def key_gen(salt: str, nr=64):
    """Generate new one-time pad keys
    rules:
    - md5 based on salt
    - lowercase hexadecimal representation
    - if a triplet is in the key
    - in next thousand hashes has the same triplet but 5 times
    """
    idx = 1
    potential_keys: list[Potential] = []
    keys = []
    for idx in count():
        answer = f"{salt}{idx}".encode("ascii")
        digest = md5(answer).hexdigest()
        groups = [(label, sum(1 for _ in group)) for label, group in groupby(digest)]
        five = [x[0] for x in groups if x[1] == 5]
        if five:
            pots = [x for x in potential_keys if x.rep == five[0]]
            for key in pots:
                if idx - key.idx <= 1000:
                    keys.append(key.key)
                    potential_keys.remove(key)
                else:
                    pots.remove(key)
        three = [x[0] for x in groups if x[1] == 3]
        if three:
            potential_keys.append(Potential(digest, idx, three[0]))
        if len(keys) >= 64:
            break
        idx += 1
    return idx, keys


def part_1(source):
    return key_gen(source)[0]


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""abc""")

    def test_example_data_part_1(self):
        self.assertEqual(22728, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
