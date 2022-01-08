#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 08/01/2022 10:35$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Circular Doubly Linked List
"""

import unittest


class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None


class CDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def createCDLL(self, value):
        """Function to create Circular Doubly Linked List"""
        new_node = Node(value)
        new_node.next = None
        new_node.prev = None
        self.head = new_node
        self.tail = new_node

    def __iter__(self):
        """Iterator Function"""
        node = self.head
        while node:
            yield node
            node = node.next
            if node == self.tail.next:
                break

    def atBeg(self, value):
        """Function to add node in the beginning"""
        new_node = Node(value)
        self.head.prev = new_node
        new_node.next = self.head
        self.head = new_node
        self.tail.next = self.head
        self.head.prev = self.tail

    def inMid(self, prev_node, value):
        """Function to add node in the middle"""
        if prev_node is None:
            print("Mentioned node doesn't exist")
            return

        next_node = prev_node.next
        new_node = Node(value)
        prev_node.next = new_node
        new_node.prev = prev_node
        new_node.next = next_node
        next_node.prev = new_node

    def atEnd(self, value):
        """Function to add node in the end"""
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return
        last_node = self.head
        while (last_node.next != self.head):
            last_node = last_node.next
        last_node.next = new_node
        new_node.prev = last_node
        self.tail = new_node
        self.tail.next = self.head
        self.head.prev = self.tail

    def printForwardList(self):
        """Forward Traversal through Circular Doubly Linked List"""
        if self.head == None:
            print("The linked list does not exist.")
        else:
            temp_node = self.head
            while temp_node:
                print(temp_node.value)
                if temp_node == self.tail:
                    break
                temp_node = temp_node.next

    def printReverseList(self):
        """Reverse Traversal through Circular Doubly Linked List"""
        if self.head == None:
            print("The linked list does not exist.")
        else:
            temp_node = self.tail
            while temp_node:
                print(temp_node.value)
                if temp_node == self.head:
                    break
                temp_node = temp_node.prev

    def searchList(self, value):
        """Searching in a Circular Doubly Linked List"""
        position = 0
        found = 0
        if self.head is None:
            print("The linked list does not exist")
        else:
            temp_node = self.head
            while temp_node:
                position = position + 1
                if temp_node.value == value:
                    print("The required value was found at position: " + str(position))
                    found = 1
                    break
                if temp_node == self.tail:
                    print("The required value does not exist in the list")
                    break
                temp_node = temp_node.next

    def delBeg(self):
        """Deletion at the beginning of a Circular Doubly Linked List"""
        if (self.head == None):
            return
        elif (self.head.next == self.tail.next):
            self.head = self.tail = None
            return
        elif (self.head is not None):
            next_node = self.head.next
            next_node.prev = None
            self.head = next_node
            self.tail.next = self.head
            self.head.prev = self.tail
            return

    def delMid(self, del_value):
        """Function to delete a node from between the linked list"""
        if (self.head == None):
            return
        temp_node = self.head
        found = False
        while (temp_node):
            if (temp_node.value == del_value):
                found = True
                break
            temp_node = temp_node.next
        if (found == True):
            prev_node = temp_node.prev
            next_node = temp_node.next
            prev_node.next = next_node
            next_node.prev = prev_node
            return
        else:
            print("Element not found.")

    def delEnd(self):
        """Function to delete node from the end"""
        if (self.head == None):
            return
        elif (self.head.next == self.tail.next):
            self.head = self.tail = None
            return
        else:
            temp_node = self.head
            while (temp_node.next is not self.tail):
                temp_node = temp_node.next
            self.tail = temp_node
            temp_node.next = None
            self.tail.next = self.head
            self.head.prev = self.tail
            return

    def delCDLL(self):
        """Deletion of an entire Circular Doubly Linked List"""
        if self.head is None:
            print("The circular doubly linked list does not exist.")
        else:
            self.tail.next = None
            temp_node = self.head
            while (temp_node):
                temp_node.prev = None
                temp_node = temp_node.next
            self.head = None
            self.tail.next = None
            self.tail = None
        print("The circular doubly linked list has been deleted.")


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        cdll = CDoublyLinkedList()
        cdll.createCDLL(5)

    def test_cdll_1(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
