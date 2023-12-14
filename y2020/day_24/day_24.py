#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

from collections import defaultdict

from ivonet.files import read_rows

WHITE = 0
BLACK = 1

NAMED = {
    #    up,right
    "e": (1, 0),  # 0
    "se": (0.5, -1),  # 1
    "sw": (-0.5, -1),  # 2
    "w": (-1, 0),  # 3
    "nw": (-0.5, 1),  # 4
    "ne": (0.5, 1)  # 5
}

DIRECTIONS = {
    #    up,right
    "0": (1, 0),  # "e"
    "1": (0.5, -1),  # "se"
    "2": (-0.5, -1),  # "sw"
    "3": (-1, 0),  # "w"
    "4": (-0.5, 1),  # "nw"
    "5": (0.5, 1)  # "ne"
}

example = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""


def get_neigbors(x, y, with_self=False):
    if with_self:
        yield x, y
    yield x + NAMED["e"][0], y + NAMED["e"][1]
    yield x + NAMED["se"][0], y + NAMED["se"][1]
    yield x + NAMED["sw"][0], y + NAMED["sw"][1]
    yield x + NAMED["w"][0], y + NAMED["w"][1]
    yield x + NAMED["nw"][0], y + NAMED["nw"][1]
    yield x + NAMED["ne"][0], y + NAMED["ne"][1]


def main():
    tiles = defaultdict()
    data = read_rows("day_24.input")
    # data = example
    # lines = data.split("\n")
    black_tiles = set()
    for line in data:
        # print(line)
        line = line.replace("se", "1") \
            .replace("ne", "5") \
            .replace("e", "0") \
            .replace("sw", "2") \
            .replace("nw", "4") \
            .replace("w", "3")
        x, y = (0, 0)
        for direction in line:
            dx, dy = DIRECTIONS[direction]
            x += dx
            y += dy
        tiles[(x, y)] = (tiles.get((x, y), WHITE) + 1) % 2
        if (x, y) in black_tiles:
            black_tiles.remove((x, y))
        else:
            black_tiles.add((x, y))

    print("Answer part 1:", len(black_tiles))

    for _ in range(100):
        new_black_tiles = set()
        # Get all neighbors of all black tiles including themselves to start processing
        # now we have the whole grid
        for x, y in set.union(*[set(get_neigbors(xx, yy, True)) for xx, yy in black_tiles]):
            count_black_tiles = 0
            for xx, yy in get_neigbors(x, y):
                if (xx, yy) in black_tiles:
                    count_black_tiles += 1
                    if count_black_tiles > 2:
                        break

            if (x, y) in black_tiles:  # black tile
                if count_black_tiles in [1, 2]:  # Stay black if on 1 or bigger than 2
                    new_black_tiles.add((x, y))
            elif count_black_tiles == 2:  # white tile with two black tiles touching
                new_black_tiles.add((x, y))

        black_tiles = new_black_tiles
    print("Answer part_2:", len(black_tiles))


if __name__ == '__main__':
    main()
