#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Some stuff I learned about complex numbers and why it is so useful when working with these kinds of puzzles
https://realpython.com/python-complex-numbers/

is very cool stuff there
It seems that I can "calculate" direction changes when using complex numbers!
My student math days are a while ago so lets start trying stuff out :-)
"""

import os
import sys
import unittest
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True

Point = complex
GAME_LOOP: bool = True


@dataclass
class Cart:
    loc: complex
    direction: Direction


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def rotate(z: complex, degrees: float) -> complex:
    """https://realpython.com/python-complex-numbers/#multiplication"""
    return z * 1j ** (degrees / 90)


@dataclass
class Cart:
    pos: complex
    dir: complex
    step: int = 0


class CardTrackSystem:
    """cart-and-track system
    Some rules translated to actions
    - standard moves
      - 0 turn left
      - 1 straight
      - 2 turn right (3 steps so % 3 == 0)
    - No reason to separate the carts from the system as we are determining the directions
    """

    def __init__(self, source) -> None:
        self.directions = {'>': 1, '<': -1, '^': -1j, 'v': 1j}
        self.tracks = {x + y * 1j: value for y, row in enumerate(source) for x, value in enumerate(row)}
        self.carts = sorted([Cart(pos, self.directions[d]) for pos, d in self.tracks.items() if d in self.directions],
                            key=lambda cart: cart.pos.imag)

    def __move(self, cart: Cart):
        """The real work is done here :-) Moving the carts
        - the first iteration of all the cats it will return itself.
          it will then skip all the ifs because none are true and then go to the next position and as we already know
          our direction that is just fine
        - the next move of all a cart it can encounter a few things but the only three of note are +/\ as they have an
          effect on direction.
        - so if it encounters a |^-v<> just go ahaid in the direction you were going already
        - when encountering a + we will:
          - first action (step == 0): turn left
          - second action (step == 1): do nothing as we were already going in that direction
          - third action (step == 2): tirn right
        - when we encounter a \ or / sign we need to turn in the right directions based on the direction
        - and just do a step
        """
        track = self.tracks[cart.pos]
        if track == "+":
            if cart.step == 0:  # going left
                cart.dir = rotate(cart.dir, -90)
            elif cart.step == 2:  # going right
                cart.dir = rotate(cart.dir, 90)
            cart.step = (cart.step + 1) % 3
        elif track in "\\":
            cart.dir = rotate(cart.dir, -90 if cart.dir.imag else 90)
        elif track in "/":
            cart.dir = rotate(cart.dir, -90 if cart.dir.real else 90)
        cart.pos += cart.dir

    def first_collision(self):
        """Find the first collision"""
        while True:
            for cart in self.carts:
                self.__move(cart)
                if any(c for c in self.carts if c != cart and c.pos == cart.pos):
                    return f"{int(cart.pos.real)},{int(cart.pos.imag)}"

    def last_collision(self):
        """Simulate until only one card left then tell us where it is
        - as we are removing the crashed cards we need to re sort them after every remove
        - the order might have changed.
        - Sort based on the row they are on as top rows move first
        """
        carts = deepcopy(self.carts)
        while True:
            if len(carts) == 1:
                return f"{int(carts[0].pos.real)},{int(carts[0].pos.imag)}"
            carts = sorted(carts, key=lambda cart: cart.pos.imag)
            for cart in carts:
                self.__move(cart)
                crashed = [c for c in carts if c != cart and c.pos == cart.pos]
                if crashed:
                    carts = [c for c in carts if c != cart and c != crashed[0]]


def part_1(source):
    return CardTrackSystem(source).first_collision()


def part_2(source):
    return CardTrackSystem(source).last_collision()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input", raw=True)
        self.test_source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test.input", raw=True)
        self.test_source2 = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test_2.input", raw=True)

    def test_example_data_part_1(self):
        self.assertEqual("7,3", part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual("76,108", part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual("6,4", part_2(self.test_source2))

    def test_part_2(self):
        self.assertEqual("2,84", part_2(self.source))


if __name__ == '__main__':
    unittest.main()
