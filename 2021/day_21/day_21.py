#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from itertools import product
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


class Player(NamedTuple):
    position: int
    score: int


class State(NamedTuple):
    players: Tuple[Player, Player]
    next_player: 0


def play(player: player, roll: int) -> Player:
    npos = (player.position - 1 + roll) % 10 + 1
    nscore = player.score + npos
    return Player(npos, nscore)


def deterministic_die():
    while True:
        for roll in range(1, 101):
            yield roll


def quantum_die():
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
            players[1] = play(players[1], next(dice) + next(dice) + next(dice))
        else:
            players[2] = play(players[2], next(dice) + next(dice) + next(dice))
        flip = not flip
        _(throws, players)
        if players[1].score >= 1000:
            return players[2].score * throws
        if players[2].score >= 1000:
            return players[1].score * throws


def add(tuples):
    """Gets all the individual results of the same "key" per universe
    and adds the collums as they represent player 0 and 1
    so left wins versus right wins
    """
    return tuple(sum(column) for column in zip(*tuples))


def dirac_dice(players: tuple[Player, Player], player: int, cache) -> tuple[int, int]:  # left player 0, right player 1
    if players[0].score >= 21:
        return 1, 0  # player 0 wins (represented by left)
    if players[1].score >= 21:
        return 0, 1

    key = (players, player)
    if key in cache:
        return cache[key]
    results: tuple[int, int] = []
    for quantum_roll in product(range(1, 4), repeat=3):
        new_pos = (players[player].position - 1 + sum(quantum_roll)) % 10 + 1
        new_score = players[player].score + new_pos
        new_players: tuple[Player, Player] = None
        if player == 0:
            new_players = (Player(new_pos, new_score), players[1])
        else:  # 1
            new_players = (players[0], Player(new_pos, new_score))
        results.append(dirac_dice(new_players, (player + 1) % 2, cache))
        cache[key] = add(results)
    # _(results)
    return cache[key]


def part_2(players):
    """
    universe 0:
    2 players with a state
    - p1(4, 0)
    - p2(8, 0)
    turn 1: three new universes for every face of the die (1,2,3)
    u1:
    p1(4,0)

    die with 3 faces deterministicly thrown hmmm
    throws where sum =
    - 3 -> 111
    - 4 -> 112, 121, 211
    - 5 -> 113, 131, 311, 221, 212, 122
    - 6 -> 222, 123, 312, 231, 132, 213, 321
    - 7 -> 223, 322, 232, 331, 313, 133
    - 8 -> 332, 323, 233
    - 9 -> 333
    these are all possibilities! per 3 throws
    this means 27 universes per "turn" of three throws
    does also mean that:
    sum of throw  |  # of universes
    --------------------------------
      3           |  1
      4           |  3
      5           |  6
      6           |  7
      7           |  6
      8           |  3
      9           |  1
    --------------------------------
      Total       |  27

    so in if the dice is thrown with 1 in it it can have
    4 outcomes

    this is the same as:
    product(range(1, 4), repeat=3)

    while playing we need a way to keep track of what has already been played.
    Done is done right

    so if a score of a play in the product goes over 21 it is done and should be cached or something
    and removed from the player list

    it does not matter which player wins just the amount it wins with (max)

    I feel a recursive function comming up :-)

    """
    # a dict with a key and a total of the left vs right wins
    quantum_cache: dict[tuple[tuple[Player, Player], int], tuple[int, int]] = {}
    return max(dirac_dice(tuple(players.values()), 0, quantum_cache))


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
        self.assertEqual(444356092776315, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(634769613696613, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
