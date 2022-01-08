#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 08/01/2022 10:29$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Circular Doubly  Linked Lists

Stongly based on what can be found here:
https://www.askpython.com/python/examples/doubly-circular-linked-list
"""


class Node:
    """Node representing an item in a Doubly Circular Linked Lists
    A node when the only element will point to itself in both directions.
    """

    def __init__(self, data=None):
        self.data = data
        self.previous = self
        self.next = self

    def __repr__(self) -> str:
        return f"Node<{self.data}>"


class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.count = 0

    def __repr__(self):
        string = ""

        if (self.head == None):
            string += "CircularDoublyLinkedList Empty"
            return string

        string += f"CircularDoublyLinkedList: \n{self.head.data}"
        temp = self.head.next
        while (temp != self.head):
            string += f" -> {temp.data}"
            temp = temp.next
        return string

    def append(self, data):
        self.insert(data, self.count)

    def insert(self, data, index):
        if (index > self.count) | (index < 0):
            raise IndexError(f"Index out of range: {index}, size: {self.count}")

        if self.head == None:
            self.head = Node(data)
            self.count = 1
            return

        temp = self.head
        if (index == 0):
            temp = temp.previous
        else:
            for _ in range(index - 1):
                temp = temp.next

        temp.next.previous = Node(data)
        temp.next.previous.next, temp.next.previous.previous = temp.next, temp
        temp.next = temp.next.previous
        if (index == 0):
            self.head = self.head.previous
        self.count += 1

    def remove(self, index):
        if (index >= self.count) | (index < 0):
            raise IndexError(f"Index out of range: {index}, size: {self.count}")

        if self.count == 1:
            self.head = None
            self.count = 0
            return

        target = self.head
        for _ in range(index):
            target = target.next

        if target is self.head:
            self.head = self.head.next

        target.previous.next, target.next.previous = target.next, target.previous
        self.count -= 1

    def index(self, data):
        temp = self.head
        for i in range(self.count):
            if (temp.data == data):
                return i
            temp = temp.next
        return None

    def get(self, index):
        if (index >= self.count) | (index < 0):
            raise IndexError(f"Index out of range: {index}, size: {self.count}")

        temp = self.head
        for _ in range(index):
            temp = temp.next
        return temp.data

    def size(self):
        return self.count

    def display(self):
        print(self)


if __name__ == '__main__':
    cdll = CircularDoublyLinkedList()
    cdll.append(5)
    cdll.append(3)
    cdll.append(2)
    print(cdll)
    cdll.remove(1)
    print(cdll)
