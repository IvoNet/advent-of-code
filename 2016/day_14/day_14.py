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
from itertools import count
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def mdfive(s):
    return md5(s.encode()).hexdigest()


def md5i(salt, idx):
    return mdfive(f"{salt}{idx}")


def index(salt):
    found = 0
    for i in count():
        digest = md5i(salt, i)
        for x in range(len(digest) - 2):
            if digest[x] == digest[x + 1] == digest[x + 2]:
                c = digest[x]
                is_key = False
                for k in range(1, 1001):
                    digest2 = md5i(salt, i + k)
                    for y in range(len(digest2) - 5):
                        if digest2[y:y + 5] == c * 5:
                            is_key = True
                            break
                    if is_key:
                        break
                if is_key:
                    found += 1
                    if found == 64:
                        return i
                break  # only check the first


def part_1(source):
    return index(source)


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
