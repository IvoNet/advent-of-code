#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2023 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import sys
import unittest
from collections import defaultdict
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Hand(object):
    TYPES = {
        (5,): "Five of a kind",
        (4, 1): "Four of a kind",
        (3, 2): "Full House",
        (3, 1, 1): "Three of a kind",
        (2, 2, 1): "Two pair",
        (2, 1, 1, 1): "One pair",
        (1, 1, 1, 1, 1): "High card"
    }

    STRENGTH = {
        (5,): 7,
        (4, 1): 6,
        (3, 2): 5,
        (3, 1, 1): 4,
        (2, 2, 1): 3,
        (2, 1, 1, 1): 2,
        (1, 1, 1, 1, 1): 1
    }

    CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    CARDS_JOKER = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]

    def __init__(self, cards: str, bid: int, joker: bool = False):
        self.joker = joker
        if self.joker:
            self.cmp_cards = self.CARDS_JOKER
        else:
            self.cmp_cards = self.CARDS
        self.cards = cards
        self.bid = bid
        self.type = defaultdict(list)
        self.hand: tuple = ()
        self.parse()

    def parse(self):
        for c in self.cards:
            self.type[c].append(c)
        if self.joker and "J" in self.type:
            self.handle_joker()
        else:
            self.hand = tuple(sorted([len(v) for v in self.type.values()], reverse=True))

    def handle_joker(self):
        joker_count = len(self.type["J"])
        if len(self.type["J"]) >= 4:
            self.hand = (5,)
            return
        del self.type["J"]
        self.hand = tuple(sorted([len(v) for v in self.type.values()], reverse=True))
        self.hand = tuple(sorted([self.hand[0] + joker_count, *self.hand[1:]], reverse=True))

    def __lt__(self, other):
        if not isinstance(other, Hand):
            return False
        if self.STRENGTH[self.hand] == self.STRENGTH[other.hand]:
            for i in range(len(self.cards)):
                if self.cmp_cards.index(self.cards[i]) == self.cmp_cards.index(other.cards[i]):
                    continue
                return self.cmp_cards.index(self.cards[i]) < self.cmp_cards.index(other.cards[i])
        return self.STRENGTH[self.hand] < self.STRENGTH[other.hand]

    def __repr__(self):
        return f"Hand: {self.cards}, bid:{self.bid:5d}, strength: {self.STRENGTH[self.hand]}, type: {self.TYPES[self.hand]:15}"


class CamelCards(object):

    def __init__(self, source, joker: bool = False):
        self.source = source
        self.hands = [Hand(cards, int(bid), joker=joker) for cards, bid in [line.split() for line in source]]
        self.hands.sort()

    def play_1(self):
        answer = 0
        for i, hand in enumerate(self.hands, 1):
            answer += hand.bid * i
            _(f"Rank: {i:4d} {hand}, score: {hand.bid * i:10d}, answer: {answer:10d}")
        return answer


def part_1(source):
    cc = CamelCards(source)
    return cc.play_1()


def part_2(source):
    cc = CamelCards(source, True)
    return cc.play_1()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""")
        self.test_source2 = read_rows("""""")

    def test_example_data_part_1(self):
        self.assertEqual(6440, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(246409899, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(5905, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(244848487, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
