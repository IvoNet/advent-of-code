#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from queue import LifoQueue

from ivonet.iter import dictify


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


# def verify_open_closing_tags(s: str, tags="(){}[]<>"):
#     assert tags, "tags may not be empty"
#     assert s, "the input string may not be empty"
#     assert len(tags) % 2 == 0, "tags should come in pairs"
#     translation_table = dictify(tags)
#     bucket = LifoQueue()
#     for ch in s:
#         if ch in translation_table:
#             bucket.put(translation_table[ch])
#             continue
#         last = bucket.get()
#         if ch != last:
#             raise TagError(last, ch)
#     ret = ""
#     while not bucket.empty():
#         ret += bucket.get()
#     if len(ret)


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


def chunk_string(string, length):
    """Chops up strings in to fixed length chunks with possible leftover smaller than length at the end

    >>> list(chunk_string("abcdefghijklmnopqrstuvwxyz", 5))
    ['abcde', 'fghij', 'klmno', 'pqrst', 'uvwxy', 'z']
    """
    return (string[0 + i:length + i] for i in range(0, len(string), length))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
