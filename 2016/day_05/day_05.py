#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from functools import lru_cache
from hashlib import md5
from pathlib import Path

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def decoder(key):
    idx = 0
    while True:
        answer = f"{key}{idx}".encode("ascii")
        digest = md5(answer).hexdigest()
        if digest.startswith("00000"):
            _(answer, digest)
            yield digest[5]
        idx += 1


def inspired_decoder(key):
    idx = 0
    while True:
        answer = f"{key}{idx}".encode("ascii")
        digest = md5(answer).hexdigest()
        if digest.startswith("00000") and digest[5] in "01234567":
            _(answer, digest)
            yield digest[5], digest[6]
        idx += 1


def part_1(source):
    ret = ""
    decode = decoder(source)
    for _ in range(8):
        ret += next(decode)
    return ret


def part_2(source):
    ret = [None] * 8
    decode = inspired_decoder(source)
    while None in ret:
        k, v = next(decode)
        k = int(k)
        if ret[k] is None:
            ret[k] = v
        _(ret)
    return "".join(ret)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"day_{day.zfill(2)}.input")
        self.test_source = read_data("""abc""")

    def test_example_data_part_1(self):
        self.assertEqual("18f47a30", part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual("f77a0e6e", part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual("05ace8e3", part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual("999828ec", part_2(self.source))


if __name__ == '__main__':
    unittest.main()
