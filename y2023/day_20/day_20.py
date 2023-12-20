#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

# noinspection DuplicatedCode
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

from ivonet.calc import lcm_list
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
    """
    A module is a component that can receive a pulse and send pulses to other modules.
    """
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
    """
    A flip-flop is a module that can be switched on and off.

    it only flips on a low pulse and sends the opposite pulse to its destinations.
    on a high pulse it does nothing.
    """
    def __init__(self, name, destinations: list):
        super().__init__(name, destinations)
        self.on = False

    def process(self, pulse: Pulse) -> list[Pulse]:
        if pulse.pulse == 'high':
            return []
        self.on = not self.on
        sending = 'high' if self.on else 'low'
        return [Pulse(pulse.destination, dest, sending) for dest in self.destinations]

    def __repr__(self):
        return f"{self.name}[{self.destinations}]={self.on}"


class Conjunction(Module):
    """
    The Conjunction Module remembers the state of all its received pulses and only sends a low pulse to its
    destinations if all its remembered pulses are high, otherwise it sends a high pulse to its destinations.
    """
    def __init__(self, name, destinations):
        super().__init__(name, destinations)
        self.memory = {}

    def process(self, pulse: Pulse) -> list[Pulse]:
        self.memory[pulse.origin] = pulse.pulse
        if all(state == 'high' for state in self.memory.values()):
            return [Pulse(pulse.destination, dest, 'low') for dest in self.destinations]
        return [Pulse(pulse.destination, dest, 'high') for dest in self.destinations]

    def __repr__(self):
        return f"{self.name}[{self.destinations}]={self.memory}"


class Broadcaster(Module):
    """
    The broadcaster module sends a pulse as received to all its destinations.
    """
    def __init__(self, name, destinations):
        super().__init__(name, destinations)
        self.destinations = destinations

    def process(self, pulse: Pulse) -> list[Pulse]:
        return [Pulse(pulse.destination, dest, pulse.pulse) for dest in self.destinations]


class System(object):
    """
    The system is the brains of the operation. It:
     - reads the configuration
     - creates the modules
     - processes the button pushes
    """
    def __init__(self, source):
        self.source = source
        self.modules = {}
        self.parse_config(source)

    def parse_config(self, source):
        for line in source:
            name, destinations = line.split(' -> ')
            destinations = destinations.split(', ')
            if name == 'broadcaster':
                self.modules[name] = Broadcaster("broadcaster", destinations)
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

    def push_button(self):
        p("====pushing button=====")
        pulses = []
        q = collections.deque([Pulse('button', 'broadcaster', 'low')])
        while q:
            pulse = q.popleft()
            p(pulse)

            pulses.append(pulse.pulse)

            if pulse.destination not in self.modules:
                continue

            module = self.modules[pulse.destination]
            new_pulses = module.process(pulse)
            q.extend(new_pulses)
        return pulses

    def simulate(self, num_pushes=1000):
        pulses = [pulse for _ in range(num_pushes) for pulse in self.push_button()]
        return sum(pulse == 'low' for pulse in pulses), sum(pulse == 'high' for pulse in pulses)

    def rx_flip(self):
        """
        I've been looking at the input data to analyze the problem with the rx flip.
        - there seems to be one Conjunction module that has the rx module as a destination
        - and 4 flip-flops that have that Conjunction module as destination
        - so if all of those 4 flip-flops have been flipped at least once we have a cycle
        - all of these have a number of cycle steps we can find out before it cycles.
        - at least that is my assumption :-)
        - if all are flipped at the same time the Conjunction module will flip as well so that is the terminator
        - the cycle length is the LCM of the cycle lengths of the 4 flip-flops should be the answer

        Calculate the least common multiple (LCM) (see also day 8) of the cycle lengths of all modules that have "rx"
        in their destinations.
        (as this is the second time I needed lcm I moved it to my ivonet library)

        Steps to take:

        1. Identify the module that has "rx" in its destinations and assign its name to the variable
          `module_with_rx_as_destination`.

        2. Initialize two dictionaries, `cycle_steps` and `watched`. `cycle_steps` will store the cycle length of each
           module that has `module_with_rx_as_destination` in its destinations, and `watched` will store the number
           of times each of these modules has been seen.

        3. Enter a loop that simulates pushing the button. For each button push, it creates a queue of pulses starting
           with a low pulse to the broadcaster.

        4. Enter a nested loop that processes each pulse in the queue. If a pulse is destined for a module that is
           not in the system, it is ignored. Otherwise, the pulse is processed by the destination module, and any
           resulting pulses are added to the queue.

        5. If the destination module is the `module_with_rx_as_destination` module and the pulse is high, the method
           increments the count of the origin module in the `watched` dictionary. If this is the first time the
           origin module has been seen, its cycle length is recorded in the `cycle_steps` dictionary.

        6. Once all modules that have `module_with_rx_as_destination` in their destinations have been seen at least
           once, the method calculates the LCM of their cycle lengths and returns it.
           The LCM is used so as not to have to do it brute force.

        :return: The LCM of the cycle lengths.
        """
        cycle_steps = {}
        watched = {}
        module_with_rx_as_destination = None
        for name, module in self.modules.items():
            if "rx" in module.destinations:
                module_with_rx_as_destination = name
                break

        p(f"to watch: {module_with_rx_as_destination}")
        for name, module in self.modules.items():
            if module_with_rx_as_destination in module.destinations:
                watched[name] = 0

        button_presses = 0
        while True:
            button_presses += 1
            # p(f"====pushing button {button_presses}=====")
            q = collections.deque([Pulse('button', 'broadcaster', 'low')])

            while q:
                pulse = q.popleft()
                # p(pulse)
                if pulse.destination not in self.modules:
                    continue

                module = self.modules[pulse.destination]

                if module.name == module_with_rx_as_destination and pulse.pulse == "high":
                    watched[pulse.origin] += 1
                    p(f"watched: {watched}")

                    if pulse.origin not in cycle_steps:
                        cycle_steps[pulse.origin] = button_presses
                        p(f"cycle_steps: {cycle_steps}")

                    # all watched modules have received a pulse
                    if all(watched.values()):
                        return lcm_list(list(cycle_steps.values()))

                module = self.modules[pulse.destination]
                new_pulses = module.process(pulse)
                q.extend(new_pulses)


def part_1(source: list[str]) -> int | None:
    system = System(source)
    low_pulses, high_pulses = system.simulate(1000)
    return low_pulses * high_pulses


def part_2(source: list[str]) -> int | None:
    system = System(source)
    cycles = system.rx_flip()
    return cycles


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1a(self) -> None:
        self.assertEqual(32000000, part_1(self.test_source_2))

    def test_example_data_part_1(self) -> None:
        self.assertEqual(11687500, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(731517480, part_1(self.source))

    def test_part_2(self) -> None:
        self.assertEqual(244178746156661, part_2(self.source))

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
