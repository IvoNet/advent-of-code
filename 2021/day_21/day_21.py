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


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    players = {}
    for line in source:
        player, start = ints(line)
        players[player] = Player(start, 0)
    return players


@dataclass
class Player:
    position: int
    score: int = 0


def play(player, roll):
    player.position = (player.position - 1 + roll) % 10 + 1
    player.score += player.position


def deterministic_die():
    while True:
        for roll in range(1, 101):
            yield roll


def three_sided_die():
    while True:
        for roll in range(1, 4):
            yield roll


def part_1(players):
    print()
    _("Starting players:", players)
    dice = deterministic_die()
    throws = 0
    flip = True
    while True:
        throws += 3
        if flip:
            play(players[1], next(dice) + next(dice) + next(dice))
        else:
            play(players[2], next(dice) + next(dice) + next(dice))
        flip = not flip
        _(throws, players)
        if players[1].score >= 1000:
            return players[2].score * throws
        if players[2].score >= 1000:
            return players[1].score * throws


class State(NamedTuple):
    players: dict[Player]
    next: int


def part_2(players):
    """


    """
    state: dict

    return 0


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = parse(read_rows(f"day_{day.zfill(2)}.input"))
        self.test_source = parse(read_rows("""Player 1 starting position: 4
Player 2 starting position: 8"""))

    def test_example_data_part_1(self):
        self.assertEqual(739785, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(597600, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
