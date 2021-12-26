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

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def part_1(source):
    instructions = {}
    for line in source:
        v, k = line.split(" -> ")
        # value = v.replace("AND", "&").replace("LSHIFT", "<<").replace("RSHIFT", ">>").replace("OR", "|")
        # if value.strip().startswith("NOT"):
        #     value = value.replace("NOT ", "")
        #     value += " ^ 0xFFFF"
        # numbers = ints(value)
        # if len(value.strip().split()) == 1 == len(numbers):
        #     value = numbers[0]
        instructions[k.strip()] = v.strip()
    _(instructions)
    for i in instructions:
        for k, v in instructions.items():
            if k == "a":
                continue
            numbers = ints(v)
            if len(v.strip().split()) == 1 == len(numbers):
                instructions["a"] = instructions["a"].replace(f"{k}", f"{v}")
            else:
                instructions["a"] = instructions["a"].replace(f"{k}", f"({v})")
    _(instructions["a"])
    cmd = instructions["a"]
    cmd = cmd.replace("AND", "&") \
        .replace("LSHIFT", "<<") \
        .replace("RSHIFT", ">>") \
        .replace("OR", "|") \
        .replace("NOT", "0xFFFF ^")
    indent_print(cmd)
    indent_print(instructions["a"])

    # _(cmd)
    return eval(cmd)


def indent_print(cmd):
    ind = 0
    inds = "  "
    prev = ""
    for i, c in enumerate(cmd):
        if c in "()":
            prev = c
            if c == "(":
                print(f"\n{inds * ind}{c}", end="")
                ind += 1
            if c == ")":
                ind -= 1
                print(f"\n{inds * ind}{c}", end="")
            if ind < 0:
                ind = 0
        else:
            if prev == "(":
                print(f"\n{inds * ind}{c}", end="")
                prev = ""
            else:
                print(f"{c}", end="")


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i""")

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
