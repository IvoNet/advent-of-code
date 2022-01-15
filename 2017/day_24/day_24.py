#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import sys
import unittest
from collections import defaultdict
from pathlib import Path
from typing import TypeVar, Callable

from ivonet.collection import Queue, PriorityQueue
from ivonet.files import read_rows
from ivonet.iter import ints
from ivonet.search import Node, node_to_path

sys.dont_write_bytecode = True
T = TypeVar('T')

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


def parse(source):
    ret = defaultdict(set)
    for line in source:
        a, b = ints(line)
        ret[a].add(b)
        ret[b].add(a)
    return ret


def bfs(start: T, successors: Callable[[T], list[T]]):
    """Breath first search
    """
    # frontier is where we've yet to go
    strongest = float("-inf")

    for initial in successors(start):
        frontier: Queue[Node[T]] = Queue()
        frontier.push(Node(initial, None))
        # explored is where we've been
        explored: set[T] = {initial}
        # keep going while there is more to explore
        while not frontier.empty:
            current_node: Node[T] = frontier.pop()
            current_state: T = current_node.state
            path = node_to_path(current_node)
            strength = sum(x + y for x, y in path)
            # all_paths.append((strength, path))
            strongest = max(strongest, strength)
            # check where we can go next and haven't explored
            for child in successors(current_state[1]):
                if child in explored:  # skip children we already explored
                    continue
                explored.add(child)
                frontier.push(Node(child, current_node))
    return strongest  # , strongest_path, all_paths, explored


def astar(start: T,
          successors: Callable[[T], list[T]],
          cost: Callable[[T], int] = lambda z: z[0] + z[1]):
    strongest = float("-inf")
    strongest_path = None
    all_paths = []

    for initial in successors(start):
        frontier: PriorityQueue[Node[T]] = PriorityQueue()
        frontier.push(Node(initial, None, 0.0, 0.0))
        explored: dict[T, float] = {initial: 0.0}

        # keep going while there is more to explore
        while not frontier.empty:
            current_node: Node[T] = frontier.pop()
            current_state: T = current_node.state
            # if we found the goal, we're done
            path = node_to_path(current_node)
            strength = sum(x + y for x, y in path)
            all_paths.append((strength, path))
            if strength > strongest:
                strongest_path = path
                strongest = strength
            for nb in successors(current_state):
                new_cost: float = current_node.cost + cost(nb)

                if nb not in explored or explored[nb] > new_cost:
                    explored[nb] = new_cost
                    frontier.push(Node(nb, current_node, new_cost, 0.0))
    return strongest


def can_connect(magnets) -> Callable[[list[tuple[int, int]]], list[T]]:
    def connectors(a: T) -> list[T]:
        ret = set()
        for b in magnets[a]:
            ret.add((a, b) if a <= b else (b, a))
        return list(ret)

    return connectors


def part_1(source):
    magnets = parse(source)
    connectors = can_connect(magnets)
    strongest = bfs(0, connectors)
    return strongest


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10""")

    def test_example_data_part_1(self):
        self.assertEqual(31, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
