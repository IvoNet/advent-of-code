#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
               w               x                   y                     z
  0-----------------------------------------------------------------------------------------------
  inp w    -->   w[1-9]                                                                 <- always a positive number between 1 and 9 
  mul x 0  -->                   0
  add x z  -->                   z
  mod x 26 -->                  x%26
  div z 1  -->                                                             z
  add x 13 -->                 (x%26) + 13
  eql x w  -->                   0                                                       why 0? -> x min = 13 and w max = 9 so x = 0
  eql x 0  -->                   1
  mul y 0  -->                                        0
  add y 25 -->                                        25
  mul y x  -->                                        25
  add y 1  -->                                        26
  mul z y  -->                                                             26z
  mul y 0  -->                                        0
> add y w  -->                                        w
  add y 13 -->                                        w + 13
  mul y x  -->                                        w + 13 * 1
  add z y  -->                                                             26z + w + 13 -> 26z = 13 + 26 -> 26z = 39 -> z = 39 % 26 != 0
  1--------------w---------------x--------------------y---------------------z-------------------------
  inp w1   --> w[1-9]                                                      26z + w + 13
  mul x 0  -->                   0
  add x z  -->                   z
  mod x 26 -->                   x%26
  div z 1  -->                                                              z
  add x 11 -->                   x%26 + 11
  eql x w  -->                     0
  eql x 0  -->                     1
  mul y 0  -->                                        0
  add y 25 -->                                        25
  mul y x  -->                                        25
  add y 1  -->                                        26
  mul z y  -->                                                              26z -> 26(26z + w + 13)
  mul y 0  -->                                        0
  add y w  -->                                        w
> add y 10 -->                                        w + 10
  mul y x  -->                                        w + 10
  add z y  -->                                                              26(26z + w + 13) + w + 10
  2---------------w---------------x--------------------y--------------------z-------------------------
  inp w         w[1-9]                                                     26(26z + w + 13) + w + 10
  mul x 0  -->                    0
  add x z  -->                    z
  mod x 26 -->                    z%26
  div z 1  -->                                                              z
  add x 15 -->                    z%26 + 15
  eql x w  -->                    0
  eql x 0  -->                    1
  mul y 0  -->                                        0
  add y 25 -->                                        25
  mul y x  -->                                        25
  add y 1  -->                                        26
  mul z y  -->                                                              26z
  mul y 0  -->                                        0
  add y w  -->                                        w
  add y 5  -->                                        w+5
  mul y x  -->                                        w+5
  add z y  -->                                                              26z + w + 5
  3-----------------w-------------x-------------------y---------------------z-------------------------
  inp w            w[1-9]
  mul x 0  -->                    0
  add x z  -->                    z
  mod x 26 -->                    z%26
  div z 26 -->                                                              z // 26 round down
  add x -11-->                    z%26 - 11
  eql x w  -->                    1 or 0
  eql x 0  -->                    0 or 1
  mul y 0  -->                                        0
  add y 25 -->                                        25
  mul y x  -->                                        0 or 25
  add y 1  -->                                        1 or 26
  mul z y  -->                                                            z // 26 or 26(z // 26)
  mul y 0  -->                                        0
  add y w  -->                                        w
  add y 14 -->                                        w + 14
  mul y x  -->                                        0 or w + 14
  add z y  -->                                                             z // 26 or 26(z // 26) + w + 14

Looking further we see only these types of calculations

2 types of caclulations
7 of the one and 7 of the other!

Identified by either 'div z 26' or 'div z 1'

type 1      |    type 2
-----------------------------------------
'div z 1'   |    'div z 26'
26z+w+?     |    z // 26 or 26(z//26+w+?)

type 1 increases z about 26 times (huge increase)
type 2 decreases z about 26 times if we have the left calc and stays roughly the same of we have the right one
7 huge increases and 7 possible decreases or samesies
we need the round down! as the other increases every time! so the left one of type 2 is needed as that decreases a lot
and z needs to be zero at the end
how do we guarantee a decrease? that happens in type 2 calculations and only if
the (z%26)-X == w happends

Intermezzo / summerize:
- z is maintained throughout the whole run
- z is always modified
- type 1: z = 26z + w + ?
- type 2: z = z // 26 
The question is in what conditions do we get z to be zero?
Conditions:
e.g (my first input that was different)
(z % 26) - 11 == w
so in this case we can actually calculate what the value of z must be! nice so in 7 of the cases we know!
the other we just have to try :-) a lot less tries thatn 9**14 
we only need to try 9**7 times which is about 5 milion times very nice!

We need the highest value so we need to count down from 9999999 to 9999998 etc

For type 1 we need the Y value
for type 2 the a X value

if every 4th command is 
  - 'div z 1'  -> Type 1
  - 'div z 26' -> Type 2
  
if type 1 then we need the Y of the set of instructions (15th instruction)
if type 2 then we need the x of the instruction after the 'div z 26' (the negative or zero number) 

"""

import sys
import unittest
from itertools import product
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

ADD_X_POS = 5
ADD_Y_POS = 15

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)

class Alu:

    def __init__(self, source) -> None:
        self.assembly = source
        self.type_1 = [None] * 14
        self.type_2 = [None] * 14

        for i in range(14):
            if source[i * 18 + 4] == 'div z 1':
                self.type_1[i] = ints(source[i * 18 + ADD_Y_POS])[0]
            else:  # 'div z 26'
                self.type_2[i] = ints(source[i * 18 + ADD_X_POS])[0]
        _("Type_1:", self.type_1)
        _("Type_2:", self.type_2)

    def __correct(self, digits):
        z = 0
        res = [0] * 14
        idx = 0

        for i in range(14):
            inc = self.type_1[i]
            req = self.type_2[i]

            if inc is not None:  # type 1 calc
                z = z * 26 + digits[idx] + inc
                res[i] = digits[idx]
                idx += 1
            else:  # type 2 calc
                res[i] = (z % 26) + req
                z //= 26
                if not (1 <= res[i] <= 9):
                    return False
        return res

    def __monad(self, all_digits):
        for i, digits in enumerate(all_digits):
            result = self.__correct(digits)
            if result:
                result = "".join([str(i) for i in result])
                _(f"Found result {result} in {i} tries")
                return result

    def highest_monad(self):
        return self.__monad(product(range(9, 0, -1), repeat=7))

    def lowest_monad(self):
        return self.__monad(product(range(1, 10), repeat=7))

def part_1(source):
    return Alu(source).highest_monad()


def part_2(source):
    return Alu(source).lowest_monad()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")

    def test_part_1(self):
        self.assertEqual("12934998949199", part_1(self.source))

    def test_part_2(self):
        self.assertEqual("11711691612189", part_2(self.source))


if __name__ == '__main__':
    unittest.main()
