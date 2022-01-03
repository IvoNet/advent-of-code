#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints, rotate, zip_list

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Tcds:
    """tiny-code-displaying-screen"""

    def __init__(self) -> None:
        self.display = [
            list("00000000000000000000000000000000000000000000000000"),
            list("00000000000000000000000000000000000000000000000000"),
            list("00000000000000000000000000000000000000000000000000"),
            list("00000000000000000000000000000000000000000000000000"),
            list("00000000000000000000000000000000000000000000000000"),
            list("00000000000000000000000000000000000000000000000000"),
        ]

    def __flip(self):
        """flips the list of list so that former rows are now cols and vise versa
        This makes manipulating a column easier as it will be contained in its own
        list. Useful for the col rotations function
        """
        self.display = zip_list(self.display)

    def rect(self, width, height):
        ww = width if width <= len(self.display[0]) else len(self.display[0])
        hh = height if height <= len(self.display) else len(self.display)
        for h in range(hh):
            for w in range(ww):
                self.display[h][w] = "1"

    def rotate_col(self, column, by):
        self.__flip()
        col = rotate(self.display[column], by)
        self.display[column] = col
        self.__flip()

    def rotate_row(self, row, by):
        r = rotate(self.display[row % len(self.display)], by)
        self.display[row % len(self.display)] = r

    def __str__(self) -> str:
        ret = ""
        for row in self.display:
            ret += "".join(row)
            ret += "\n"
        return ret

    def letters(self):
        return str(self).replace("0", " ").replace("1", "#")

    def lit(self):
        total = 0
        for row in self.display:
            for c in row:
                total += 1 if c == "1" else 0
        return total


def part_1(source):
    tcds = Tcds()
    for instruction in source:
        left, right = ints(instruction)
        if "rect" in instruction:
            tcds.rect(left, right)
        elif "rotate row" in instruction:
            tcds.rotate_row(left, right)
        elif "rotate column" in instruction:
            tcds.rotate_col(left, right)
        else:
            raise ValueError("Should not be here")
    return tcds


def part_2(source):
    letters = part_1(source).letters()
    _(letters)
    return letters


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(str(Path(__file__).parent.joinpath(f"day_{day.zfill(2)}.input")))

    def test_part_1(self):
        self.assertEqual(116, part_1(self.source).lit())

    def test_part_2(self):
        self.assertEqual("""#  # ###   ##    ## #### #    ###   ##  #### #### 
#  # #  # #  #    # #    #    #  # #  # #       # 
#  # #  # #  #    # ###  #    ###  #    ###    #  
#  # ###  #  #    # #    #    #  # #    #     #   
#  # #    #  # #  # #    #    #  # #  # #    #    
 ##  #     ##   ##  #    #### ###   ##  #### #### 
""", part_2(self.source))


if __name__ == '__main__':
    unittest.main()
