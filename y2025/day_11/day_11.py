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
    """
    Counts the number of simple paths from the current_device to the end_device in a directed graph,
    ensuring no cycles by tracking visited nodes.

    This function uses a recursive backtracking approach to explore all possible paths from the
    starting device to the ending device. It maintains a set of visited nodes to prevent revisiting
    any node, thus avoiding infinite loops in graphs with cycles.

    Args:
        devices (dict[str, list[str]]): A dictionary where keys are device names and values are lists
            of devices they connect to (outputs).
        current_device (str): The device to start the path from.
        end_device (str): The target device to reach.
        visited (set[str]): A set of devices already visited in the current path. This is modified
            during recursion and should be initialized with the starting device.

    Returns:
        int: The number of distinct simple paths from current_device to end_device.

    Strengths:
        - Correctly handles graphs with cycles by enforcing simple paths (no revisits).
        - Straightforward implementation using recursion.

    Weaknesses:
        - Exponential time complexity due to exploring all possible paths, which can be very slow
          for graphs with many nodes or high branching factors.
        - High space usage for the recursion stack and visited set, especially in deep graphs.
        - Does not scale well for large inputs.
    """
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
    """
    Counts the number of simple paths from the current_device to the end_device that visit all mandatory devices,
    ensuring no cycles by tracking visited nodes.

    This function extends the basic path counting by requiring that all devices in the 'mandatory' set are visited
    at least once before reaching the end_device. It uses recursive backtracking, maintaining a set of visited nodes
    to avoid cycles and a set of remaining mandatory devices to track progress.

    Args:
        devices (dict[str, list[str]]): A dictionary where keys are device names and values are lists
            of devices they connect to (outputs).
        current_device (str): The device to start the path from.
        end_device (str): The target device to reach.
        visited (set[str]): A set of devices already visited in the current path. Modified during recursion;
            initialize with the starting device.
        mandatory (set[str]): A set of devices that must be visited in the path. Modified during recursion
            as devices are visited.

    Returns:
        int: The number of distinct simple paths from current_device to end_device that visit all mandatory devices.

    Strengths:
        - Correctly handles graphs with cycles and ensures mandatory visits.
        - Builds on the basic path finding logic, making it easy to extend.

    Weaknesses:
        - Even higher exponential time complexity than find_paths due to additional constraints and branching.
        - Increased space usage from managing the mandatory set.
        - Inefficient for large graphs or many mandatory devices.
    """
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


def find_paths_memo(devices: dict[str, list[str]], node: str, mandatory: frozenset[str], end_device: str, memo: dict) -> int:
    """
    Counts the number of paths from the given node to end_device that have visited all mandatory devices,
    using memoization. Assumes the graph is a Directed Acyclic Graph (DAG) (no cycles).

    This function optimizes path counting by memoizing results based on the current node and the set of
    remaining mandatory devices to visit. It recursively explores paths, updating the mandatory set when
    devices are encountered, and only counts paths that reach end_device with all mandatory devices visited.

    Args:
        devices (dict[str, list[str]]): A dictionary where keys are device names and values are lists
            of devices they connect to (outputs).
        node (str): The current device in the path.
        mandatory (frozenset[str]): A frozenset of devices that must be visited in the path.
        end_device (str): The target device to reach.
        memo (dict): A dictionary for memoization, mapping (node, mandatory) tuples to computed counts.

    Returns:
        int: The number of paths from node to end_device with all mandatory devices visited.

    Strengths:
        - Efficient for DAGs due to memoization, reducing redundant computations.
        - Generalizable to any set of mandatory devices and end device.
        - Simple and fast for acyclic graphs.

    Weaknesses:
        - Assumes no cycles; if cycles exist, it will cause infinite recursion.
        - Memoization dictionary can grow large with many nodes or mandatory devices.
        - Frozenset operations are efficient but may be slower than bitmasks for small sets.
    """
    if node == end_device:
        return 1 if not mandatory else 0
    key = (node, mandatory)
    if key in memo:
        return memo[key]
    count = 0
    for next_node in devices.get(node, []):
        new_mandatory = mandatory - {next_node} if next_node in mandatory else mandatory # create new frozenset (hashable)
        count += find_paths_memo(devices, next_node, new_mandatory, end_device, memo)
    memo[key] = count
    return count

@debug
@timer
def part_1(source) -> int | None:
    """
    A device has a label and a list of devices it is connected (outputs) to.
    A connection is one way only.
    The start device is the device called `you` and the end device is the device called `out`.
    Goal is to find all the paths from `you` to `out` and count them.

    """
    devices = parse_devices(source)

    answer= find_paths(devices, "you", "out", {"you"})
    # answer = find_paths_with_mandatory(devices, "you", "out", {"you"}, set())
    # answer = find_paths_memo(devices, "you", frozenset(), "out", {})
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

    """
    devices = parse_devices(source)
    memo = {}
    answer = find_paths_memo(devices, "svr", frozenset({"dac", "fft"}), "out", memo)
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
        self.assertEqual(362956369749210, part_2(self.source))

    def setUp(self) -> None:
        print()
        folder = Path(__file__).resolve().parent
        day = f"{ints(Path(__file__).stem)[0]:02}"
        self.source = read_rows(f"{folder}/day_{day}.input")
        self.test_source = read_rows(f"{folder}/test_{day}.input")
        self.test_source_2 = read_rows(f"{folder}/test_{day}_2.input")


if __name__ == '__main__':
    unittest.main()
