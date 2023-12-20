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
from dataclasses import dataclass
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

collections.Callable = collections.abc.Callable  # type: ignore
sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def p(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


@dataclass
class Pulse:
    origin: str
    destination: str
    pulse: str

    def __repr__(self):
        return f"{self.origin} -{self.pulse}-> {self.destination}"


class Module:
    def __init__(self, name: str, destinations: list):
        if destinations is None:
            self.destinations: list = []
        else:
            self.destinations = destinations
        self.name = name

    def process(self, pulse: Pulse) -> list[Pulse]:
        return []

    def __repr__(self):
        return f"{self.name}[{self.destinations}]"


class FlipFlop(Module):
    def __init__(self, name, destinations: list):
        super().__init__(name, destinations)
        self.on = False

    def process(self, pulse: Pulse) -> list[Pulse]:
        if pulse.pulse == 'high':
            return []
        self.on = not self.on
        sending = 'high' if self.on else 'low'
        return [Pulse(pulse.destination, dest, sending) for dest in self.destinations]


class Conjunction(Module):
    def __init__(self, name, destinations):
        super().__init__(name, destinations)
        self.memory = {}

    def process(self, pulse: Pulse) -> list[Pulse]:
        self.memory[pulse.origin] = pulse.pulse
        if all(state == 'high' for state in self.memory.values()):
            return [Pulse(pulse.destination, dest, 'low') for dest in self.destinations]
        return [Pulse(pulse.destination, dest, 'high') for dest in self.destinations]


class Broadcaster(Module):
    def __init__(self, name, destinations):
        super().__init__(name, destinations)
        self.destinations = destinations

    def process(self, pulse: Pulse) -> list[Pulse]:
        return [Pulse(pulse.destination, dest, pulse.pulse) for dest in self.destinations]


class System(object):
    def __init__(self, source):
        self.source = source
        self.modules = {}
        self.broadcaster = None
        self.parse_config(source)

    def push_button(self):
        lo = 1  # the button itself
        hi = 0
        q = collections.deque(self.broadcaster.process(Pulse('button', 'broadcaster', 'low')))
        p("button -low-> broadcaster")
        while q:
            pulse = q.popleft()
            p(pulse)
            if pulse.pulse == 'low':
                lo += 1
            else:
                hi += 1

            if pulse.destination not in self.modules:
                continue

            module = self.modules[pulse.destination]
            new_pulses = module.process(pulse)
            q.extend(new_pulses)
        return lo, hi

    def simulate(self, num_pushes):
        low_pulses = high_pulses = 0
        for i in range(num_pushes):
            low, high = self.push_button()
            p(f"===>button pushed: {i}, low: {low} high: {high}")
            low_pulses += low
            high_pulses += high
        return low_pulses, high_pulses

    def parse_config(self, source):
        for line in source:
            name, destinations = line.split(' -> ')
            destinations = destinations.split(', ')
            if name == 'broadcaster':
                self.broadcaster = Broadcaster("broadcaster", destinations)
                continue
            typ = name[0]
            name = name[1:].strip()
            if typ == "%":
                self.modules[name] = FlipFlop(name, destinations)
            else:  # typ == "&":
                self.modules[name] = Conjunction(name, destinations)

            # connect the destinations to the conjunctions
            for name, module in self.modules.items():
                for destination in module.destinations:
                    if destination in self.modules and isinstance(self.modules[destination], Conjunction):
                        self.modules[destination].memory[name] = 'low'


def part_1(source: list[str]) -> int | None:
    system = System(source)
    low_pulses, high_pulses = system.simulate(1000)
    p(f"total ======= low: {low_pulses} high: {high_pulses}")
    return low_pulses * high_pulses


def part_2(source: str | list[str]) -> int | None:
    return None


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1a(self) -> None:
        self.assertEqual(32000000, part_1(self.test_source_2))

    def test_example_data_part_1(self) -> None:
        self.assertEqual(11687500, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(731517480, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = os.path.dirname(os.path.realpath(__file__))
        day = f"{str(ints(Path(__file__).name)[0]).zfill(2)}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")
        self.test_source_2 = read_rows("""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""")


if __name__ == '__main__':
    unittest.main()
