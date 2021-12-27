#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from ivonet.calc import prod
from ivonet.files import read_rows
from ivonet.iter import ints, four_way_split

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Ingredient(NamedTuple):
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def parse(source) -> list[Ingredient]:
    ret = []
    for line in source:
        ret.append(Ingredient(*ints(line)))
    return ret


def calc(ingredients: list[Ingredient], spoons: tuple) -> tuple[int, int]:
    score = defaultdict(int)
    calories = 0
    for i, ingredient in enumerate(ingredients):
        score["c"] += spoons[i] * ingredient.capacity
        score["d"] += spoons[i] * ingredient.durability
        score["f"] += spoons[i] * ingredient.flavor
        score["t"] += spoons[i] * ingredient.texture
        calories += spoons[i] * ingredient.calories
    for v in score.values():
        if v < 0:
            return 0, 0
    total_score = int(prod(list(score.values())))
    if calories == 500:
        _(spoons, total_score)
    return total_score, calories


def part_1(source):
    ingredients = parse(source)
    score = []
    for spoons in four_way_split(100, first=0, inclusive=True):
        score.append(calc(ingredients, spoons)[0])

    return max(score)


def part_2(source):
    ingredients = parse(source)
    score = []
    for spoons in four_way_split(100, first=0, inclusive=True):
        total, calories = calc(ingredients, spoons)
        if total > 0 and calories == 500:
            score.append(total)
    return max(score)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3""")

    def test_example_data_part_1(self):
        self.assertEqual(62842880, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(18965440, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(57600000, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(15862900, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
