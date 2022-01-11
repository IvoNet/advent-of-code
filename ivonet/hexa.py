#!/usr/bin/env python
#  -*- coding: utf-8 -*-

#          "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
from hashlib import md5

ALPHABET = "OIZE S L G"


def mdfive(s):
    """Convenience method to get an md5 hash from a string"""
    return md5(s.encode()).hexdigest()


def number_as_word(num) -> str:
    """Transforms a number into a hexadecimal notation and transforms the digits to 'corresponding' letters
    1 = I
    0 = O
    5 = S etc.
    """
    hexa = str(hex(num)).replace("0x", "").upper()
    answer = []
    for x in list(hexa):
        if x.isdigit():
            idx = int(x)
            answer.append(ALPHABET[idx])
        else:
            answer.append(x)
    return "".join(answer)


def hexagon_distance(row, col):
    """Hexagon distance.
    - if the col is larger than the row and we always walk diagonally
      we do not need to take the row into account the distance is the col
    - if the col is smaller than the row the formulae is a bit more convoluted
      it is the col distance plus the number of steps up or down we need to do and
      those are measured in halves and we need to subtract the col times halve from
      that because we walk diagonally.
          \ n  /
        nw +--+ ne
          /    \
        -+      +-
          \    /
        sw +--+ se
          / s  \
    """
    if abs(col) >= abs(row):
        return abs(col)
    else:
        return abs(col) + (abs(row) - abs(col) * 0.5)


if __name__ == '__main__':
    print(number_as_word(84679335))
    print(number_as_word(12484125))
    print(number_as_word(2677))
    print(number_as_word(52443814518132510))
