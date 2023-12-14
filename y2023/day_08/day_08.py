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
import unittest
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple, Type

import sys

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Node(NamedTuple):
    left: str
    right: str

    def __repr__(self):
        return f"Node(left: {self.left}, right: {self.right})"


def parse_v1(source):
    """
    Parse the source to create a dictionary of nodes and return the instructions and nodes.

    :param source: The source data to parse.
    :return: A tuple containing the instructions and nodes.
    """
    nodes = defaultdict(Type[Node])
    instructions = source[0]
    for line in source[2:]:
        name, targets = line.split(" = ")
        nodes[name] = Node(*(targets[1:-1].split(", ")))
    return instructions, nodes


def parse(source):
    """
    Parse the source to create a dictionary of nodes and return the instructions and nodes.

    :param source: The source data to parse.
    :return: A tuple containing the instructions and nodes.
    """
    nodes = {
        name: Node(left, right)
        for line in source[2:]
        for name, rest in [line.split(" = ")]
        for left, right in [rest[1:-1].split(", ")]
    }
    return source[0], nodes


def gcd(a, b):
    """
    Calculate the greatest common divisor (GCD) of two numbers using
    the Euclidean algorithm.
    https://en.wikipedia.org/wiki/Euclidean_algorithm
    :param a: The first number.
    :param b: The second number.
    :return: The GCD of a and b.
    """
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    """
    Calculate the least common multiple (LCM) of two numbers.
    :param a: The first number.
    :param b: The second number.
    :return: The LCM of a and b.
    """
    return abs(a * b) // gcd(a, b)


def lcm_list(numbers: list[int]):
    """
     Calculate the least common multiple (LCM) of a list of numbers.
     :param numbers: The list of numbers.
     :return: The LCM of the numbers in the list.
     """
    if not numbers:
        return 0
    if len(numbers) == 1:
        return numbers[0]
    result = numbers[0]
    for number in numbers[1:]:
        result = lcm(result, number)
    return result


def rotate(instructions):
    """
    Rotate the instructions one step to the left to make it continues
    """
    return instructions[1:] + instructions[0]
    return instructions[1:] + instructions[0]



def part_1(source):
    """
    Calculate the number of steps it takes to reach a node named 'ZZZ'.
    :param source:
    :return: the answer in number of steps
    """
    instructions, nodes = parse(source)

    current = "AAA"
    steps = 0
    while current != "ZZZ":
        steps += 1
        current = nodes[current].left if instructions[0] == "L" else nodes[current].right
        instructions = rotate(instructions)
    return steps


def part_2(source):
    """
    Calculate the least common multiple of the number of steps it takes for each starting node to reach a node ending with 'Z'.

    :param source: The source data to use for the calculation.
    :return: The least common multiple of the number of steps.
    """
    instructions, nodes = parse(source)

    current_nodes = [name for name in nodes if name.endswith('A')]
    steps = [0 for _ in current_nodes]
    num_steps = 0
    while not all(steps):
        for idx, name in enumerate(current_nodes):
            if name.endswith("Z") and not steps[idx]:
                steps[idx] = num_steps
                if all(steps):
                    return lcm_list(steps)  # can be replaced with math.lcm function
        current_nodes = [nodes[node].left if instructions[0] == "L" else nodes[node].right for node in current_nodes]
        instructions = rotate(instructions)
        num_steps += 1


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""")
        self.test_source2 = read_rows("""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""")

    def test_example_data_part_1(self):
        self.assertEqual(2, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(13019, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(6, part_2(self.test_source2))

    def test_part_2(self):
        self.assertEqual(13524038372771, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
