#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:43$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

from ivonet.alphabet import *
from ivonet.calc import *
from ivonet.grid import *
from ivonet.hexadecimal import *
from ivonet.io import *
from ivonet.iter import *
from ivonet.primes import *
from ivonet.roman_numerals import *
from ivonet.str import *

__all__ = [
    # io
    "read_rows",
    "read_data",
    "read_ints",
    # calc
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
    # iter
    "consecutive_element_pairing",
    "plist",
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
]
