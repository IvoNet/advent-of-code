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
import unittest
from pathlib import Path

import pyperclip
from z3 import *
from ivonet.decorators import debug
from ivonet.decorators import timer
from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Machine:
    ON = "#"
    OFF = "."

    def __init__(self, data: str) -> None:
        self.data = data
        self.indicator_lights: list[bool] = []
        self.light_diagram: list[list[bool]] = []
        self.buttons: list[list[int]] = []
        self.joltages: list[int] = []

        self.__parse()

    def state(self):
        return self.state

    def __parse(self):
        indicator_lights, rest = self.data.split("]")
        indicator_lights = indicator_lights.replace("[", "")
        self.indicator_lights = [True if x == self.ON else False for x in indicator_lights]
        buttons, rest = rest.strip().split("{")
        buttons = buttons.split("(")
        self.buttons = [ints(x) for x in buttons if x]
        self.joltages = ints(rest.strip())
        self.joltages_state = [0] * len(self.joltages) # +1 for every indexed press of button

    def __repr__(self):
        return f"Machine(indicator_lights: [{''.join([self.ON if x else self.OFF for x in self.indicator_lights])}], buttons: {str(self.buttons):}, joltages: {str(self.joltages)}] )"

    def match_state_bfs(self):
        from ivonet.search import bfs

        def goal_test(state: list[bool]) -> bool:
            return state == self.indicator_lights

        def successors(state: list[bool]) -> list[list[bool]]:
            result = []
            for button in self.buttons:
                new_state = state[:]
                for index in button:
                    new_state[index] = not new_state[index]
                result.append(new_state)
            return result

        initial_state = [False] * len(self.indicator_lights)
        result_node = bfs(initial_state, goal_test, successors)
        if result_node:
            path = []
            node = result_node
            while node:
                path.append(node.state)
                node = node.parent
            path.reverse()
            return path
        return []

    def part_1(self):
        path = self.match_state_bfs()
        return len(path) - 1

    def match_joltages_bfs(self):
        """Bfs search for matching the joltages_state to the joltages using the buttons presses.
        every button press increases the joltages_state by one at the indexes defined by the button.
        deprecated in favor of z3 solver as this one is much too slow for larger inputs.
        """
        from ivonet.search import bfs

        def goal_test(state: list[int]) -> bool:
            return state == self.joltages

        def successors(state: list[int]) -> list[list[int]]:
            result = []
            for button in self.buttons:
                new_state = state[:]
                for index in button:
                    new_state[index] += 1
                result.append(new_state)
            return result

        initial_state = [0] * len(self.joltages)
        result_node = bfs(initial_state, goal_test, successors)
        p(result_node)
        if result_node:
            path = []
            node = result_node
            while node:
                path.append(node.state)
                node = node.parent
            path.reverse()
            return path
        return []


    def match_joltages_z3(self):
        """Z3 solver for finding the minimum number of button presses to match the joltages."""
        num_buttons = len(self.buttons)
        counts = [Int(f'c{i}') for i in range(num_buttons)]
        opt = Optimize()
        for c in counts:
            opt.add(c >= 0)
        for j in range(len(self.joltages)):
            opt.add(Sum([counts[i] for i, button in enumerate(self.buttons) if j in button]) == self.joltages[j])
        opt.minimize(Sum(counts))
        if opt.check() == sat:
            model = opt.model()
            total = sum(model[c].as_long() for c in counts)
            return total
        else:
            return None

    def part_2(self):
        return self.match_joltages_z3()



@debug
@timer
def part_1(source) -> int | None:
    machines = [Machine(line) for line in source]
    answer = sum(machine.part_1() for machine in machines)
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    machines = [Machine(line) for line in source]
    answer = sum(machine.part_2() for machine in machines)
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(7, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(550, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(33, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(20042, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")


if __name__ == '__main__':
    unittest.main()
