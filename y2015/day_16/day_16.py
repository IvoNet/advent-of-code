#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

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


def logic(logica):
    ret = {}
    for line in logica:
        key = line.split(":")[0].strip()
        value = ints(line)[0]
        ret[key] = value
    return ret


def aunts(source):
    ret = {}
    for line in source:
        line = line.replace(":", "").replace(",", "")
        nrs = ints(line)
        assert len(nrs) == 4
        items = line.split()
        ret[nrs[0]] = {items[2]: nrs[1],
                       items[4]: nrs[2],
                       items[6]: nrs[3]}
    return ret


def narrow_down(aunties: dict, item: str, amount: int):
    ret = aunties.copy()
    for aunt, items in aunties.items():
        if item in items and aunties[aunt][item] != amount:
            del ret[aunt]
    return ret


def part_1(source, logica):
    facts = logic(logica)
    aunties = aunts(source)
    _(facts)
    _(aunties)
    for key, value in facts.items():
        aunties = narrow_down(aunties, key, value)
        _(aunties)
    assert len(aunties) == 1
    return list(aunties.keys())[0]


FUNCTION = {
    "cats": lambda left, right: left > right,
    "trees": lambda left, right: left > right,
    "pomeranians": lambda left, right: left < right,
    "goldfish": lambda left, right: left < right,
    "children": lambda left, right: left == right,
    "samoyeds": lambda left, right: left == right,
    "akitas": lambda left, right: left == right,
    "vizslas": lambda left, right: left == right,
    "cars": lambda left, right: left == right,
    "perfumes": lambda left, right: left == right,
}


def narrow_down_2(aunties: dict, item: str, amount: int):
    ret = aunties.copy()
    for aunt, items in aunties.items():
        if item in items and not FUNCTION[item](aunties[aunt][item], amount):
            _("deleting:", aunt, item)
            del ret[aunt]
    return ret


def part_2(source, logica):
    facts = logic(logica)
    aunties = aunts(source)

    for key, value in facts.items():
        aunties = narrow_down_2(aunties, key, value)
        _(aunties)
    assert len(aunties) == 1
    return list(aunties.keys())[0]


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))
        self.logica = read_rows("""children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1""")

    def test_part_1(self):
        self.assertEqual(373, part_1(self.source, self.logica))

    def test_part_2(self):
        self.assertEqual(260, part_2(self.source, self.logica))


if __name__ == '__main__':
    unittest.main()
