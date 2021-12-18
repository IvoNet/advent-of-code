#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
--- Day 18: Snailfish ---
You descend into the ocean trench and encounter some snailfish. They say they saw the sleigh keys! They'll even tell you which direction the keys went if you help one of the smaller snailfish with his math homework.

Snailfish numbers aren't like regular numbers. Instead, every snailfish number is a pair - an ordered list of two elements. Each element of the pair can be either a regular number or another pair.

Pairs are written as [x,y], where x and y are the elements within the pair. Here are some example snailfish numbers, one snailfish number per line:

[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]
This snailfish homework is about addition. To add two snailfish numbers, form a pair from the left and right parameters of the addition operator. For example, [1,2] + [[3,4],5] becomes [[1,2],[[3,4],5]].

There's only one problem: snailfish numbers must always be reduced, and the process of adding two snailfish numbers can result in snailfish numbers that need to be reduced.

To reduce a snailfish number, you must repeatedly do the first action in this list that applies to the snailfish number:

If any pair is nested inside four pairs, the leftmost such pair explodes.
If any regular number is 10 or greater, the leftmost such regular number splits.
Once no action in the above list applies, the snailfish number is reduced.

During reduction, at most one action applies, after which the process returns to the top of the list of actions. For example, if split produces a pair that meets the explode criteria, that pair explodes before other splits occur.

To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair (if any), and the pair's right value is added to the first regular number to the right of the exploding pair (if any). Exploding pairs will always consist of two regular numbers. Then, the entire exploding pair is replaced with the regular number 0.

Here are some examples of a single explode action:

[[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4] (the 9 has no regular number to its left, so it is not added to any regular number).
[7,[6,[5,[4,[3,2]]]]] becomes [7,[6,[5,[7,0]]]] (the 2 has no regular number to its right, and so it is not added to any regular number).
[[6,[5,[4,[3,2]]]],1] becomes [[6,[5,[7,0]]],3].
[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] (the pair [3,2] is unaffected because the pair [7,3] is further to the left; [3,2] would explode on the next action).
[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[7,0]]]].
To split a regular number, replace it with a pair; the left element of the pair should be the regular number divided by two and rounded down, while the right element of the pair should be the regular number divided by two and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.

Here is the process of finding the reduced result of [[[[4,3],4],4],[7,[[8,4],9]]] + [1,1]:

after addition: [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
after explode:  [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
after explode:  [[[[0,7],4],[15,[0,13]]],[1,1]]
after split:    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
after split:    [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
after explode:  [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
Once no reduce actions apply, the snailfish number that remains is the actual result of the addition operation: [[[[0,7],4],[[7,8],[6,0]]],[8,1]].

The homework assignment involves adding up a list of snailfish numbers (your puzzle input). The snailfish numbers are each listed on a separate line. Add the first snailfish number and the second, then add that result and the third, then add that result and the fourth, and so on until all numbers in the list have been used once.

For example, the final sum of this list is [[[[1,1],[2,2]],[3,3]],[4,4]]:

[1,1]
[2,2]
[3,3]
[4,4]
The final sum of this list is [[[[3,0],[5,3]],[4,4]],[5,5]]:

[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
The final sum of this list is [[[[5,0],[7,4]],[5,5]],[6,6]]:

[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
Here's a slightly larger example:

[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
The final sum [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] is found after adding up the above snailfish numbers:

  [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
+ [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
= [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]

  [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
+ [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
= [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]

  [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
+ [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
= [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]

  [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
+ [7,[5,[[3,8],[1,4]]]]
= [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]

  [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]
+ [[2,[2,2]],[8,[8,1]]]
= [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]

  [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
+ [2,9]
= [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]

  [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]
+ [1,[[[9,3],9],[[9,0],[0,7]]]]
= [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]

  [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]
+ [[[5,[7,4]],7],1]
= [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]

  [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
+ [[[[4,2],2],6],[8,7]]
= [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
To check whether it's the right answer, the snailfish teacher only checks the magnitude of the final sum. The magnitude of a pair is 3 times the magnitude of its left element plus 2 times the magnitude of its right element. The magnitude of a regular number is just that number.

For example, the magnitude of [9,1] is 3*9 + 2*1 = 29; the magnitude of [1,9] is 3*1 + 2*9 = 21. Magnitude calculations are recursive: the magnitude of [[9,1],[1,9]] is 3*29 + 2*21 = 129.

Here are a few more magnitude examples:

[[1,2],[[3,4],5]] becomes 143.
[[[[0,7],4],[[7,8],[6,0]]],[8,1]] becomes 1384.
[[[[1,1],[2,2]],[3,3]],[4,4]] becomes 445.
[[[[3,0],[5,3]],[4,4]],[5,5]] becomes 791.
[[[[5,0],[7,4]],[5,5]],[6,6]] becomes 1137.
[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] becomes 3488.
So, given this example homework assignment:

[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
The final sum is:

[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
The magnitude of this final sum is 4140.

Add up all of the snailfish numbers from the homework assignment in the order they appear. What is the magnitude of the final sum?
"""

import sys
import unittest
from pathlib import Path

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False


def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Pair:
    def __init__(self, left: int | None = None,
                 right: int | None = None,
                 left_pair: Pair | None = None,
                 right_pair: Pair | None = None,
                 parent: Pair | None = None,
                 depth: int = 0) -> None:
        self.left: int | None = left
        self.right: int | None = right
        self.left_pair: Pair | None = left_pair
        self.right_pair: Pair | None = right_pair
        self.parent: Pair | None = parent
        self.depth: int = depth

    def __str__(self) -> str:
        return visualize(self)

    def __repr__(self) -> str:
        return f"Pair(left={self.left}, right={self.right}, " \
               f"left_pair={self.left_pair}, right_pair={self.right_pair}, " \
               f"depth={self.depth}, parent={'...' if self.parent else None})"


def visualize(sfn: Pair):
    """if you want to debug and visualize the snailfish number"""
    ret = "["
    if sfn.left is not None:
        ret += f"{sfn.left}"
    else:
        ret += visualize(sfn.left_pair)
    ret += ","
    if sfn.right is not None:
        ret += f"{sfn.right}"
    else:
        ret += visualize(sfn.right_pair)
    ret += "]"
    return ret


def string_to_snailfish_number(value) -> list:
    """Make a list of the string
    Easy as it is already in a python format just eval
    """
    return eval(value)


def parse(sfn: list, depth: int = 0, parent: [Pair | None] = None) -> [Pair | None]:
    """Parse the lists into a pair tree
    """
    _("parse:", sfn)
    ret = Pair(parent=parent, depth=depth)
    # left (zero index)
    if type(sfn[0]) == list:
        _("parse:", "left_pair")
        ret.left_pair = parse(sfn[0], depth + 1, ret)
    else:  # plain number
        _("parse:", "left value", sfn[0])
        ret.left = sfn[0]
    # right (index 1)
    if type(sfn[1]) == list:
        _("parse:", "right_pair")
        ret.right_pair = parse(sfn[1], depth + 1, ret)
    else:
        _("parse:", "right value", sfn[1])
        ret.right = sfn[1]

    return ret


def update_depths(sfn: Pair) -> Pair:
    """Updates the depths of all the pairs when moved down a level (after addition)
    """
    sfn.depth += 1
    _("update_depths:", sfn)
    if sfn.left_pair is not None:
        _("update_depths:", "left_pair")
        sfn.left_pair = update_depths(sfn.left_pair)
    if sfn.right_pair is not None:
        _("update_depths:", "right_pair")
        sfn.right_pair = update_depths(sfn.right_pair)
    return sfn


def update_down_right(sfn: Pair, value: int):
    """Updating down right
    - add the value if it its left value already has meaning
    - otherwise walk down the left side until you can do this
    """
    if sfn.left is not None:
        sfn.left += value
    else:
        update_down_right(sfn.left_pair, value)


def update_up_right(sfn: Pair, value: int):
    """Update up right
    - now you have to look down as we need to
    """
    _("update_up_right:", visualize(sfn), value)
    parent: Pair = sfn.parent
    if parent is None:
        _("update_up_right:", "No parent")
        return
    if parent.left_pair == sfn:
        _("update_up_right:", "left_pair == sfn")
        if parent.right is not None:
            _("update_up_right:", "setting parent.right =", value)
            parent.right += value
        else:
            update_down_right(parent.right_pair, value)
    elif parent.right_pair == sfn:
        update_up_right(parent, value)
    else:
        _("update_up_right:", "No parent to update")


def update_down_left(sfn: Pair, value: int):
    """Updating down left
    - should always find something
    - start from right as that will eventually give a value
    """
    if sfn.right is not None:
        sfn.right += value
    else:
        update_down_left(sfn.right_pair, value)


def update_up_left(sfn: Pair, value: int):
    """Up left update
    - left should aways have a parent as it is at depth >= 4
    - add if left value else 0
    """
    parent: Pair = sfn.parent
    if parent is None:
        _("update_up_left:", "No parent")
        return
    if parent.right_pair == sfn:
        _("update_up_left:", "right_pair == sfn")
        if parent.left is not None:
            _("update_up_left:", "setting parent.left =", value)
            parent.left += value
        else:
            update_down_left(parent.left_pair, value)
    elif parent.left_pair == sfn:
        update_up_left(parent, value)
    else:
        _("update_up_left:", "No parent to update")


def explode(sfn: Pair) -> bool:
    """Explode function.
    We explode when:
    - a depth >= 4
    - our left and right values not empty
    """
    _("explode:", str(sfn))
    if sfn.depth >= 4 and sfn.left is not None and sfn.right is not None:
        _("explode:", "Depth found:", repr(sfn))
        # should there always be a parent? yes as we have a depth of more than 4
        update_up_left(sfn, sfn.left)
        update_up_right(sfn, sfn.right)

        if sfn.parent.left_pair == sfn:
            sfn.parent.left_pair = None
            sfn.parent.left = 0
        elif sfn.parent.right_pair == sfn:
            sfn.parent.right_pair = None
            sfn.parent.right = 0
        else:
            _("Explode: no parent to clean", sfn)
            return False
        return True
    if sfn.left_pair is not None and explode(sfn.left_pair):
        return True
    if sfn.right_pair is not None and explode(sfn.right_pair):
        return True
    return False


def split_it(sfn: Pair) -> bool:
    """Splitting it
    - from left to right the first one bigger than 9
        - left div 2 (rounded down)
        - right div 2 (rounded up) -> effectively sfn.right - left
    - act on ourselves first
    the returning bool tells if a split has taken place or not
    """
    _("split:", sfn)
    if sfn.left is not None and sfn.left > 9:
        _("split:", "left split:", sfn)
        left = sfn.left // 2
        right = sfn.left - left
        sfn.left_pair = Pair(left=left, right=right, parent=sfn, depth=sfn.depth + 1)
        sfn.left = None
        _("split:", "becomes   :", sfn)
        return True
    if sfn.left_pair is not None and split_it(sfn.left_pair):  # Possible recursion here
        return True
    if sfn.right is not None and sfn.right > 9:
        _("split:", "right split: ", sfn)
        left = sfn.right // 2
        right = sfn.right - left
        sfn.right_pair = Pair(left=left, right=right, parent=sfn, depth=sfn.depth + 1)
        sfn.right = None
        _("split:", "becomes    :", sfn)
        return True
    if sfn.right_pair is not None and split_it(sfn.right_pair):  # Possible recursion here
        return True
    return False


def sfn_reduce(sfn: Pair) -> None:
    """Starfish number reduce function
    - one action at the time
    - explode has precedence over split
    - repeat until no reduce actions left
      this happens when split returns false
    """
    _("reduce:", sfn)
    while True:
        action_performed = explode(sfn)
        if action_performed:
            _("reduce:", "exploded:", sfn)
            continue
        action_performed = split_it(sfn)
        if not action_performed:
            break
        else:
            _("reduce:", "split:", sfn)


def addition(left: Pair, right: Pair):
    """
    [[[[4,3],4],4],[7,[[8,4],9]]] + [1,1]

    0            p                  p
               /   \               / \
    1         p     p             1   1
            /  \   / \      +
    2      p    4 7   p
          / \        / \
    3    p   4      p   9
        / \        / \
       4   3      8   4


    first action: addition

    - new Pair (depth 0)
        - with left_pair the original pair
        - with right the new pair

    0                  p (top)
                  /        \
    1            p (orig)   p (new)
               /   \       / \
    2         p     p     1   1
            /  \   / \
    3      p    4 7   p
          / \        / \
    4    p   4      p   9
        / \        / \
       4   3      8   4

    - all original pairs (left_pair) have a new depth +1
    - the orig needs to have its parent assigned to the new top pair
        - top.left_pair.parent := top
        - top.right_pair.parent := top
    """
    _("addition:", left, "+", right)
    top = Pair(left_pair=update_depths(left), right_pair=update_depths(right))

    top.left_pair.parent = top
    top.right_pair.parent = top

    # pair_print(top)
    sfn_reduce(top)
    return top


def magnitude(sfn: Pair) -> int:
    total = 0
    if sfn.left is not None:
        total += 3 * sfn.left
    else:
        total += 3 * magnitude(sfn.left_pair)
    if sfn.right is not None:
        total += 2 * sfn.right
    else:
        total += 2 * magnitude(sfn.right_pair)
    return total


def sum_all(snailfish_numbers):
    sf_sum = snailfish_numbers[0]
    for i, sfn in enumerate(snailfish_numbers):
        if i == 0:  # skip as we already assigned it to have a starting point
            continue
        sf_sum = addition(sf_sum, sfn)
    _("sum_all:", "result", sf_sum)
    return sf_sum


def parse_all(source):
    snailfish_numbers: list[Pair] = []
    for s in source:
        snailfish_numbers.append(parse(string_to_snailfish_number(s), depth=0, parent=None))
    return snailfish_numbers


def part_1(source):
    snailfish_numbers = parse_all(source)

    sf_sum = sum_all(snailfish_numbers)

    return magnitude(sf_sum)


def part_2(source):
    max_magnitude = 0
    for i, x in enumerate(source):
        for j, y in enumerate(source):
            if i == j:
                continue
            x_snf = parse(string_to_snailfish_number(x), depth=0, parent=None)
            y_snf = parse(string_to_snailfish_number(y), depth=0, parent=None)
            add = addition(x_snf, y_snf)
            mt = magnitude(add)

            if mt > max_magnitude:
                _(visualize(add))
                max_magnitude = mt
    return max_magnitude


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = ints(Path(__file__).name)[0]
        self.source = read_rows(f"day_{day}.txt")
        self.test_source = read_rows("""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""")

    def test_explode_1(self):
        pair = parse([[[[[9, 8], 1], 2], 3], 4])
        self.assertTrue(explode(pair))
        self.assertEqual("[[[[0,9],2],3],4]", visualize(pair))

    def test_explode_2(self):
        pair = parse([7, [6, [5, [4, [3, 2]]]]])
        self.assertTrue(explode(pair))
        self.assertEqual("[7,[6,[5,[7,0]]]]", visualize(pair))

    def test_explode_3(self):
        pair = parse([[6, [5, [4, [3, 2]]]], 1])
        self.assertTrue(explode(pair))
        self.assertEqual("[[6,[5,[7,0]]],3]", visualize(pair))

    def test_explode_4(self):
        pair = parse([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
        self.assertTrue(explode(pair))
        self.assertEqual("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", visualize(pair))

    def test_explode_5(self):
        pair = parse([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])
        self.assertTrue(explode(pair))
        self.assertEqual("[[3,[2,[8,0]]],[9,[5,[7,0]]]]", visualize(pair))

    def test_split_1(self):
        pair = parse([[[[0, 7], 4], [15, [0, 13]]], [1, 1]])
        self.assertTrue(True, split_it(pair))
        self.assertEqual("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", visualize(pair))
        self.assertTrue(True, split_it(pair))
        self.assertEqual("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]", visualize(pair))

    def test_split_(self):
        pair = parse([[[[0, 7], 4], [15, [0, 13]]], [1, 1]])
        self.assertTrue(True, split_it(pair))
        self.assertEqual("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", visualize(pair))

    def test_magnitude_1(self):
        sfn = parse([[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]])
        self.assertEqual(4140, magnitude(sfn))

    def test_magnitude_2(self):
        sfn = parse([[1, 2], [[3, 4], 5]])
        self.assertEqual(143, magnitude(sfn))

    def test_magnitude_3(self):
        sfn = parse([[[[1, 1], [2, 2]], [3, 3]], [4, 4]])
        self.assertEqual(445, magnitude(sfn))

    def test_magnitude_4(self):
        sfn = parse([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])
        self.assertEqual(1384, magnitude(sfn))

    def test_magnitude_5(self):
        sfn = parse([[[[3, 0], [5, 3]], [4, 4]], [5, 5]])
        self.assertEqual(791, magnitude(sfn))

    def test_magnitude_6(self):
        sfn = parse([[[[5, 0], [7, 4]], [5, 5]], [6, 6]])
        self.assertEqual(1137, magnitude(sfn))

    def test_magnitude_(self):
        sfn = parse([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]])
        self.assertEqual(3488, magnitude(sfn))

    def test_visualize(self):
        s = "[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]"
        pair = parse(string_to_snailfish_number(s))
        self.assertEqual(s, visualize(pair))

    def test_small_data_set(self):
        s = parse_all(read_rows("""[1,1]
[2,2]
[3,3]
[4,4]"""))
        self.assertEqual("[[[[1,1],[2,2]],[3,3]],[4,4]]", visualize(sum_all(s)))

    def test_small_data_set_1(self):
        s = parse_all(read_rows("""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]"""))
        self.assertEqual("[[[[3,0],[5,3]],[4,4]],[5,5]]", visualize(sum_all(s)))

    def test_small_data_set_2(self):
        s = parse_all(read_rows("""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]"""))
        self.assertEqual("[[[[5,0],[7,4]],[5,5]],[6,6]]", visualize(sum_all(s)))

    def test_example_data_part_1(self):
        self.assertEqual(4140, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(3654, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(3993, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(4578, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
