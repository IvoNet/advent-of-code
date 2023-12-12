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
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


def valid(springs: str, parity: tuple[int, ...]):
    """
    check if the springs are valid according to the parity list
    - the numbers in the parity list correspond to groups of "#" in the springs list
    - every group must be separated by at least one . to be a group
    - ? is a wildcard and can be either "#" or "."
    - check if a group is valid by checking if the number of # in the group is equal to the number in the parity list
      and their length is equal to the parity
    """
    broken = [x for x in springs.split(".") if x != ""]
    if len(broken) != len(parity):
        return False
    for i, group in enumerate(broken):
        if len(group) != parity[i]:
            return False
        if group.count("#") != parity[i]:
            return False
    return True


def generate_combinations(s):
    """
    This function generates all possible combinations of a string where "?" can be either "#" or ".".

    It uses a recursive approach to replace each "?" in the string with "#" and ".", generating two new strings.
    This process is repeated until there are no "?" left in the string.
    The function then yields each possible combination.

    Parameters:
    s (str): The input string with "?" placeholders.

    Yields:
    str: The next combination of the input string where "?" has been replaced with "#" or ".".

    NOTE: this is a very slow implementation (not used in the final solution) but illustrates my thinking process
    """
    if '?' not in s:
        yield s
    else:
        yield from generate_combinations(s.replace('?', '#', 1))
        yield from generate_combinations(s.replace('?', '.', 1))


def parse(source):
    """
    parse the source:
    - every line contains springs and a parity list of numbers
    - the two are separated by a space
    """
    for line in source:
        springs, parity = line.split(" ")
        yield springs, tuple(ints(parity))


def multiply_string(s, n, separator):
    return separator.join([s] * n)


def combinations(left, parity):
    stack = [(left, parity)]
    result = 0

    while stack:
        left, parity = stack.pop()

        # Termination case 1: if left is an empty string
        if left == "":
            # If parity is also empty, increment result by 1, else do nothing
            result += 1 if not parity else 0
        elif not parity:
            # If there is a "#" in left, do nothing, else increment result by 1
            result += 0 if "#" in left else 1
        else:
            # If the first character of left is "." or "?"
            if left[0] in ".?":
                # Add the next state to the stack
                stack.append((left[1:], parity))

            # If the first character of left is "#" or "?"
            if left[0] in "#?":
                # If the length of left is greater than or equal to the first integer in parity
                # and there is no "." in the first parity[0] characters of left
                # and the parity[0]th character of left is not "#"
                if len(left) >= parity[0] and "." not in left[:parity[0]] and (
                        parity[0] == len(left) or left[parity[0]] != "#"):
                    # Add the next state to the stack
                    stack.append((left[parity[0] + 1:], parity[1:]))

    return result


def part_1(source):
    answer = 0
    for springs, parity in parse(source):
        count = 0
        for spring in generate_combinations(springs):
            if valid(spring, parity):
                count += 1
        answer += count
    return answer


def part_2(source, times=5):
    answer = 0
    for springs, parity in parse(source):
        s = multiply_string(springs, times, "?")
        p = parity * times
        answer += combinations(s, p)
    return answer


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""")
        self.test_source2 = read_rows("""#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1""")

    def test_example_data_part_1(self):
        self.assertEqual(21, part_1(self.test_source))

    def test_example_data_part_1_valid(self):
        for springs, parity in parse(self.test_source2):
            self.assertEqual(True, valid(springs, parity))
        self.assertEqual(False, valid("###.###", (1, 1, 3)))

    def test_part_1(self):
        self.assertEqual(7173, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(525152, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
