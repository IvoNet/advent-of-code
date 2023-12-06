#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2023 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import sys
import unittest
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows, read_data
from ivonet.iter import ints, lmap, chunkify

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


class Range(NamedTuple):
    """
    Represents a range
    """
    destination: int
    source: int
    length: int


class Seed(NamedTuple):
    start: int
    end: int


class Almanac(object):
    """
    The Almanac is a collection of maps that can be used to transform a seed into a location.
    The trouble is that the ranges are much too big to iterate over, so we need to find a way to
    find the location in a more efficient way.
    """

    def __init__(self, source):
        """
        The source is a text containing blocks. The first block is the seeds block and the rest are
        the maps.
        :param source:
        """
        seeds, *blocks = source.split("\n\n")
        self.maps = blocks
        self.seeds = lmap(int, seeds.split(":")[1].split())

    @staticmethod
    def parse_ranges(block) -> list[Range]:
        """
        This method parses the ranges for a given block.
        """
        ranges = []
        # skip the first line as it contains the map name, and we do not need it.
        for line in block.splitlines()[1:]:
            ranges.append(Range(*lmap(int, line.split())))
        _(ranges)
        return ranges

    def find_nearest_seed_location(self):
        """
        This method will find the nearest seed location for the given seed.
        it does this by iterating over the maps and transforming the seed into a location.
        - parse the ranges for the map
        - iterate over the seed locations
        - iterate over the ranges
        - if the location is in the range then transform to the new mapping and break
        - else keep the location as the seed location

        the offset is calculated:
        e.g. 50 98 2
        50 is the destination start
        98 is the source start
        2 is the length of the ranges
        so seed 98 corresponds to 50 and 99 corresponds to 51
        so the offset is 98 - 50 = 48 so the formula is:
        location - source + destination = offset
        """
        locations = self.seeds
        for block in self.maps:
            _(block)
            ranges: list[Range] = self.parse_ranges(block)
            new_seed: list[Seed] = []
            for location in locations:
                for rng in ranges:
                    if location in range(rng.source, rng.source + rng.length):  # dst <= location <  dst + length:
                        # transform by calculating the offset
                        new_seed.append(location - rng.source + rng.destination)
                        # can be in only one range so
                        break
                else:
                    # no transformation so keep the seed
                    new_seed.append(location)
            _(new_seed)
            locations = new_seed
        return min(locations)

    def find_nearest_ranged_seed_location(self):
        """
        This method will find the nearest seed location for the given seed ranges.
        - first lets split the seeds into ranges and give them a clear start and end
          transform the seeds into a list of tuples (start, end) instead of a start and a length.
          so now seeds = [(start, end), (start, end), ...] this is better than creating all the
          individual seeds as the ranges are way too big.
        - Trouble is that we can not apply the entire range of the seed to the maps as the ranges as it not
          guaranteed that it will be in the range. The mappings may not
          e.g.
             range_mappings: -------------               ----------------------
             seed_range:              -------------------------
                                      ^^^^~~~~~~~~~~~~~~~^^^^^^
             overlaps (^) and not overlaps (~)
          so we need to split the seed range into smaller segments to be able to apply the mappings.
          - the first set of ^^^ will be mapped to the left mapping
          - the second set of ^^^ will be mapped to the right mapping
          - the ~~~ will not be mapped
        - we will do the segmentation by using the seeds as a kind of queue (not a real one) and process seeds
          as long as we have seeds to process.
        - we first have to find the overlapping ranges for the seed range and the mapping range.
          e.g.
          seed_range:      min_s-------------------------max_s
          mapping_range:                min_r----------------------max_r
          overlap:                           ------------
          so the start of an overlap is the max of the min_s and min_r
          and the end of an overlap is the min of the max_s and max_r (max_r is the source + length)
        (this took me ages to figure out)
        - There is only an overlap if the start of the overlap is smaller than the end of the overlap.
          if not then there is no overlap, and we can skip the mapping.
        - if there is a seed before the overlap then we add it to the queue for further processing
        - if there is a seed after the overlap then we add it to the queue for further processing
        - and if there was no overlap then we add the seed to the new seeds list as is
        """

        seeds: list[Seed] = [Seed(start, start + length - 1) for start, length in chunkify(self.seeds, 2)]
        _(seeds)

        for block in self.maps:
            _(block)
            ranges: list[Range] = self.parse_ranges(block)
            new_seeds: list[Seed] = []
            while seeds:
                seed = seeds.pop()
                _(seed)
                for r in ranges:
                    overlap_start = max(seed.start, r.source)
                    overlap_end = min(seed.end, r.source + r.length)
                    if overlap_start < overlap_end:  # there is an overlap
                        # transform by calculating the offset (as in the find_nearest_seed_location method)
                        new_seeds.append(
                            Seed(
                                overlap_start - r.source + r.destination,
                                overlap_end - r.source + r.destination
                            )
                        )
                        if overlap_end < seed.end:  # there is a seed after the overlap
                            # add the new seed range to the queue for further processing
                            seeds.append(Seed(overlap_end, seed.end))
                        if seed.start < overlap_start:  # there is a seed before the overlap
                            # add the new seed range to the queue for further processing
                            seeds.append(Seed(seed.start, overlap_start))
                        break
                else:  # no overlap
                    new_seeds.append(seed)
            seeds = new_seeds

        return min(seeds)[0]


def part_1(source):
    return Almanac(source).find_nearest_seed_location()


def part_2(source):
    return Almanac(source).find_nearest_ranged_seed_location()


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_data("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""")
        self.test_source2 = read_rows("""""")

    def test_example_data_part_1(self):
        self.assertEqual(35, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(26273516, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(46, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(34039469, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
