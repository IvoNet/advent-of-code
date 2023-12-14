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

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def prepare(source):
    program = []
    for line in source:
        tmp = line.strip().split()
        cmd = [tmp[0]]
        for x in tmp[1:]:
            try:
                cmd.append(int(x))
            except ValueError:
                cmd.append(x)
        program.append(cmd)
    return program


def part_1(source, a=0, b=0, c=0, d=0):
    # see 07 and 23 of 2015
    program = prepare(source)
    register = {
        "a": a,
        "b": b,
        "c": c,
        "d": d,
    }
    i = 0
    while True:
        _(register)
        try:
            cmd = program[i]
        except IndexError:
            return register["a"]
        if cmd[0] == "cpy" and type(cmd[1]) == int:
            register[cmd[2]] = cmd[1]
            i += 1
            continue
        if cmd[0] == "cpy" and type(cmd[1]) != int:
            register[cmd[2]] = register[cmd[1]]
            i += 1
            continue
        if cmd[0] == "inc":
            register[cmd[1]] += 1
            i += 1
            continue
        if cmd[0] == "dec":
            register[cmd[1]] -= 1
            i += 1
            continue
        if cmd[0] == "jnz" and type(cmd[1]) == int and cmd[1] != 0:
            i += cmd[2]
            _(f"jnz to cmd {i}")
            continue
        if cmd[0] == "jnz" and register[cmd[1]] != 0:
            i += cmd[2]
            _(f"jnz to cmd {i}")
            continue
        _("No command going to next command:", cmd)
        i += 1
    return None


def part_2(source):
    return part_1(source, c=1)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a""")

    def test_example_data_part_1(self):
        self.assertEqual(42, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(318083, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(9227737, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
