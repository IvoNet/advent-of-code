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
from collections import defaultdict
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


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


def duet(program):
    # see also day 23 and day 12.... Used the day 12 version but cleaned it up a bit
    register = defaultdict(int)
    antenna = []
    i = 0
    last_sound = None
    while True:
        _(register)
        try:
            cmd = program[i]
        except IndexError:
            return None
        if cmd[0] == "set":
            register[cmd[1]] = cmd[2] if type(cmd[2]) == int else register[cmd[2]]
        elif cmd[0] == "snd":
            _("Playing sound:", register[cmd[1]])
            last_sound = register[cmd[1]]
        elif cmd[0] == "add":
            register[cmd[1]] += cmd[2] if type(cmd[2]) == int else register[cmd[2]]
        elif cmd[0] == "mul":
            register[cmd[1]] *= cmd[2] if type(cmd[2]) == int else register[cmd[2]]
        elif cmd[0] == "mod":
            register[cmd[1]] %= cmd[2] if type(cmd[2]) == int else register[cmd[2]]
        elif cmd[0] == "rcv":
            val = cmd[1] if type(cmd[1]) == int else register[cmd[1]]
            if val != 0:
                _("Recovering sound:", last_sound)
                return last_sound
        elif cmd[0] == "jgz":
            val = cmd[1] if type(cmd[1]) == int else register[cmd[1]]
            if val > 0:
                i += cmd[2] - 1
        i += 1


def part_1(source):
    program = prepare(source)
    return duet(program)


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2""")

    def test_example_data_part_1(self):
        self.assertEqual(4, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(1187, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
