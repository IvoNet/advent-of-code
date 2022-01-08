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
from itertools import count
from pathlib import Path
from typing import Optional

from ivonet.files import read_data
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self) -> str:
        return f"Node<data={repr(self.data)} prev={repr(self.prev.data)} next={repr(self.next.data)}>"


class CircularDoublyLinkedList:
    def __init__(self):
        self.first: Node = Optional[Node]
        self.current: Node = Optional[Node]

    def __repr__(self) -> str:
        """Representation of one cicle from the first node to the last node walking right"""
        if not self.first:
            return "CircularDoublyLinkedList<>"
        ret = "CircularDoublyLinkedList<["
        node = self.first
        while True:
            ret += f"{repr(node)}, "
            node = node.next
            if node == self.first:
                break
        return ret + "]>"

    def get_node(self, index):
        current = self.first
        for _ in range(index):
            current = current.next
        self.current = current
        return current

    def next(self):
        if not self.first:
            return None
        if not self.current:
            self.current = self.first
        self.current = self.current.next
        return self.current

    def previous(self):
        if not self.first:
            return None
        if not self.current:
            self.current = self.first
        self.current = self.current.prev
        return self.current

    def reset(self):
        self.current = self.first

    @staticmethod
    def insert_after(ref_node, new_node):
        new_node.prev = ref_node
        new_node.next = ref_node.next
        new_node.next.prev = new_node
        ref_node.next = new_node

    def insert_before(self, ref_node, new_node):
        self.insert_after(ref_node.prev, new_node)

    def insert_at_end(self, new_node):
        if self.first is None:
            self.first = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            self.insert_after(self.first.prev, new_node)

    def append(self, value):
        self.insert_at_end(Node(value))

    def insert_at_beginning(self, new_node):
        self.insert_at_end(new_node)
        self.first = new_node

    def prepend(self, value):
        self.insert_at_beginning(Node(value))

    def remove(self, node):
        if self.first.next == self.first:
            self.first = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if self.first == node:
                self.first = node.next
            if self.current == node:
                self.current = self.first

    def delete_at_index(self, index):
        node = self.get_node(index)
        if node:
            self.remove(node)

    def display(self):
        if self.first is None:
            return
        current = self.first
        while True:
            print(current.data, end=' ')
            current = current.next
            if current == self.first:
                break

    def __len__(self) -> int:
        node = self.first
        for i in count():
            node = node.next
            if node == self.first:
                return i

    def get(self):
        return self.current.data


def create_cll(elves):
    elf_ring = CircularDoublyLinkedList()
    for i in range(1, elves + 1):
        elf_ring.append(i)
    return elf_ring


def part_1(source):
    nr_of_elves = int(source)
    elf_ring = create_cll(nr_of_elves)
    start_elf = elf_ring.get_node(0)
    while len(elf_ring) > 1:
        elf_ring.remove(start_elf.next)
        start_elf = start_elf.next
    return elf_ring.get()


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")

    def test_example_data_part_1(self):
        self.assertEqual(3, part_1("5"))

    def test_part_1(self):
        self.assertEqual(None, part_1(self.source))

    def test_part_2(self):
        self.assertEqual(None, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
