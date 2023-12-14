#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import sys
import unittest
from pathlib import Path

from ivonet.calc import prod
from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


# Global monkey state. Dirty but I do not care :-)
monkeys = {}


class Monkey(object):

    def __init__(self, data: str) -> None:
        super().__init__()
        self.operations = {
            "+": lambda x, y: int(x) + int(y),
            "*": lambda x, y: int(x) * int(y),
        }
        self.round = 1
        self.inspections = 0
        instructions = data.split("\n")
        self.name = instructions[0]
        self.items = ints(instructions[1])
        new = instructions[2].split(" = ")[1]
        self.operation = new.split(" ")
        self.test = ints(instructions[3])[0]
        self.yes = ints(instructions[4])[0]
        self.no = ints(instructions[5])[0]

    def play_round(self, part_2_modulo=None) -> None:
        for old in self.items[:]:
            self.items.pop(0)
            self.inspections += 1
            right = self.operation[2]
            if right == "old":
                worry_level = self.operations[self.operation[1]](old, old)
            else:
                worry_level = self.operations[self.operation[1]](old, self.operation[2])
            if not part_2_modulo:
                worry_level = worry_level // 3
            else:
                worry_level = worry_level % part_2_modulo
            if worry_level % self.test == 0:
                monkeys[self.yes].append(worry_level)
            else:
                monkeys[self.no].append(worry_level)
        self.round += 1

    def append(self, item):
        self.items.append(item)

    def __str__(self) -> str:
        return f"{self.name} [inspections: {self.inspections:<6} - worry_levels: {len(self.items):<3} - # items: {self.items}]"

    def __repr__(self) -> str:
        return self.__str__()


def parse_monkeys(source):
    """Parse the monkeys from the source data.
    The reason for the part 2 modulo is that it reduces the enormous numbers you would otherwise get.
    by multiplying the test numbers of all the monkeys together you get the modulo you can apply to all the
    worry levels and still adhere to the same rules as before without the huge numbers.
    e.g. of the example data:
    modulo = 23 * 19 * 13 * 17 = 96577
    The remainder of the worry level divided by 96577 adheres to the same rules as before,
    because that is how math works :-)
    Because you only need to count the number of inspections you can do this modulo without losing needed data.
    """
    part_2_modulo = 1
    for i, ape in enumerate(source):
        monkeys[i] = Monkey(ape)
        part_2_modulo *= monkeys[i].test
    return part_2_modulo


def play_rounds(rounds, part_2_modulo=None):
    """Play the rounds of the game."""
    for i, __ in enumerate(range(rounds), 1):
        for monkey in monkeys.values():
            monkey.play_round(part_2_modulo)
        if DEBUG and (i <= 20 or i % 1000 == 0):
            _(f"Round: {i}:\n-" + "\n-".join(str(x) for x in monkeys.values()))

    return prod(x.inspections for x in sorted(monkeys.values(), key=lambda x: x.inspections)[-2:])


def part_1(source, rounds=20):
    parse_monkeys(source)
    return play_rounds(rounds)


def part_2(source, rounds=10000):
    modulo = parse_monkeys(source)
    return play_rounds(rounds, modulo)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input").split("\n\n")
        self.test_source = read_data("""Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""").split("\n\n")

    def test_example_data_part_1(self):
        self.assertEqual(10605, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(88208, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(2713310158, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(21115867968, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
