#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 07/12/2021 22:15$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import numpy as np


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


def normalize_overlap_matrix(mtrx):
    """
    Normalizes a numpy matrix used for overlap matrices,
    by dividing every element A_ij by sqrt(A_ii)*sqrt(A_jj)
    """
    assert isinstance(mtrx, np.ndarray), 'Input shall be a numpy array'
    assert np.isreal(mtrx).all(), 'Numpy array shall contain real numbers'
    assert mtrx.shape[0] == mtrx.shape[1], 'Overlap matrix shall be square'
    assert (np.diag(mtrx) != 0).all(), 'Overlap matrix shall not have 0 on its diagonal'

    b = np.sqrt(np.diag(mtrx))
    result = ((mtrx / b).T / b).T

    return result
