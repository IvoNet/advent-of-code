#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from itertools import combinations
from pathlib import Path

from more_itertools import set_partitions

from ivonet.calc import prod
from ivonet.files import read_ints
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def brute_force_too_long(source) -> int:
    """Tried this one but killed it after a few minutes.... way to slow!
    Not even sure if it would work"""
    cache = {}
    quantum_entanglement = float("inf")
    for a, b, c in set_partitions(source, 3):
        if sum(a) == sum(b) == sum(c):
            qe = prod(a)
            _("QE=", qe, "[", a, b, c, "]")
            cache[qe] = (a, b, c)
            if qe < quantum_entanglement:
                quantum_entanglement = qe
    return int(quantum_entanglement)


def process(source, groups=3) -> int:
    """Tried bruteforce but was way too slow.
    so now I just try to find the smalest group that sums up to 1 third of the total sum (they all must be equal)
    In my solution I assume that if I have one group that sums up to the needed amount the other two will too.
    NOTE: This is not a rule per se! But for perormance reasons I will try this assumption first.
    If I have found the smallest group that sums up I will probably also have the best Quantum Entanglement
    Seems to work and is fast
    """
    s = sum(source)
    target = s // groups
    for i in range(1, len(source) - 1):
        qe = float("inf")
        for g in combinations(source, i):
            if sum(g) == target:
                p = prod(g)
                qe = min(qe, p)
        if qe < float("inf"):
            return qe


def part_1(source):
    return process(source)


def part_2(source):
    return process(source, groups=4)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_ints(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")), delimiter="\n")

    def test_part_1(self):
        self.assertEqual(10439961859, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(72050269, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
