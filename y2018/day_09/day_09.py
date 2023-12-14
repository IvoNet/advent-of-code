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
from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import count
from pathlib import Path
from typing import Optional

from ivonet.cdll import CircularDoublyLinkedList
from ivonet.files import read_data
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def marble_game(players=403, last_marble=71920):
    """Works but in the higher numbers becomes very slow
    """
    board = CircularDoublyLinkedList()
    board.append(0)
    score = defaultdict(int)
    for m in count(1):
        player = (m - 1) % players + 1
        if m % 23 == 0:
            score[player] += m
            board.step_left(7)
            score[player] += board.get()
            board.remove(board.current())
        else:
            board.step_right(1)
            board.insert_after_current(m)
            board.next()
        if m == last_marble:
            break
        if DEBUG:
            print(board)
    return score


@dataclass
class Marble:
    value: int
    before: Optional[Marble] = None
    after: Optional[Marble] = None


def marble_game_v2(players=403, marbles=71920):
    scores = defaultdict(int)
    current = Marble(0)
    current.before = current
    current.after = current
    for m in range(1, marbles + 1):
        player = (m - 1) % players + 1
        if m % 23 == 0:
            scores[player] += m
            for _ in range(7):
                current = current.before
            before = current.before
            after = current.after
            scores[player] += current.value
            before.after = after
            after.before = before
            current = after
        else:
            before = current.after
            after = before.after
            new = Marble(m, before, after)
            before.after = new
            after.before = new
            current = new
    return scores


def marble_game_v3(players=403, marbles=71920):
    """Best performing for now
    deque is effective as we can rotate.
    If you look at the example the current is effectively always the last -1
    """
    board = deque([0])
    scores = defaultdict(int)
    for m in rangei(1, marbles):
        player = (m - 1) % players + 1
        if m % 23 == 0:
            board.rotate(7)
            scores[player] += board.pop() + m
            board.rotate(-1)
        else:
            board.rotate(-1)
            board.append(m)
        if DEBUG:
            print(player, list(board))
    return scores


def part_1(source):
    players, marble = ints(source)
    score = marble_game_v2(players, marble)
    _(score)
    return max(score.values())


def part_2(source):
    players, marble = ints(source)
    score = marble_game_v3(players, marble * 100)
    return max(score.values())


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_example_1_part_1(self):
        self.assertEqual(32, max(marble_game(9, 25).values()))

    def test_example_v1_2_part_1(self):
        self.assertEqual(8317, max(marble_game(10, 1618).values()))

    def test_example_v1_3_part_1(self):
        self.assertEqual(146373, max(marble_game(13, 7999).values()))

    @unittest.SkipTest  # Don't try this one.... takes forever but does work :-)
    def test_example_v1_3_part_1(self):
        self.assertEqual(3668541094, max(marble_game(403, 7192000).values()))

    def test_example_v1_v2_1_part_1(self):
        self.assertEqual(32, max(marble_game_v2(9, 25).values()))

    def test_example_v2_2_part_1(self):
        self.assertEqual(8317, max(marble_game_v2(10, 1618).values()))

    def test_example_v2_3_part_1(self):
        self.assertEqual(146373, max(marble_game_v2(13, 7999).values()))

    @unittest.SkipTest  # works but a takes about 11 seconds... v3 is better
    def test_example_v2_4_part_2(self):
        self.assertEqual(3668541094, max(marble_game_v2(403, 7192000).values()))

    def test_example_v3_1_part_1(self):
        self.assertEqual(32, max(marble_game_v3(9, 25).values()))

    def test_example_v3_2_part_1(self):
        self.assertEqual(8317, max(marble_game_v3(10, 1618).values()))

    def test_example_v3_3_part_1(self):
        self.assertEqual(146373, max(marble_game_v3(13, 7999).values()))

    @unittest.SkipTest  # Already done in the official part_2 test
    def test_example_v3_4_part_2(self):
        self.assertEqual(3668541094, max(marble_game_v3(403, 7192000).values()))

    def test_part_1(self):
        self.assertEqual(439089, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(3668541094, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
