#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = False

X = 0
Y = 1
Z = 2

first_debug_statement = True


# noinspection DuplicatedCode
def _(*args, end="\n"):
    global first_debug_statement
    if DEBUG:
        if first_debug_statement:
            first_debug_statement = not first_debug_statement
            print()
        # print(" ".join(str(x) for x in args), end=end)
        with open("debug.txt", "a") as fo:
            fo.write(" ".join(str(x) for x in args))
            fo.write(end)


def part_1(source):
    grid = defaultdict(bool)
    for cmd in source:
        x1, x2, y1, y2, z1, z2 = ints(cmd)
        # skip if totally out of range
        if x2 < -50 or y2 < -50 or z2 < -50:
            continue
        if x1 > 50 or y1 > 50 or z1 > 50:
            continue
        #  if partly out of range set the range
        if x1 < -50:
            x1 = -50
        if x2 > 50:
            x2 = 50
        if y1 < -50:
            y1 = -50
        if y2 > 50:
            y2 = 50
        if z1 < -50:
            z1 = -50
        if z2 > 50:
            z2 = 50
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    # if -50 >= x >= 50 or -50 >= y >= 50 or -50 >= z >= 50:
                    #     continue
                    grid[(x, y, z)] = cmd.startswith("on")

    return sum(1 for v in grid.values() if v is True)


class Coord(NamedTuple):
    x: int
    y: int
    z: int


class Cuboid(NamedTuple):
    lower: Coord
    upper: Coord


class Instruction(NamedTuple):
    toggle_on: bool
    cuboid: Cuboid


def volume(cuboid: Cuboid):
    """Calc the volume of a cuboid"""
    return (cuboid.upper.x - cuboid.lower.x + 1) * \
           (cuboid.upper.y - cuboid.lower.y + 1) * \
           (cuboid.upper.z - cuboid.lower.z + 1)


def parse(source) -> list[Instruction]:
    instructions: list[Instruction] = []
    for cmd in source:
        x1, x2, y1, y2, z1, z2 = ints(cmd)
        instructions.append(Instruction(cmd.startswith("on"), Cuboid(Coord(x1, y1, z1), Coord(x2, y2, z2))))
    return instructions


def overlap(left: Cuboid, right: Cuboid) -> Cuboid:
    """Calc the overlap of two cuboids
    what can happen:
    - 1: No overlap (see function no_overlap)
    - 2: left full overlap of right (lllrrrlll)
    - 3 partial overlap
    """
    lower = [None, None, None]
    upper = [None, None, None]
    _(f"Start overlap check with left({left}) vs right({right})")
    for i in range(3):  # for all sides
        if left.lower[i] > right.upper[i] or left.upper[i] < right.lower[i]:
            return None
        elif left.upper[i] <= right.upper[i] and left.lower[i] >= right.lower[i]:
            # left contain right
            _("left >= right")
            upper[i] = left.upper[i]
            lower[i] = left.lower[i]
        elif right.upper[i] <= left.upper[i] and right.lower[i] >= left.lower[i]:
            # right contain left
            _("right >= left")
            upper[i] = right.upper[i]
            lower[i] = right.lower[i]
        elif right.lower[i] <= left.lower[i] and right.upper[i] <= left.upper[i]:
            _("Partial right")
            upper[i] = right.upper[i]
            lower[i] = left.lower[i]
        elif left.lower[i] <= right.lower[i] and left.upper[i] <= right.upper[i]:
            _("Partial left")
            upper[i] = left.upper[i]
            lower[i] = right.lower[i]
        else:
            _("Something went wrong?!", left, right)
            return None
    _(lower, upper)
    return Cuboid(Coord(*lower), Coord(*upper))


def subtract(left: Cuboid, overlap: Cuboid) -> list[Cuboid]:
    """This subract function takes subracts right from left
    right is an exact subset of what needs to be taken out (overlap)
    """
    ret: list[Cuboid] = []
    if left == overlap:
        # full delete so return empty
        # that will cause it to not add new cuboids
        _("Exact same so just delete")
        return ret

    if left.lower.z != overlap.lower.z:
        _("left.lower.z != overlap.lower.z")
        lower = left.lower
        upper = Coord(left.upper.x, left.upper.y, overlap.lower.z - 1)
        if upper.z:
            ret.append(Cuboid(lower, upper))

    if left.lower.y != overlap.lower.y:
        _(left.lower.y != overlap.lower.y)
        lower = Coord(left.lower.x, left.lower.y, overlap.lower.z)
        upper = Coord(left.upper.x, overlap.lower.y - 1, overlap.upper.z)
        ret.append(Cuboid(lower, upper))

    if left.lower.x != overlap.lower.x:
        lower = Coord(left.lower.x, overlap.lower.y, overlap.lower.z)
        upper = Coord(overlap.lower.x - 1, overlap.upper.y, overlap.upper.z)
        ret.append(Cuboid(lower, upper))

    if left.upper.x != overlap.upper.x:
        lower = Coord(overlap.upper.x + 1, overlap.lower.y, overlap.lower.z)
        upper = Coord(left.upper.x, overlap.upper.y, overlap.upper.z)
        ret.append(Cuboid(lower, upper))

    if left.upper.y != overlap.upper.y:
        lower = Coord(left.lower.x, overlap.upper.y + 1, overlap.lower.z)
        upper = Coord(left.upper.x, left.upper.y, overlap.upper.z)
        ret.append(Cuboid(lower, upper))

    if left.upper.z != overlap.upper.z:
        lower = Coord(left.lower.x, left.lower.y, overlap.upper.z + 1)
        upper = left.upper
        ret.append(Cuboid(lower, upper))
    _("subract:", ret)
    return ret


def how_many_on(instructions: list[Instruction]) -> int:
    cuboids_on = {}
    for cmd in instructions:
        to_add: list[Cuboid] = []
        left = cmd.cuboid
        if cmd.toggle_on:
            to_add.append(left)
        for right in list(cuboids_on):
            overlap_cuboid = overlap(left, right)
            if overlap_cuboid is None:
                continue
            _("Overlapping cuboid:", overlap_cuboid)
            del (cuboids_on[right])
            to_add.extend(subtract(right, overlap_cuboid))
        for c in to_add:
            cuboids_on[c] = True
    total = 0
    _(cuboids_on)
    _(len(cuboids_on))
    for cuboid in cuboids_on:
        total += volume(cuboid)
    return total


def part_2(source):
    """
    https://www.mathsisfun.com/geometry/cuboids-rectangular-prisms.html#Volume
    https://www.mathworks.com/matlabcentral/answers/522003-how-do-i-find-the-overlapping-volume-of-multiple-3d-rectangles
    """
    instructions = parse(source)
    _(instructions)
    return how_many_on(instructions)


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"day_{day.zfill(2)}.input")
        self.test_source = read_rows("""on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10""")
        self.test_sources_2 = read_rows("""on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682""")
        self.test_sources_3 = read_rows("""on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507""")

    def test_overlap_1(self):
        left = Cuboid(Coord(1, 1, 1), Coord(3, 3, 3))
        self.assertEqual(left, overlap(left, left))

    def test_overlap_2(self):
        left = Cuboid(Coord(1, 1, 1), Coord(3, 3, 3))
        right = Cuboid(Coord(2, 2, 2), Coord(4, 4, 4))
        self.assertEqual(Cuboid(Coord(2, 2, 2), Coord(3, 3, 3)), overlap(left, right))

    def test_overlap_3(self):
        """Right is bigger than left so overlap is the smaller one rest can be ignored"""
        left = Cuboid(Coord(1, 1, 1), Coord(3, 3, 3))
        right = Cuboid(Coord(0, 0, 0), Coord(4, 4, 4))
        self.assertEqual(left, overlap(left, right))

    def test_overlap_4(self):
        """Right is smaller"""
        left = Cuboid(Coord(0, 0, 0), Coord(4, 4, 4))
        right = Cuboid(Coord(1, 1, 1), Coord(3, 3, 3))
        self.assertEqual(right, overlap(left, right))

    def test_subtract_1(self):
        left = Cuboid(Coord(0, 0, 0), Coord(2, 2, 2))
        right = Cuboid(Coord(1, 1, 1), Coord(3, 3, 3))
        self.assertEqual([Cuboid(lower=Coord(x=0, y=0, z=1), upper=Coord(x=2, y=0, z=2)),
                          Cuboid(lower=Coord(x=0, y=1, z=1), upper=Coord(x=0, y=2, z=2))],
                         subtract(left, overlap(left, right)))

    def test_subtract_2(self):
        """Right is bigger than left so overlap is the smaller one rest can be ignored"""
        left = Cuboid(Coord(1, 1, 1), Coord(3, 3, 3))
        right = Cuboid(Coord(0, 0, 0), Coord(4, 4, 4))
        self.assertEqual([], subtract(left, overlap(left, right)))

    def test_subtact_3(self):
        """Right is smaller"""
        left = Cuboid(Coord(0, 0, 0), Coord(4, 4, 4))
        right = Cuboid(Coord(1, 1, 1), Coord(3, 3, 3))
        self.assertEqual([Cuboid(lower=Coord(x=0, y=0, z=1), upper=Coord(x=4, y=0, z=3)),
                          Cuboid(lower=Coord(x=0, y=1, z=1), upper=Coord(x=0, y=3, z=3)),
                          Cuboid(lower=Coord(x=4, y=1, z=1), upper=Coord(x=4, y=3, z=3)),
                          Cuboid(lower=Coord(x=0, y=4, z=1), upper=Coord(x=4, y=4, z=3)),
                          Cuboid(lower=Coord(x=0, y=0, z=4), upper=Coord(x=4, y=4, z=4))],
                         subtract(left, overlap(left, right)))

    def test_example_data_part_1(self):
        self.assertEqual(39, part_1(self.test_source))

    def test_example_data_part_1_2(self):
        self.assertEqual(590784, part_1(self.test_sources_2))

    def test_example_data_part_1_3(self):
        self.assertEqual(474140, part_1(self.test_sources_3))

    def test_part_1(self):
        self.assertEqual(583641, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(2758514936282235, part_2(self.test_sources_3))

    def test_part_2(self):
        self.assertEqual(1182153534186233, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
