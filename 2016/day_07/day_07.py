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
    """Representation of IPv7"""

    def __init__(self, ip) -> None:
        self.parts = re.findall(r"(\w+)", ip)  # finds all of them
        self.brackets = re.findall(r"\[(\w+)]", ip)
        for b in self.brackets:
            self.parts.remove(b)  # just remove them from the parts list
        assert self.parts is not None
        assert self.brackets is not None
        _(self.parts, self.brackets)

    def has_tls(self):
        """TLS (transport-layer snooping) protocol checker
        - if ABBA exists in the bracketed words it is not good
        - if not rule one and ABBA exists in the parts then good
        """
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
        """SSL (super-secret listening) protocol checker
        if any ABA combi exists in the supernet sequences and has a corresponding
        BAB sequence in the hypernet sequences all is good otherwise not.
        """
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
    return sum(1 for x in source if Ip(x).has_tls())


def part_2(source):
    return sum(1 for x in source if Ip(x).has_ssl())


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""abba[mnop]qrst""")

    def test_tls_1(self):
        self.assertTrue(Ip("abba[mnop]qrst").has_tls())

    def test_tls_2(self):
        self.assertFalse(Ip("abcd[bddb]xyyx").has_tls())

    def test_tls_3(self):
        self.assertFalse(Ip("aaaa[qwer]tyui").has_tls())

    def test_tls_4(self):
        self.assertTrue(Ip("ioxxoj[asdfgh]zxcvbn").has_tls())

    def test_example_1_data_part_1(self):
        self.assertEqual(1, part_1(self.test_source))

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
