#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from unittest import TestCase, main

from ivonet.alphabet import base_26_encode_string, sum_letter_values_of_word, alphabet, product_letter_values_of_word, \
    base_26_decode_string
from ivonet.calc import base_10_to_base_x, base_3
from ivonet.cdll import CircularDoublyLinkedList
from ivonet.hexa import number_as_word
from ivonet.iter import consecutive_element_pairing
from ivonet.roman_numerals import roman
from ivonet.str import sort_str, is_sorted, letters, OpenCloseTags, TagError

TAG_ERROR = "Should have raised a TagError"


class TestBase(TestCase):
    def test_base_10_to_x(self):
        self.assertTrue(base_10_to_base_x("102", 3) == "11")

    def test_base_3(self):
        self.assertEqual(base_3(102), "11")


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


class UnitTests(TestCase):
    def test_consecutive_element_paring(self):
        self.assertEqual(consecutive_element_pairing([1, 2, 3, 4, 5, 6], elements=7, map_to_func=list), [])
        self.assertEqual(consecutive_element_pairing([1, 2, 3, 4, 5, 6], elements=3, map_to_func=list),
                         [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]])
        # first pair to the list ^^^ then sum the the separate sub lists and make that into a list
        self.assertEqual(consecutive_element_pairing([1, 2, 3, 4, 5, 6], elements=3, map_to_func=sum),
                         [6, 9, 12, 15])
        self.assertEqual(
            consecutive_element_pairing([1, 2, 3, 4, 5, 6], elements=3,
                                        map_to_func=lambda z: "".join([str(x) for x in z])),
            ['123', '234', '345', '456'])


class TestAlphabet(TestCase):
    def test_base_26_encoded(self):
        self.assertEqual(0, base_26_encode_string("A"))
        self.assertEqual(1, base_26_encode_string("B"))
        self.assertEqual(25, base_26_encode_string("z"))
        self.assertEqual(26, base_26_encode_string("ba"))
        self.assertEqual(16197, base_26_encode_string("XYZ"))
        self.assertEqual(3296799508237, base_26_encode_string("PUMEGENMB"))
        self.assertEqual(9849791328331451697274678861440325, base_26_encode_string(alphabet()))
        self.assertEqual(
            20569858802338608448364049446852061780140090404415032130205785332253615286792604334631099850853638206681253072973938092469074262459481025482721597642516904700401181296799991465053389302729514,
            base_26_encode_string(
                "FCJNIPMLEEUHUATKMSOZUTXLEZBBFTLKYHXLLORKXQDDIFJCDCZGJWANKVALRMVNZSDRRHDXEICQVBSLUKKLYVEWGGFOKUHEBPHIHLIJPXTQEOANYBDOIWPLKRLVNXTKVGBCDSK"))

    def test_base_26_decoded(self):
        self.assertEqual("A", base_26_decode_string(0))
        self.assertEqual("PUMEGENMB", base_26_decode_string(3296799508237))
        self.assertEqual(9849791328331451697274678861440325, base_26_encode_string(alphabet()))
        self.assertEqual(
            "FCJNIPMLEEUHUATKMSOZUTXLEZBBFTLKYHXLLORKXQDDIFJCDCZGJWANKVALRMVNZSDRRHDXEICQVBSLUKKLYVEWGGFOKUHEBPHIHLIJPXTQEOANYBDOIWPLKRLVNXTKVGBCDSK",
            base_26_decode_string(
                20569858802338608448364049446852061780140090404415032130205785332253615286792604334631099850853638206681253072973938092469074262459481025482721597642516904700401181296799991465053389302729514
            ))

    def test_sum_letter_values_of_word(self):
        self.assertEqual(3, sum_letter_values_of_word("aaa"))
        self.assertEqual(27, sum_letter_values_of_word("az"))
        self.assertEqual(25, sum_letter_values_of_word("az", 0))
        self.assertEqual(351, sum_letter_values_of_word(alphabet()))

    def test_product_letter_values_of_word(self):
        self.assertEqual(403291461126605635584000000, product_letter_values_of_word(alphabet()))


class StringFunctions(TestCase):
    def test_sort_alphanumerical(self):
        self.assertEqual("abdij", sort_str("abdij"))
        self.assertEqual("jidba", sort_str("abdij", True))

    def test_is_sorted(self):
        self.assertFalse(is_sorted("za"))
        self.assertTrue(is_sorted("za", True))
        self.assertTrue(is_sorted("aabbccdd"))

    def test_letters(self):
        self.assertEqual("HW", letters("Hallo Wereld"))
        self.assertEqual("ae", letters("Hallo Wereld", 1))

    def test_open_close_tags(self):
        oc = OpenCloseTags("<<<((({{{[[[]]]}}})))>>>")
        self.assertTrue(oc.is_valid())
        self.assertEqual({'actual': None,
                          'expected': None,
                          'incomplete': '',
                          'source': '<<<((({{{[[[]]]}}})))>>>',
                          'valid': True}, oc.meta())
        oc = OpenCloseTags("<]")
        self.assertFalse(oc.is_valid())
        self.assertEqual({'actual': ']',
                          'expected': '>',
                          'incomplete': '',
                          'source': '<]',
                          'valid': False}, oc.meta())
        oc = OpenCloseTags("<>>")
        self.assertFalse(oc.is_valid())
        oc = OpenCloseTags("""=/;:?+""", tags="/?;:=+")
        self.assertTrue(oc.is_valid())

    def test_open_closet_tags_exception(self):
        try:
            OpenCloseTags("<>>", exception=True)
            self.fail(TAG_ERROR)
        except TagError as e:
            self.assertEqual("Expected to be finished, but found > instead.", str(e))
            self.assertEqual(">", e.actual)

        try:
            OpenCloseTags("<]", exception=True)
            self.fail(TAG_ERROR)
        except TagError as e:
            self.assertEqual(">", e.expected)
            self.assertEqual("]", e.actual)
            self.assertEqual("Expected >, but found ] instead.", str(e))

        try:
            OpenCloseTags("<[{()()", exception=True)
            self.fail(TAG_ERROR)
        except TagError as e:
            self.assertEqual("}]>", e.incomplete)
            self.assertEqual("Expected these closing tags '}]>'.", str(e))


class CircularDoublyLinkedListTests(TestCase):

    def setUp(self) -> None:
        self.cdll = CircularDoublyLinkedList()

    def test_cdll_1(self):
        self.cdll.extend(range(100))
        self.cdll.append("A")
        self.cdll.previous()
        self.assertEqual("A", self.cdll.get())
        self.assertEqual(101, len(self.cdll))

    def test_cdll_remove(self):
        self.cdll.append(1)
        self.assertEqual(1, len(self.cdll))
        self.cdll.remove_index(0)
        self.assertEqual(0, len(self.cdll))
        self.cdll.remove_index(0)
        self.assertEqual(0, len(self.cdll))

    def test_cdll_subscriptable(self):
        self.cdll.append(1)
        self.cdll.append(2)
        self.assertEqual(1, self.cdll[0])
        self.assertEqual(1, self.cdll[2])
        self.assertEqual(1, self.cdll[4])
        self.assertEqual(2, self.cdll[1])
        self.assertEqual(2, self.cdll[3])

    def test_next(self):
        self.cdll.extend(range(200))
        [self.cdll.next() for _ in range(50)]
        self.assertEqual(50, self.cdll.get())

    def test_previous(self):
        self.cdll.extend(range(200))
        [self.cdll.previous() for _ in range(50)]
        self.assertEqual(150, self.cdll.get())

    def test_remove(self):
        self.cdll.extend(range(2))
        self.cdll.remove(self.cdll.node(0))
        self.cdll.remove(self.cdll.node(0))
        self.cdll.remove(self.cdll.node(0))
        self.assertEqual(None, self.cdll.get())

    def test_remove_current(self):
        self.cdll.extend(range(5))
        current = self.cdll.next()
        self.cdll.remove(current)
        self.assertEqual(2, self.cdll.get())

    def test_popleft(self):
        self.cdll.extend(range(5))
        self.cdll.node(4)
        self.assertEqual(0, self.cdll.popleft())
        self.assertEqual(1, self.cdll.popleft())
        self.assertEqual(2, self.cdll[0])
        self.assertEqual(3, len(self.cdll))
        self.cdll.previous()
        self.assertEqual(3, self.cdll.get())


if __name__ == "__main__":
    main()
