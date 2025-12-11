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
import sys
import unittest
from collections import defaultdict
from pathlib import Path

import pyperclip
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


def parse_devices(source: list[str]) -> dict[str, list[str]]:
    devices = defaultdict(list)
    for line in source:
        if not line:
            continue
        dev, outputs = line.split(": ")
        devices[dev.strip()] = [d.strip() for d in outputs.split(" ") if d.strip()]
    return devices


def find_paths(devices: dict[str, list[str]], current_device: str, end_device: str, visited: set[str]) -> int:
    if current_device == end_device:
        return 1
    path_count = 0
    for next_device in devices[current_device]:
        if next_device not in visited:
            visited.add(next_device)
            path_count += find_paths(devices, next_device, end_device, visited)
            visited.remove(next_device)
    return path_count

def find_paths_with_mandatory(devices: dict[str, list[str]], current_device: str, end_device: str, visited: set[str],
                              mandatory: set[str]) -> int:
    if current_device == end_device:
        return 1 if not mandatory else 0
    path_count = 0
    for next_device in devices[current_device]:
        if next_device not in visited:
            visited.add(next_device)
            new_mandatory = mandatory - {next_device} if next_device in mandatory else mandatory
            path_count += find_paths_with_mandatory(devices, next_device, end_device, visited, new_mandatory)
            visited.remove(next_device)
    return path_count

@debug
@timer
def part_1(source) -> int | None:
    """
    A device has a label and a list of devices it is connected (outputs) to.
    A connection is one way only.
    The start device is the device called `you` and the end device is the device called `out`.
    Goal is to find all the paths from `you` to `out` and count them.

    """
    END_DEVICE_NAME = "out"
    START_DEVICE_LABEL = "you"

    devices = parse_devices(source)
    answer = find_paths(devices, START_DEVICE_LABEL, END_DEVICE_NAME, {START_DEVICE_LABEL})
    pyperclip.copy(str(answer))
    return answer


@debug
@timer
def part_2(source) -> int | None:
    """
    A device has a label and a list of devices it is connected (outputs) to.
    A connection is one way only.
    The start device is the device called `svr` and the end device is the device called `out`.
    A path needs to visit `dac` and `fft` at least once before reaching `out` in any order to be counted.
    Goal is to find all the paths from `svr` to `out` and count them.

    :param source:
    :return:
    """
    devices = parse_devices(source)
    answer = find_paths_with_mandatory(devices, "svr", "out", {"svr"}, {"dac", "fft"})
    pyperclip.copy(str(answer))
    return answer


# noinspection DuplicatedCode
class UnitTests(unittest.TestCase):

    def test_example_data_part_1(self) -> None:
        self.assertEqual(5, part_1(self.test_source))

    def test_part_1(self) -> None:
        self.assertEqual(652, part_1(self.source))

    def test_example_data_part_2(self) -> None:
        self.assertEqual(2, part_2(self.test_source_2))

    def test_part_2(self) -> None:
        self.assertEqual(None, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")
        self.test_source_2 = read_rows(f"{folder}/test_{day}_2.input")


if __name__ == '__main__':
    unittest.main()
