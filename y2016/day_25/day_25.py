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
from itertools import count
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


def assembunny(program, a=0, b=0, c=0, d=0):
    # see also day 23 and day 12.... Used the day 12 version but cleaned it up a bit
    register = {
        "a": a,
        "b": b,
        "c": c,
        "d": d,
    }
    antenna = []
    i = 0
    while True:
        _(register)
        try:
            cmd = program[i]
        except IndexError:
            return register["a"]
        if cmd[0] == "cpy":
            register[cmd[2]] = cmd[1] if type(cmd[1]) == int else register[cmd[1]]
        elif cmd[0] == "inc":
            register[cmd[1]] += 1
        elif cmd[0] == "dec":
            register[cmd[1]] -= 1
        elif cmd[0] == "jnz":
            val = cmd[1] if type(cmd[1]) == int else register[cmd[1]]
            if val != 0:
                i += cmd[2] - 1
        elif cmd[0] == "out":
            antenna.append(register[cmd[1]])
            if register[cmd[1]] != ((len(antenna) + 1) % 2):  # nice way to check the flipping action
                break
            if len(antenna) == 42:  # This is kinda endless right :-)
                return a
        i += 1


def part_1(source):
    program = prepare(source)
    for i in count():
        if assembunny(program, a=i):
            return i


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(180, part_1(self.source))


if __name__ == '__main__':
    unittest.main()
