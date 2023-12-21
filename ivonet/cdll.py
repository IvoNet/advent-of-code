#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__revised__ = "$revised: 08/01/2022 14:55$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """A Circular Doubly Linked List
a simple implementation of a CircularDoublyLinkedList

See the unit tests in this package and a good 
usage example in 2016 day 19 and 2018 day 9
"""

from typing import TypeVar, Generic, Optional, Iterator

T = TypeVar('T')


class Node(Generic[T]):
    """A Node as companion to the Circular Doubly Linked List
    A node contains data and a reference to its next and previous.
    On its own it points to itself both ways.
    """

    def __init__(self, data: T):
        self.data: T = data
        self.next: Optional[Node] = self
        self.prev: Optional[Node] = self

    def __repr__(self) -> str:
        return f"Node<data={repr(self.data)} prev={repr(self.prev.data)} next={repr(self.next.data)}>"


class CircularDoublyLinkedList:

    def __init__(self) -> None:
        self.first: Node[T] | None = None
        self.current_node: Node[T] | None = None
        self.size: int = 0
        self.current_first = True

    def node(self, index: int, update_current=True) -> Optional[Node[T]]:
        """Gets the node at index.
        As this is a circular linked list there is no end to the index.
        It goes round and round and round :-) So be careful what you ask for.
        To speed things up first a mod of the size will be done so that we are not
        walking around in circles for nothing.
        """
        if not self.first:
            return None
        current = self.first
        for _ in range(index % self.size):
            current = current.next
        if update_current:
            self.current_node = current
        return current

    def next(self) -> Optional[Node[T]]:
        """'Walks' forwards from the current node"""
        if not self.first:
            return None
        if not self.current_node:
            self.current_node = self.first
        self.current_first = False
        self.current_node = self.current_node.next
        return self.current_node

    def step_right(self, times) -> Optional[Node[T]]:
        """'Walks' forwards from the current node"""
        for _ in range(times % self.size):
            self.next()
        return self.current()

    def previous(self) -> Optional[Node[T]]:
        """'Walks' backwards from the current node"""
        if not self.first:
            return None
        if not self.current_node:
            self.current_node = self.first
        self.current_node = self.current_node.prev
        self.current_first = False
        return self.current_node

    def step_left(self, times) -> Optional[Node[T]]:
        for _ in range(times % self.size):
            self.previous()
        return self.current()

    def current(self) -> Optional[Node[T]]:
        if self.current_node:
            return self.current_node
        return None

    def done(self) -> bool:
        """Checks if the current node is the first node
        it assumes that if these are the same we are done
        but if it is the first cycle it is not done
        This function only has purpose as long as you walk
        only one way :-)
        """
        if self.current_first:
            return False
        return self.first == self.current_node

    def reset(self):
        """Resets the current node to the first node"""
        self.current_node = self.first
        self.current_first = True

    def insert_after(self, ref_node: Node[T], new_node: Node[T]):
        """Inserts a node after the reference node"""
        new_node.prev = ref_node
        new_node.next = ref_node.next
        new_node.next.prev = new_node
        ref_node.next = new_node
        self.size += 1

    def insert_after_current(self, value):
        self.insert_after(self.current_node, Node(value))

    def insert_before_current(self, value):
        self.insert_before(self.current_node, Node(value))

    def insert_before(self, ref_node: Node[T], new_node: Node[T]):
        """Inserts a node before the reference node"""
        self.insert_after(ref_node.prev, new_node)

    def insert_at_end(self, new_node: Node[T]):
        """Appends a node at the 'end' of the cycle"""
        if self.first is None:
            self.first = new_node
            self.current_node = self.first
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

    def extend(self, iterator: Iterator[T]):
        """Extend the cycle by adding the whole iterable to the 'end' of the cycle"""
        for i in iterator:
            self.append(i)

    def insert_at_beginning(self, new_node: Node[T]):
        self.insert_at_end(new_node)
        self.first = new_node

    def prepend(self, value: T):
        """Insert at start of cycle based on value
        Convenience method so you do not have to create the Node
        """
        self.insert_at_beginning(Node(value))

    def popleft(self) -> T | None:
        """Returns the value of the first and removes the node from the cycle
        the next node will become the first node.
        """
        if self.empty():
            return None
        value = self.first.data
        self.remove(self.first)
        return value

    def remove(self, node: Node[T]):
        if not self.first:
            return
        if self.first.next == self.first:
            self.first = None
            self.current_node = None
            self.size = 0
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if self.first == node:
                self.first = node.next
            if self.current_node == node:
                self.current_node = node.next
            self.size -= 1

    def remove_index(self, index: int):
        node = self.node(index, update_current=False)
        if node:
            self.remove(node)

    def get(self):
        """Convenience method to get the data of the current node"""
        if self.current_node:
            return self.current_node.data
        return None

    def repr_current_circle(self):
        if not self.first:
            return f"{self.__class__.__name__}<>"
        ret = f"{self.__class__.__name__}<["
        node = self.current_node
        while True:
            ret += f"{repr(node)}, "
            node = node.next
            if node == self.current_node:
                break
        return ret + "]>"

    def empty(self) -> bool:
        """Do we have nodes or not"""
        return self.size == 0

    def __getitem__(self, item: int) -> T:
        """Gets the data of a node based on the index"""
        return self.node(item, update_current=False).data

    def __repr__(self) -> str:
        """Representation of one cycle from the first node to the last node walking right"""
        if not self.first:
            return f"{self.__class__.__name__}<>"
        ret = f"{self.__class__.__name__}<["
        node = self.first
        while True:
            ret += f"{repr(node)}, "
            node = node.next
            if node == self.first:
                break
        return ret + "]>"

    def __len__(self) -> int:
        return self.size
