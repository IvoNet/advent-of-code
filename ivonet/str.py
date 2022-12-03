#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from queue import LifoQueue

from ivonet.iter import dictify

cat = "".join


def sort_str(txt, reverse=False) -> str:
    return "".join(sorted(txt, reverse=reverse))


def is_sorted(txt, reverse=False) -> bool:
    return txt == sort_str(txt, reverse=reverse)


def letters(txt, index=0):
    """return the indexed letter of words"""
    words = txt.split(" ")
    return ''.join([x[index] for x in words])


class TagError(RuntimeError):

    def __init__(self, expected=None, actual=None, incomplete=None) -> None:
        self.expected = expected
        self.actual = actual
        self.incomplete = incomplete

    def __str__(self) -> str:
        if self.incomplete:
            return f"Expected these closing tags '{self.incomplete}'."
        if self.expected and self.actual:
            return f"Expected {self.expected}, but found {self.actual} instead."
        if not self.expected and self.actual:
            return f"Expected to be finished, but found {self.actual} instead."


class OpenCloseTags(object):

    def __init__(self, s: str, tags="(){}[]<>", exception=False) -> None:
        assert tags, "tags may not be empty"
        assert s, "the input string may not be empty"
        assert len(tags) % 2 == 0, "tags should come in pairs"
        self.source = s
        self.translation_table = dictify(tags)
        self.bucket = LifoQueue()
        self.raise_exception = exception
        self.expected = None
        self.actual = None
        self.incomplete = ""
        self.__validate()
        self.__error()

    def __validate(self):
        for ch in self.source:
            if ch in self.translation_table:
                self.bucket.put(self.translation_table[ch])
                continue
            if self.bucket.empty():
                self.expected = None
                self.actual = ch
            else:
                last = self.bucket.get()
                if ch != last:
                    self.expected = last
                    self.actual = ch
                    return
        while not self.bucket.empty():
            self.incomplete += self.bucket.get()

    def is_valid(self) -> bool:
        if self.expected or self.actual or self.incomplete:
            return False
        return True

    def meta(self):
        return {
            "source": self.source,
            "valid": self.is_valid(),
            "expected": self.expected,
            "actual": self.actual,
            "incomplete": self.incomplete,
        }

    def __error(self):
        if self.raise_exception and not self.is_valid():
            raise TagError(expected=self.expected, actual=self.actual, incomplete=self.incomplete)


def swap_position(data: str, x: int, y: int):
    """Swap position X with position Y means that the letters at indexes X and Y
    (counting from 0) should be swapped"""
    ret = list(data)
    ret[x], ret[y] = ret[y], ret[x]
    return "".join(ret)


def swap_letter(data: str, a: str, b: str):
    """Swap letter X with letter Y means that the letters X and Y should be swapped
    (regardless of where they appear in the string)."""
    return swap_position(data, data.index(a), data.index(b))


def rotate_right(data: str, steps: int):
    """Rotate right X steps means that the whole string should be rotated."""
    steps = steps % len(data)
    return data[-steps:] + data[:-steps]


def rotate_left(data: str, steps: int):
    """Rotate left X steps means that the whole string should be rotated."""
    steps = steps % len(data)
    return data[steps:] + data[:steps]


def move_pos(data: str, x: int, y: int):
    """Move position X to position Y means that the letter which is at index X
    should be removed from the string, then inserted such that it ends up at index Y"""
    l = data[x]
    lst = list(data)
    lst.remove(l)
    lst.insert(y, l)
    return "".join(lst)


def reverse_positions(data: str, x: int, y: int):
    """reverse positions X through Y means that the span of letters at indexes X through Y
    (including the letters at X and Y) should be reversed in order"""
    ret = data[:x]
    ret += data[x:y + 1][::-1]
    tail = len(data) - 1 - y
    if tail > 0:
        ret += data[-tail:]
    return ret


def str_minus_str(s1: str, s2: str):
    """s1 minus s2 only leaving in the list all the letters not in s2

    eg.
    >>> str_minus_str("acdge", "dex")
    'acg'
    >>> str_minus_str("acdge", "abdeerwerede")
    'cg'
    >>> str_minus_str("a", "ab")
    ''
    >>> str_minus_str("ab", "a")
    'b'
    """
    return "".join([x for x in s1 if x not in s2])


def str_minus_len(s1, s2):
    """calc length of str_min_str(s1, s2)

    >>> str_minus_len("acdge", "dex")
    3
    >>> str_minus_len("acdge", "abdeerwerede")
    2
    >>> str_minus_len("a", "ab")
    0
    >>> str_minus_len("ab", "a")
    1
    """
    return len(str_minus_str(s1, s2))


def common_elements(interable) -> list:
    """return the common elements of a list of iterables
    >>> common_elements([range(10), range(5, 15), range(8, 18)])
    [8, 9]
    """
    return list(set.intersection(*map(set, interable)))


def read_european_number(european_number):
    """Transform a European number into a float."""
    try:
        number = european_number.replace('.', '')
        number = number.replace(',', '.')
        number = float(number)
        return number
    except ValueError:
        # If the string cannot be converted (e.g. an empty string), the original is returned
        return european_number


if __name__ == '__main__':
    import doctest

    doctest.testmod()
