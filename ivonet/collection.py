#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 29/12/2021 20:31$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

from collections import deque
from heapq import heappush, heappop
from typing import Generic, TypeVar, Deque, Iterable

T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: list[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()  # LIFO

    def __repr__(self) -> str:
        return repr(self._container)


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = deque()

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()  # FIFO

    def extend(self, iterable: Iterable[T]):
        self._container.extend(iterable)
        return self

    def __repr__(self) -> str:
        return repr(self._container)


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: list[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def push(self, item: T) -> None:
        heappush(self._container, item)  # in by priority

    def pop(self) -> T:
        return heappop(self._container)  # out by priority

    def __repr__(self) -> str:
        return repr(self._container)



def max_k_subsequence(digits: str, k: int) -> str:
    """Return the lexicographically largest subsequence of length k from the string of digits.

    Uses a greedy stack algorithm: for each digit, pop smaller digits from the stack
    while there are enough remaining digits to fill k, then push current digit.
    Finally, take the first k digits from the stack.
    see: 2025 day 3
    """
    n = len(digits)
    if k >= n:
        return digits
    stack: list[str] = []
    to_remove = n - k  # number of digits we can drop
    for i, ch in enumerate(digits):
        # While we can pop and current char is greater than last in stack, pop.
        while stack and to_remove > 0 and stack[-1] < ch:
            stack.pop()
            to_remove -= 1
        stack.append(ch)
    # If still have removals left, drop from the end
    if to_remove:
        stack = stack[:-to_remove]
    # Join and ensure length k
    result = ''.join(stack[:k])
    return result
