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
sys.setrecursionlimit(10000000)

DEBUG = False


def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Pair:
    left: int | None = None
    right: int | None = None
    left_pair: Pair | None = None
    right_pair: Pair | None = None
    depth: int = 0
    parent: Pair | None = None


def pair_print(sfn: Pair):
    print("[", end="")
    if sfn.left is not None:
        print(f"{sfn.left}", end="")
    else:
        pair_print(sfn.left_pair)
    print(",", end="")
    if sfn.right is not None:
        print(f"{sfn.right}", end="")
    else:
        pair_print(sfn.right_pair)
    print("]", end="")


def string_to_snailfish_number(value) -> list:
    return eval(value)


def parse(sfn: list, depth: int = 0, parent: [Pair | None] = None) -> [Pair | None]:
    """Parse the lists into a pair tree
    """
    ret = Pair()
    ret.depth = depth
    ret.parent = parent
    # left (zero index)
    if type(sfn[0]) == list:
        ret.left_pair = parse(sfn[0], depth + 1, ret)
    else:  # plain number
        ret.left = sfn[0]
    # right (index 1)
    if type(sfn[1]) == list:
        ret.right_pair = parse(sfn[1], depth + 1, ret)
    else:
        ret.right = sfn[1]

    return ret


def update_depths(sfn: Pair) -> Pair:
    sfn.depth += 1
    if sfn.left_pair is not None:
        sfn.left_pair = update_depths(sfn.left_pair)
    if sfn.right_pair is not None:
        sfn.right_pair = update_depths(sfn.right_pair)
    return sfn


def update_down_right(sfn: Pair, value: int):
    """Updating down right"""
    # _("Updating down right")
    if sfn.left is not None:
        sfn.left += value
    else:
        update_down_right(sfn.left_pair, value)


def update_up_right(sfn: Pair, value: int):
    """Update up right
    """
    # _("Update up right")
    parent: Pair = sfn.parent
    if parent is None:
        _("Update up right: No parent found")
        return
    if parent.left_pair == sfn:
        if parent.right is not None:
            parent.right += value
        else:
            update_down_right(parent.right_pair, value)
    elif parent.right_pair == sfn:
        update_up_right(parent, value)
    else:
        _("Update up right: No parent to update?!")


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
        _("Update up left: No parent found")
        return
    if parent.right_pair == sfn:
        if parent.left is not None:
            parent.left += value
        else:
            update_down_left(parent.left_pair, value)
    elif parent.left_pair == sfn:
        update_up_left(parent, value)
    else:
        _("Update up left: No parent to update?!")


def explode(sfn: Pair) -> bool:
    """Explode function.
    We explode when:
    - a depth >= 4
    - our left and right values not empty
    """
    if sfn.depth >= 4 and sfn.left is not None and sfn.right is not None:
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
            _("Explode: no parent to delete?!", sfn)
            return False
        return True
    if sfn.left_pair is not None and explode(sfn.left_pair):
        return True
    if sfn.right_pair is not None and explode(sfn.right_pair):
        return True
    return False


def split_it(sfn: Pair) -> bool:
    """Splitting it
    - from left to right
    - act on ourselves
    - redepth?!
    """
    if sfn.left is not None and sfn.left > 9:
        left = sfn.left // 2
        right = sfn.left - left
        sfn.left_pair = Pair()
        sfn.left_pair.left = left
        sfn.left_pair.right = right
        sfn.left_pair.depth = sfn.depth + 1
        sfn.left_pair.parent = sfn
        sfn.left = None
        return True
    if sfn.left_pair is not None and split_it(sfn.left_pair):
        return True
    if sfn.right is not None and sfn.right > 9:
        left = sfn.right // 2
        right = sfn.right - left
        sfn.right_pair = Pair()
        sfn.right_pair.left = left
        sfn.right_pair.right = right
        sfn.right_pair.depth = sfn.depth + 1
        sfn.right_pair.parent = sfn
        sfn.right = None
        return True
    if sfn.right_pair is not None and split_it(sfn.right_pair):
        return True
    return False


def sfn_reduce(sfn: Pair) -> Pair:
    """Starfish number reduce function
    - one action at the time
    - explode has precedence over split
    - repeat until no reduce actions left
      this happens when split returns false
    """
    while True:
        action_performed = explode(sfn)
        if action_performed:
            continue
        action_performed = split_it(sfn)
        if not action_performed:
            break


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
    top = Pair()
    top.left = None
    top.right = None
    top.parent = None
    top.depth = 0
    top.left_pair = update_depths(left)
    top.right_pair = update_depths(right)

    top.left_pair.parent = top
    top.right_pair.parent = top

    # pair_print(top)
    sfn_reduce(top)
    return top


def part_1(source):
    snailfish_numbers: list[Pair] = []
    for s in source:
        snailfish_numbers.append(parse(string_to_snailfish_number(s), depth=0, parent=None))
    _("Numbers:", snailfish_numbers)

    sf_sum = snailfish_numbers[0]
    for i, sfn in enumerate(snailfish_numbers):
        if i == 0:  # skip as we already assigned it to have a starting point
            continue
        _("Addition of", sf_sum, "and", sfn)
        sf_sum = addition(sf_sum, sfn)

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
            # pair_print(add)
            mt = magnitude(add)

            if mt > max_magnitude:
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

    def test_split_(self):
        pair = parse([[[[0, 7], 4], [15, [0, 13]]], [1, 1]])
        print(split_it(pair))
        pair_print(pair)
        self.assertEqual(True, True)

    def test_magnitude(self):
        sfn = parse([[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]])
        self.assertEqual(4140, magnitude(sfn))

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
