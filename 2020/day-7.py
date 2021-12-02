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

from ivonet import get_data

SHINY_GOLD = "shiny gold"

all_bags = {}

all_names = set()


class UnknownBag(Exception):
    pass


class Bag(object):

    def __init__(self, data: str) -> None:
        self.data = data.replace(" bags", "").replace("bag", "").replace(".", "").replace("  ", " ")
        parts = list(map(str.strip, self.data.split("contain")))
        self.name = parts[0]
        all_names.add(self.name)
        parts = list(map(str.strip, parts[1].split(",")))
        self.contain = {}
        for bag in parts:
            if bag == "no other":
                break
            items = bag.split(" ")
            amount = int(items[0])
            name = " ".join(items[1:])
            self.contain[name] = [name, amount]
            all_names.add(name)
        all_bags[self.name] = self

    def __str__(self) -> str:
        return f"{self.name} -> {list(self.contain.keys())}"

    def __repr__(self) -> str:
        return f"{self.name}"

    def __eq__(self, o: object) -> bool:
        return o.name == self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def has_bag(self, bag) -> bool:
        if type(bag) == str:
            return bag in self.contain
        return bag.name in self.contain

    def amount(self, bag) -> int:
        if not self.has_bag(bag):
            return 0
        if type(bag) == str:
            return self.contain.get(bag, 0)
        return self.contain.get(bag.name, 0)


def get_direct(bags, search_for):
    ret = []
    for bag in bags:
        if bag.has_bag(search_for):
            ret.append(bag)
    return ret


def part_1(data):
    bags = list(map(Bag, data))
    shiny_gold = all_bags[SHINY_GOLD]

    # find the direct ones
    alles = set()
    direct = get_direct(bags, shiny_gold)
    alles = alles.union(direct)
    for bag in direct:
        for name in bag.contain:
            l = get_direct(bags, name)
            alles = alles.union(l)
    for bag in alles.copy():
        l = get_direct(bags, bag)
        alles = alles.union(l)
    print(len(bags))
    # print(alles)
    print(len(alles))


def part_2(data):
    pass


if __name__ == '__main__':
    source = get_data("day-7.txt")
    print(part_1(source))
    print(part_2(source))
