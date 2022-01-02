#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import re
import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints, consecutive_element_pairing

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Ip:

    def __init__(self, ip) -> None:
        self.parts = re.findall(r"(\w+)", ip)
        self.brackets = re.findall(r"\[(\w+)]", ip)
        for b in self.brackets:
            self.parts.remove(b)
        _(self.parts, self.brackets)
        assert self.parts is not None
        assert self.brackets is not None

    def has_tls(self):
        for word in self.brackets:
            for a, b, c, d in consecutive_element_pairing(word, 4, list):
                if a != b and c != d and a == d and b == c:
                    return False
        for word in self.parts:
            for a, b, c, d in consecutive_element_pairing(word, 4, list):
                if a != b and c != d and a == d and b == c:
                    return True
        return False

    def has_ssl(self):
        aba = []
        for word in self.parts:
            for a, b, c in consecutive_element_pairing(word, 3, list):
                if a != b and a == c:
                    aba.append((a, b, c))
        for word in self.brackets:
            for a, b, c in consecutive_element_pairing(word, 3, list):
                if a != b and a == c:
                    for d, e, f in aba:
                        if d == b and f == b and e == a == c:
                            return True
        return False


def part_1(source):
    total = 0
    for ip in source:
        total += 1 if Ip(ip).has_tls() else 0
    return total


def part_2(source):
    total = 0
    for ip in source:
        total += 1 if Ip(ip).has_ssl() else 0
    return total


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""abba[mnop]qrst""")
        self.test_source_wrong_1 = read_rows("""abcd[bddb]xyyx""")
        self.test_source_wrong_2 = read_rows("""aaaa[qwer]tyui""")

    def test_example_1_data_part_1(self):
        self.assertEqual(1, part_1(self.test_source))

    def test_example_2_data_part_1(self):
        self.assertEqual(0, part_1(self.test_source_wrong_1))

    def test_example_3_data_part_1(self):
        self.assertEqual(0, part_1(self.test_source_wrong_2))

    def test_part_1(self):
        self.assertEqual(115, part_1(self.source))

    def test_ssl_1(self):
        self.assertTrue(Ip("aba[bab]xyz").has_ssl())

    def test_ssl_2(self):
        self.assertFalse(Ip("xyx[xyx]xyx").has_ssl())

    def test_ssl_3(self):
        self.assertTrue(Ip("aaa[kek]eke").has_ssl())

    def test_ssl_4(self):
        self.assertTrue(Ip("zazbz[bzb]cdb").has_ssl())

    def test_part_2(self):
        self.assertEqual(231, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
