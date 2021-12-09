#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 01/12/2021 10:39$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
##############################################################################
# Part 1
##############################################################################
--- Day 24: Lobby Layout ---
Your raft makes it to the tropical island; it turns out that the small crab 
was an excellent navigator. You make your way to the resort.

As you enter the lobby, you discover a small problem: the floor is being 
renovated. You can't even reach the check-in desk until they've finished 
installing the new tile floor.

The tiles are all hexagonal; they need to be arranged in a hex grid with a 
very specific color pattern. Not in the mood to wait, you offer to help figure 
out the pattern.

The tiles are all white on one side and black on the other. They start with the 
white side facing up. The lobby is large enough to fit whatever pattern might 
need to appear there.

A member of the renovation crew gives you a list of the tiles that need to be 
flipped over (your puzzle input). Each line in the list identifies a single tile 
that needs to be flipped by giving a series of steps starting from a reference 
tile in the very center of the room. (Every line starts from the same reference tile.)

Because the tiles are hexagonal, every tile has six neighbors: east, southeast, 
southwest, west, northwest, and northeast. These directions are given in your 
list, respectively, as e, se, sw, w, nw, and ne. A tile is identified by a 
series of these directions with no delimiters; for example, esenee identifies 
the tile you land on if you start at the reference tile and then move one tile 
east, one tile southeast, one tile northeast, and one tile east.

Each time a tile is identified, it flips from white to black or from black 
to white. Tiles might be flipped more than once. For example, a line like 
esew flips a tile immediately adjacent to the reference tile, and a line like 
nwwswee flips the reference tile itself.

Here is a larger example:

sesenwnenenewseeswwswswwnenewsewsw
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
wseweeenwnesenwwwswnew
In the above example, 10 tiles are flipped once (to black), and 5 more are flipped twice (to black, then back to white). After all of these instructions have been followed, a total of 10 tiles are black.

Go through the renovation crew's list and determine which tiles they need to flip. After all of the instructions have been followed, how many tiles are left with the black side up?
##############################################################################
# Part 2
##############################################################################

"""

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
    data = read_rows("day_24.txt")
    # data = example
    lines = data.split("\n")
    black_tiles = set()
    for line in lines:
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
        # Get all neighbors of all black tiles inlcuding themselfs to start processing
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
    print(len(black_tiles))


if __name__ == '__main__':
    main()
