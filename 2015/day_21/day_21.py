#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


class Item(NamedTuple):
    cost: int
    damage: int
    armor: int


# ITEM       Cost  Damage  Armor
store = """
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5
Damage+1    25     1       0
Damage+2    50     2       0
Damage+3   100     3       0
Defense+1   20     0       1
Defense+2   40     0       2
Defense+3   80     0       3
""".strip().splitlines(keepends=False)

items = [Item(int(cost), int(damage), int(armor)) for name, cost, damage, armor in [x.split() for x in store]]
weaponry = items[:5]
armory = [Item(0, 0, 0)]
armory.extend(items[5:10])
damagery = items[10:13]
defencery = items[13:]

for a in armory.copy():
    for d in defencery.copy():
        armory.append(Item(a.cost + d.cost, 0, a.armor + d.armor))


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


@dataclass
class Player:
    hit_points: int
    damage: int
    armor: int


def play(me, boss) -> bool:
    left = False
    while me.hit_points > 0 and boss.hit_points > 0:
        left = not left
        if left:
            damage = me.armor - boss.damage
            me.hit_points += damage if damage < 0 else -1
            continue
        damage = boss.armor - me.damage
        boss.hit_points += damage if damage < 0 else -1
    return me.hit_points > boss.hit_points



def part_1(source):
    print()
    print(weaponry)
    print(armory)
    print(damagery)
    print(defencery)
    gold = float("inf")
    for weapon in weaponry:
        for armor in armory:
            boss = Player(109, 8, 2)
            me = Player(100, weapon.damage, armor.armor)
            win = play(me, boss)
            if win:
                print("Won:", me, boss)
                print("Weapon:", weapon)
                print("Armor:", armor)
                cost = weapon.cost + armor.cost
                print("Cost", cost)
                if cost < gold:
                    gold = cost
    return gold


def part_2(source):
    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""""")

    def test_part_1(self):
        self.assertEqual(111, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
