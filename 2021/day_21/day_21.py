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
from ivonet.iter import ints, chunkify

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Player:

    def __init__(self, id, pawn=0, score=0) -> None:
        self.board = list(range(1, 11)) * 100000
        self.id: int = id
        self.pawn: int = pawn
        self.score: int = score

    def walk(self, die: range):
        self.pawn += sum(die)
        self.score += self.board[self.pawn - 1]

    def __repr__(self) -> str:
        return f"Player[{self.id}, pawn=[{self.board[self.pawn]}, score=[{self.score}]"


def parse(source):
    players = {}
    for line in source:
        player, start = ints(line)
        players[player] = Player(player, start, 0)
    return players


def check(player):
    if player.score >= 1000:
        return True
    return False


def next_throw(loops=10000):
    deterministic_die = list(range(1, 101)) * loops
    for chunk in chunkify(deterministic_die, 3):
        yield chunk


def part_1(players):
    print()
    _("Starting players:", players)
    throws = 0
    flip = True
    for dice in next_throw():
        throws += 3
        if flip:
            players[1].walk(dice)
        else:
            players[2].walk(dice)
        flip = not flip
        _(throws, players)
        for player in players:
            if check(players[player]):
                if player == 1:
                    return players[2].score * throws
                return players[1].score + throws


def part_2(players):
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
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
