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

import collections
import os
import sys
import unittest
from collections import defaultdict
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def ascii_hash(step: str) -> int:
    """
    Computes a hash value for a given string. The hash value is calculated by iterating over each character in the string,
    adding its ASCII value to a running total, multiplying the total by 17, and then taking the modulus of 256.

    Parameters:
    step (str): The string for which to compute the hash value.

    Returns:
    int: The computed hash value.
    """
    current: int = 0
    for s in step:
        current += ord(s)
        current *= 17
        current %= 256
    return current


def hashmap_procedure(steps: list[str]) -> dict:
    """
    Processes a list of steps to create a dictionary of boxes. Each box is represented by a
    dictionary where the keys are labels and the values are focal lengths.

    Parameters:
    steps (list): A list of strings where each string represents a step. A step can either
    represent a new lens being added to a box or a lens being removed from a box.

    Returns:
    dict: A dictionary where each key-value pair represents a box and its lenses. The keys
    are box indices and the values are dictionaries where the keys are labels and the values
    are focal lengths.
    """
    boxes = defaultdict(dict)
    for step in steps:
        if "-" in step:
            label = step[:-1]
            box_index = ascii_hash(label)
            _("-", label, box_index)
            if label in boxes[box_index]:
                del boxes[box_index][label]
        else:
            label, focal_length = step.split("=")
            box_index = ascii_hash(label)
            _("=", label, box_index, focal_length)
            boxes[box_index][label] = int(focal_length)
    _(boxes)
    return boxes


def parse(source: list[str]) -> list[str]:
    """
    Parses the source list to a list of steps.
    """
    return source[0].strip().split(",")


def part_1(source: list[str]) -> int:
    """
    Computes the sum of the ascii hash values of the steps in the source.

    Parameters:
    source (list[str]): The source list containing the steps.

    Returns:
    int: The sum of the ascii hash values of the steps.
    """
    return sum(ascii_hash(step) for step in parse(source))


def part_2(source: list[str]) -> int:
    """
    Computes the total focal power of the boxes.

    Parameters:
    source (list[str]): The source list containing the steps.

    Returns:
    int: The total focal power of the boxes.
    """
    boxes: dict[int, dict[int, int]] = hashmap_procedure(parse(source))
    total_focal_power = 0
    for box, lenses in boxes.items():
        for index, value in enumerate(lenses.values()):
            total_focal_power += (box + 1) * (index + 1) * value
            _(box, index, value, (box + 1) * index * value)
    return total_focal_power


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        _()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows(f"{os.path.dirname(__file__)}/test_{day.zfill(2)}.input")
        self.test_source2 = read_rows("""""")

    def test_example_data_part_1(self):
        self.assertEqual(52, part_1(["HASH"]))
        self.assertEqual(1320, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(497373, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(145, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(259356, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
