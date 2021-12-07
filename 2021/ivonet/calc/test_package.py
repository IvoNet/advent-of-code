#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from unittest import main, TestCase

import numpy as np

from ivonet.calc import normalize_overlap_matrix
from ivonet.calc.base import base_10_to_base_x, base_3
from ivonet.calc.hexadecimal import number_as_word
from ivonet.calc.roman_numerals import roman


class TestBase(TestCase):
    def test_base_10_to_x(self):
        self.assertTrue(base_10_to_base_x("102", 3) == "11")

    def test_base_3(self):
        self.assertEqual(base_3("102"), "11")


class TestNormalizeOverlapMatrix(TestCase):
    def test_gw_01(self):
        a = np.ones(shape=[4, 4]) + 3 * np.eye(4)
        a[0, 0] = 100
        a[3, 3] = 25
        a[0, 3] = 16
        r = normalize_overlap_matrix(a)
        e = np.matrix([[1., 0.05, 0.05, 0.32],
                       [0.05, 1., 0.25, 0.1],
                       [0.05, 0.25, 1., 0.1],
                       [0.02, 0.1, 0.1, 1.]])
        np.testing.assert_array_almost_equal(r, e)

    def test_bw_01(self):
        """Verify that an error is raised if there is a zero on the diagonal"""
        with self.assertRaisesRegex(AssertionError, 'diagonal'):
            a = np.reshape(np.arange(16), [4, 4])
            normalize_overlap_matrix(a)

    def test_bw_02(self):
        """Verify that an error is raised if the overlap matrix is not square."""
        with self.assertRaisesRegex(AssertionError, 'square'):
            a = np.matrix(np.arange(1, 5))
            normalize_overlap_matrix(a)


class TestHexadecimal(TestCase):
    def test_number_as_word(self):
        self.assertEqual("SOCIAAL", number_as_word(84679335))
        self.assertEqual("BELEID", number_as_word(12484125))
        self.assertEqual("ALS", number_as_word(2677))
        self.assertEqual("BASISFILOSOFIE", number_as_word(52443814518132510))
        self.assertEqual("IS", number_as_word(21))
        self.assertEqual("GOEDBEDOELDE", number_as_word(159350783010782))
        self.assertEqual("IDEOLOGIE", number_as_word(8019970334))
        self.assertEqual("DE", number_as_word(222))
        self.assertEqual("BIOLOGE", number_as_word(185626782))
        self.assertEqual("ZAG", number_as_word(681))
        self.assertEqual("ZES", number_as_word(741))
        self.assertEqual("DEZELFDE", number_as_word(3727589342))
        self.assertEqual("BOLACCACIAS", number_as_word(12127591645605))


class TestRomanConversion(TestCase):
    def setUp(self):
        self.numbers = [(1, 'I'), (3, 'III'), (4, 'IV'), (27, 'XXVII'), (44, 'XLIV'),
                        (93, 'XCIII'), (141, 'CXLI'), (402, 'CDII'), (575, 'DLXXV'),
                        (1024, 'MXXIV'), (3000, 'MMM')]

    def test_to_roman(self):
        for num in self.numbers:
            self.assertEqual(num[0], roman(num[1]))

    def test_to_arabic(self):
        for num in self.numbers:
            self.assertEqual(num[1], roman(num[0]))


if __name__ == '__main__':
    main()
