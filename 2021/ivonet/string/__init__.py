#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import hashlib
import random
import string
import unicodedata


# def remove_accents(input_str):
#     nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
#     return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def remove_non_ascii_chars(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


def random_string(nr_chars=32):
    characters = string.ascii_letters + string.digits
    rs = "".join(random.choice(characters) for _ in range(nr_chars))
    return rs


def __remove_hex_chars_from_field(field):
    unprintable_chars = (char for char in field if char not in string.printable)
    for character in unprintable_chars:
        field = field.replace(character, "")
    return field


def remove_hex_chars(line):
    """Remove all non-printable characters from a string (list of words)."""

    line_after = map(__remove_hex_chars_from_field, line)
    return line_after


def generate_identifier(list_of_values, hashed=True):
    # Convert all values to strings
    list_of_strings = list()
    for val in list_of_values:
        list_of_strings.append(str(val))
    # Concatenate
    source_identifier = '_'.join(list_of_strings)
    if hashed:
        return hashlib.md5(source_identifier)
    else:
        return source_identifier


def substring_before_character(input_string, character, include_character=False, occurrence='FIRST'):
    """Return the substring before a certain character. Return None if the character does not occur."""
    if occurrence == 'FIRST':
        k = input_string.find(character)
    elif occurrence == 'LAST':
        k = input_string.rfind(character)
    else:
        msg = 'Occurrence {} not recognized. Shall be "FIRST" or "LAST"'.format(occurrence)
        raise AssertionError(msg)
    if k == -1:
        return None
    if include_character:
        k += 1
    new_string = input_string[:k]
    return new_string


def substring_after_character(input_string, character, include_character=False, occurrence='FIRST'):
    """Return the substring after a certain character. Return None if the character does not occur."""
    if occurrence == 'FIRST':
        k = input_string.find(character)
    elif occurrence == 'LAST':
        k = input_string.rfind(character)
    else:
        msg = 'Occurrence {} not recognized. Shall be "FIRST" or "LAST"'.format(occurrence)
        raise AssertionError(msg)
    if k == -1:
        return None
    if not include_character:
        k += 1
    new_string = input_string[k:]
    return new_string


def pretty_print(values, delimiter="|"):
    """pretty print lists and tuples"""
    print("=" * 80)
    if type(values) is dict:
        for key in values.keys():
            print("%-20s - %s" % (key, values[key]))
    for item in values:
        if type(item) in [list, tuple]:
            line = ""
            for i in range(0, len(item)):
                line += "%s %-20s" % (delimiter, item[i])
            print(line)
        else:
            print(item)
