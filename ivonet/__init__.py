#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:43$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
    # files
    "read_rows",
    "read_data",
    "read_ints",
    "read_int_matrix",
    # iter
    "consecutive_element_pairing",
    "sort_dict_on_values",
    "lmap",
    "pretty",
    "flatten",
    "min_max",
    "max_minus_min",
    "list_diff",
    "ints",
    "floats",
    "positive_floats",
    "words",
    "keyvalues",
    "make_hashable",
    "invert_dict",
    # calc
    "prod",
    "fibonacci",
    "step_sequence_calc",
    "normalize_overlap_matrix",
    "ternary",
    "base_3",
    "base_x_to_10",
    "binary_8_bits",
    "base_10_to_base_x",
    # str
    "sort_str",
    "is_sorted",
    "letters",
    "str_minus_len",
    "str_minus_str",
    "read_european_number",
    # primes
    "prime_factors",
    "prime_factors_unique",
    "is_prime",
    "find_smallest_factor",
    "prime_factorization",
    # roman_numerals
    "int_2_roman",
    "romain_2_int",
    "roman",
    "write_roman",
    "small_int_to_roman",
    "big_int_to_roman",
    "roman_to_int",
    "int_to_roman",
    # grid
    "neighbors",
    # alphabet
    "alphabet",
    "alphabet_idx",
    "alphabet_loc",
    "alphabet_list",
    "base_26_encode_string",
    "letter_values_of_word",
    "sum_letter_values_of_word",
    "product_letter_values_of_word",
    "print_alphabet",
    # hexadecimal
    "number_as_word",
"""

import sys

sys.setrecursionlimit(100000)

__all__ = [
    "open",
]

infinite = float("inf")


def open(source):
    """URI, filename, or string --> stream
    This open function lets you define parsers that take any input source
    (URL, pathname to local or network file, or actual data as a string)
    and deal with it in a uniform manner.  Returned object is guaranteed
    to have all the basic stdio read methods (read, readline, readlines).
    Just .close() the object when you're done with it.
    """
    from ivonet.files import open_anything
    return open_anything(source)
