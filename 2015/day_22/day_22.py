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

from ivonet.collection import PriorityQueue
from ivonet.files import read_rows
from ivonet.iter import ints

RECHARGE_COST = 229
POISON_COST = 173
SHIELD_COST = 113
DRAIN_DAMAGE = 2
DRAIN_HEALING = 2
DRAIN_COST = 73
MAGIC_MISSILE_DAMAGE = 4
MAGIC_MISSILE_COST = 53

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


@dataclass
class Player:
    mana: int = 500
    hp: int = 50
    shield_timer: int = 0
    poison_timer: int = 0
    recharge_timer: int = 0
    armor: int = 0

    def copy(self):
        return Player(self.mana, self.hp, self.shield_timer, self.poison_timer, self.recharge_timer, self.armor)

    def __lt__(self, other):
        return True


@dataclass
class Enemy:
    """NOTE! put here your own input"""
    damage: int = 9
    hp: int = 58

    def copy(self):
        return Enemy(self.damage, self.hp)

    def __lt__(self, other):
        return True


class Move(NamedTuple):
    mana_spent: int
    player: Player
    enemy: Enemy


def play(hard_mode=False):
    pq: PriorityQueue[Move] = PriorityQueue()
    pq.push(Move(0, Player(), Enemy()))
    while True:
        mana_spent, player, enemy = pq.pop()
        player: Player = player.copy()

        if hard_mode:
            player.hp -= 1
            if player.hp <= 0:
                continue

        enemy: Enemy = enemy.copy()

        def apply_effects(player: Player, enemy: Enemy) -> bool:
            if player.shield_timer > 0:
                player.shield_timer -= 1
                player.armor = 7
            if player.poison_timer > 0:
                player.poison_timer -= 1
                enemy.hp -= 3
            if player.recharge_timer > 0:
                player.recharge_timer -= 1
                player.mana += 101
            if enemy.hp <= 0:
                return True
            return False

        if apply_effects(player, enemy):
            return mana_spent

        # Magic Missile
        if player.mana >= MAGIC_MISSILE_COST:
            new_mana_spent = mana_spent + MAGIC_MISSILE_COST
            new_player = player.copy()
            new_player.mana -= MAGIC_MISSILE_COST
            new_player.armor = 0
            new_enemy = enemy.copy()
            new_enemy.hp -= MAGIC_MISSILE_DAMAGE
            if apply_effects(new_player, new_enemy):
                return new_mana_spent
            # reverse play (enemy against player)
            new_player.hp -= max(enemy.damage - player.armor, 1)
            if new_player.hp > 0:
                pq.push((new_mana_spent, new_player, new_enemy))

        # Drain
        if player.mana >= DRAIN_COST:
            new_mana_spent = mana_spent + DRAIN_COST
            new_player = player.copy()
            new_player.mana -= DRAIN_COST
            new_player.hp += DRAIN_HEALING
            new_player.armor = 0
            new_enemy = enemy.copy()
            new_enemy.hp -= DRAIN_DAMAGE
            if apply_effects(new_player, new_enemy):
                return new_mana_spent
            new_player.hp -= max(enemy.damage - player.armor, 1)
            if new_player.hp > 0:
                pq.push((new_mana_spent, new_player, new_enemy))

        # Shield
        if player.mana >= SHIELD_COST and player.shield_timer == 0:
            new_mana_spent = mana_spent + SHIELD_COST
            new_player = player.copy()
            new_player.mana -= SHIELD_COST
            new_player.shield_timer = 6
            new_player.armor = 0
            new_enemy = enemy.copy()
            if apply_effects(new_player, new_enemy):
                return new_mana_spent
            new_player.hp -= max(enemy.damage - player.armor, 1)
            if new_player.hp > 0:
                pq.push((new_mana_spent, new_player, new_enemy))

        # Poison
        if player.mana >= POISON_COST and player.poison_timer == 0:
            new_mana_spent = mana_spent + POISON_COST
            new_player = player.copy()
            new_player.mana -= POISON_COST
            new_player.poison_timer = 6
            new_player.armor = 0
            new_enemy = enemy.copy()
            if apply_effects(new_player, new_enemy):
                return new_mana_spent
            new_player.hp -= max(enemy.damage - player.armor, 1)
            if new_player.hp > 0:
                pq.push((new_mana_spent, new_player, new_enemy))

        # Recharge
        if player.mana >= RECHARGE_COST and player.recharge_timer == 0:
            new_mana_spent = mana_spent + RECHARGE_COST
            new_player = player.copy()
            new_player.mana -= RECHARGE_COST
            new_player.recharge_timer = 5
            new_player.armor = 0
            new_enemy = enemy.copy()
            if apply_effects(new_player, new_enemy):
                return new_mana_spent
            new_player.hp -= max(enemy.damage - player.armor, 1)
            if new_player.hp > 0:
                pq.push((new_mana_spent, new_player, new_enemy))


def part_1(source):
    return play()


def part_2(source):
    return play(hard_mode=True)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual(1269, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(1309, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
