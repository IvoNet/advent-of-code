#!/usr/bin/env python
#  -*- coding: utf-8 -*-

#          "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

ALPHABET = "OIZE S L G"


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


if __name__ == '__main__':
    print(number_as_word(84679335))
    print(number_as_word(12484125))
    print(number_as_word(2677))
    print(number_as_word(52443814518132510))
