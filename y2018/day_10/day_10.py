#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """"""

import os
import sys
import unittest
from itertools import count
from pathlib import Path
from typing import NamedTuple

from ivonet import infinite
from ivonet.files import read_rows
from ivonet.iter import ints, rangei

sys.dont_write_bytecode = True

DEBUG = False


# noinspection DuplicatedCode
def _(*args, end="\n"):
    if DEBUG:
        print(" ".join(str(x) for x in args), end=end)


class Light(NamedTuple):
    x: int
    y: int
    vx: int
    vy: int


class Coord(NamedTuple):
    x: int
    y: int


def parse(source):
    return [Light(*ints(line)) for line in source]


def lights_state(lights: list[Light], seconds) -> set[Coord]:
    """The positions of the lights at a certain second interval"""
    return {Coord(light.x + seconds * light.vx, light.y + seconds * light.vy) for light in lights}


def bounds(dots: set[Coord]) -> tuple[int, ...]:
    """The upper and lower bounds of the given lights coordinates."""
    return (min(dot.x for dot in dots), max(dot.x for dot in dots),
            min(dot.y for dot in dots), max(dot.y for dot in dots))


def bounded_box(dots):
    """The bounded box in which the lights 'live'"""
    xmin, xmax, ymin, ymax = bounds(dots)
    return (xmax - xmin) * (ymax - ymin)


def visualize(dots: set[Coord]):
    ret = ""
    x_min, x_max, y_min, y_max = bounds(dots)
    for y in rangei(y_min, y_max):
        for x in rangei(x_min, x_max):
            ret += "#" if Coord(x, y) in dots else " "
        ret += "\n"
    return ret


def min_state(lights):
    previous = infinite
    for seconds in count(0):
        state = bounded_box(lights_state(lights, seconds=seconds))
        if previous < state:
            return seconds - 1
        previous = state


def part_1(source):
    """Ok the idea is to move them incrementally based on their velocity until we read a message
    That seems doable but how to figure out when to stop and read the message? Observations
    - moving from far apart to nearer to each other. Is the minimal distance something to work
      with here?
    - so I assume (ass u me) for now (educated guess) that When the bounded box is at its smallest
      we have a readable text?!
    - lets go for that for now
    """
    lights = parse(source)
    minimal_bounded_box = min_state(lights)
    minimal_state = lights_state(lights, minimal_bounded_box)
    result = visualize(minimal_state)
    print(result)
    return result


def part_2(source):
    lights = parse(source)
    return min_state(lights)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}_test.input")

    def test_example_data_part_1(self):
        self.assertEqual("""#   #  ###
#   #   # 
#   #   # 
#####   # 
#   #   # 
#   #   # 
#   #   # 
#   #  ###
""", part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual("""#    #  ######  #    #  #####   #       #####   #    #  #    #
##   #  #       #    #  #    #  #       #    #  #    #  #   # 
##   #  #        #  #   #    #  #       #    #   #  #   #  #  
# #  #  #        #  #   #    #  #       #    #   #  #   # #   
# #  #  #####     ##    #####   #       #####     ##    ##    
#  # #  #         ##    #       #       #  #      ##    ##    
#  # #  #        #  #   #       #       #   #    #  #   # #   
#   ##  #        #  #   #       #       #   #    #  #   #  #  
#   ##  #       #    #  #       #       #    #  #    #  #   # 
#    #  ######  #    #  #       ######  #    #  #    #  #    #
""", part_1(self.source))

    def test_part_2(self):
        self.assertEqual(10459, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
