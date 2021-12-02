#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
##############################################################################
# Part 1
##############################################################################

##############################################################################
# Part 2
##############################################################################

"""

from collections import defaultdict
from queue import Queue
from typing import List

from ivonet import get_data

SHINY_GOLD = "shiny gold"


def parse(data: List) -> dict:
    tree = defaultdict(set)
    for rule in data:
        parent, children_str = rule.split(" bags contain ")
        if "no other bags" in children_str:
            tree[parent.strip()] = set()
            continue
        children_with_count = children_str.replace("bags", "").replace("bag", "").replace(".", "").split(", ")
        for child_wit_count in children_with_count:
            count, child = child_wit_count.strip().split(" ", maxsplit=1)
            tree[parent.strip()].add((int(count), child))
    return tree


def part_1(data):
    # Tree stores the bags that containing bags
    tree = parse(data)

    # reverse tree: stores the set of bags containing a given bag
    reversed_tree = defaultdict(set)
    for parent, children in tree.items():
        for _, child in children:
            reversed_tree[child].add(parent)

    result = set()
    q = Queue()
    q.put(SHINY_GOLD)

    while not q.empty():
        bag = q.get()
        result.add(bag)
        for next_bag in reversed_tree[bag]:
            if next_bag not in result:
                q.put(next_bag)

    result.remove(SHINY_GOLD)
    return len(result)


def part_2(data):
    tree = parse


if __name__ == '__main__':
    source = get_data("day-7.txt")
    print(part_1(source))
    print(part_2(source))
