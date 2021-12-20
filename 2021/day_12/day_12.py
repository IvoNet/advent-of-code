#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = r"""Day 12: Passage Pathing

With your submarine's subterranean subsystems subsisting suboptimally, 
the only way you're getting out of this cave anytime soon is by finding 
a path yourself. Not just a path - the only way to know if you've found 
the best path is to find all of them.

Fortunately, the sensors are still mostly working, and so you build a 
rough map of the remaining caves (your puzzle input). For example:

start-A
start-b
A-c
A-b
b-d
A-end
b-end
This is a list of how all of the caves are connected. You start in the 
cave named start, and your destination is the cave named end. An entry 
like b-d means that cave b is connected to cave d - that is, you can 
move between them.

So, the above cave system looks roughly like this:

    start
    /   \
c--A-----b--d
    \   /
     end
     
Your goal is to find the number of distinct paths that start at start, 
end at end, and don't visit small caves more than once. There are two 
types of caves: big caves (written in uppercase, like A) and small caves 
(written in lowercase, like b). It would be a waste of time to visit any 
small cave more than once, but big caves are large enough that it might 
be worth visiting them multiple times. So, all paths you find should 
visit small caves at most once, and can visit big caves any number of times.

Given these rules, there are 10 paths through this example cave system:

start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end

(Each line in the above list corresponds to a single path; the caves 
visited by that path are listed in the order they are visited and separated 
by commas.)

Note that in this cave system, cave d is never visited by any path  
to do so, cave b would need to be visited twice (once on the way to cave 
d and a second time when returning from cave d), and since cave b is 
small, this is not allowed.

Here is a slightly larger example:

dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc

The 19 paths through it are as follows:

start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end

Finally, this even larger example has 226 paths through it:

fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW

How many paths through this cave system are there that visit small caves 
at most once?


--- Part Two ---

After reviewing the available paths, you realize you might have time to 
visit a single small cave twice. Specifically, big caves can be visited 
any number of times, a single small cave can be visited at most twice, and 
the remaining small caves can be visited at most once. However, the caves 
named start and end can only be visited exactly once each: once you leave 
the start cave, you may not return to it, and once you reach the end cave, 
the path must end immediately.

Now, the 36 possible paths through the first example above are:

start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end

The slightly larger example above now has 103 paths through it, and the even 
larger example now has 3509 paths through it.

Given these new rules, how many paths through this cave system are there?
"""

import sys
import unittest
from collections import defaultdict
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True


def prepare(source):
    graph = Graph()
    for x in source:
        graph.add(x)
    return graph


class Graph:

    def __init__(self) -> None:
        self.nodes = defaultdict(list)
        self.small_nodes = set()

    def add_small(self, node: str):
        if node == node.lower() and node not in ["start", "end"]:
            self.small_nodes.add(node)

    def add(self, s: str):
        a, b = s.split("-")
        self.nodes[a].append(b)
        self.nodes[b].append(a)
        self.add_small(a)
        self.add_small(b)

    # noinspection PyDefaultArgument
    def find_all_paths(self, start="start", visited=[], path=[], small_node_twice=None):
        path = path + [start]
        if small_node_twice == start:  # part 2 special case
            small_node_twice = None
        else:
            if start == start.lower():
                visited = visited + [start]
        if start == "end":
            return [path]
        paths = []
        for node in self.nodes[start]:
            if node not in visited:
                new_paths = self.find_all_paths(node, visited, path, small_node_twice)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths

    def find_all_paths_with_one_small_twice(self):
        paths = set()  # performance boost by changing this from list to set!
        for node in self.small_nodes:
            new_paths = self.find_all_paths(small_node_twice=node)
            for new_path in new_paths:
                paths.add(",".join(new_path))  # set is much faster but list is not hashable so convert to string

        return paths


def part_1(source):
    graph = prepare(source)
    return len(graph.find_all_paths())


def part_2(source):
    graph = prepare(source)
    return len(graph.find_all_paths_with_one_small_twice())


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_rows(f"day_{day}.input")
        self.test_source_smallest = read_rows("""start-A
start-b
A-c
A-b
b-d
A-end
b-end""")
        self.test_source_bigger = read_rows("""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""")
        self.test_source = read_rows("""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""")

    def test_example_data_part_1_smallest(self):
        self.assertEqual(10, part_1(self.test_source_smallest))

    def test_example_data_part_1_biggerl(self):
        self.assertEqual(19, part_1(self.test_source_bigger))

    def test_example_data_part_1(self):
        self.assertEqual(226, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(3410, part_1(self.source))

    def test_example_data_part_2_smallest(self):
        self.assertEqual(36, part_2(self.test_source_smallest))

    def test_example_data_part_2_bigger(self):
        self.assertEqual(103, part_2(self.test_source_bigger))

    def test_example_data_part_2(self):
        self.assertEqual(3509, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(98796, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
