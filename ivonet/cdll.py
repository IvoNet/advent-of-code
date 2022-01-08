#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__revised__ = "$revised: 08/01/2022 14:55$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """A Circular Doubly Linked List
a simple implementation of a CircularDoublyLinkedList
"""

from typing import TypeVar, Generic, Optional

T = TypeVar('T')


class Node(Generic[T]):
    """A Node as companion to the Circular Doubly Linked List
    A node has data and a next and previous.
    On its own it points to itself both ways.
    """

    def __init__(self, data: T):
        self.data: T = data
        self.next: Optional[Node] = self
        self.prev: Optional[Node] = self

    def __repr__(self) -> str:
        return f"Node<data={repr(self.data)} prev={repr(self.prev.data)} next={repr(self.next.data)}>"


class CircularDoublyLinkedList:
    def __init__(self):
        self.first: Node[T] | None = None
        self.current: Node[T] | None = None
        self.size: int = 0

    def get_node(self, index: int):
        current = self.first
        for _ in range(index):
            current = current.next
        self.current = current
        return current

    def next(self):
        """'Walks' forwards from the current node"""
        if not self.first:
            return None
        if not self.current:
            self.current = self.first
        self.current = self.current.next
        return self.current

    def previous(self):
        """'Walks' backwards from the current node"""
        if not self.first:
            return None
        if not self.current:
            self.current = self.first
        self.current = self.current.prev
        return self.current

    def reset(self):
        """Resets the current node to the first node"""
        self.current = self.first

    def insert_after(self, ref_node: Node[T], new_node: Node[T]):
        """Inserts a node after the reference node"""
        new_node.prev = ref_node
        new_node.next = ref_node.next
        new_node.next.prev = new_node
        ref_node.next = new_node
        self.size += 1

    def insert_before(self, ref_node: Node[T], new_node: Node[T]):
        """Inserts a node before the reference node"""
        self.insert_after(ref_node.prev, new_node)

    def insert_at_end(self, new_node: Node[T]):
        """Appends a node at the 'end' of the cycle"""
        if self.first is None:
            self.first = new_node
            new_node.next = new_node
            new_node.prev = new_node
            self.size = 1
        else:
            self.insert_after(self.first.prev, new_node)

    def append(self, value: T):
        """Append on value.
        Convenience method so you do not have to create the node
        """
        self.insert_at_end(Node(value))

    def insert_at_beginning(self, new_node: Node[T]):
        self.insert_at_end(new_node)
        self.first = new_node

    def prepend(self, value: T):
        """Insert at start of cycle based on value
        Convenience method so you do not have to create the Node
        """
        self.insert_at_beginning(Node(value))

    def remove(self, node: Node[T]):
        if self.first.next == self.first:
            self.first = None
            self.current = None
            self.size = 0
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if self.first == node:
                self.first = node.next
            if self.current == node:
                self.current = self.first
            self.size -= 1

    def remove_index(self, index: int):
        node = self.get_node(index)
        if node:
            self.remove(node)

    def get(self):
        """Convenience method to get the data of the current node"""
        if self.current:
            return self.current.data
        return None

    def __repr__(self) -> str:
        """Representation of one cycle from the first node to the last node walking right"""
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

    def __len__(self) -> int:
        return self.size
