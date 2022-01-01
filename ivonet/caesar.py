#!/usr/bin/env python3
#  -*- coding: utf-8 -*-


ALPHABET = list("abcdefghijklmnopqrstuvwxyz")


def __alphabet(loc):
    return ALPHABET[loc]


def caesar_cipher_char(char, shift=0):
    """char in alphabet with possible shift"""
    return __alphabet((ALPHABET.index(char.lower()) + shift) % 26)


def caesar_decipher_char(char, shift=0):
    return __alphabet((shift - ALPHABET.index(char.lower())) % 26)


def caesar_cipher(value, shift=13):
    return "".join([caesar_cipher_char(x, shift) for x in value.replace(" ", "")])


def rot(value: str) -> dict:
    """
# ROTational encryption.

Return a dictionary with all standard ROTation values of the alphabet.
    """
    ret = {}
    for i in range(len(ALPHABET)):
        ret["ROT({0})".format(i)] = caesar_cipher(value, shift=i)
    return ret


if __name__ == '__main__':
    for i in range(28):
        print(caesar_cipher("TUBE".replace(" ", ""), i).upper())

    print(rot("FDHVDU"))
