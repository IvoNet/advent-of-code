#!/usr/bin/env python
#  -*- coding: utf-8 -*-


def sort_alphabetical(txt, reverse=False) -> str:
    return "".join(sorted(txt, reverse=reverse))


def is_sorted(txt, reverse=False) -> bool:
    return txt == sort_alphabetical(txt, reverse=reverse)


def letters(txt, index=0):
    """return the indexed letter of words"""
    words = txt.split(" ")
    return ''.join([x[index] for x in words])
