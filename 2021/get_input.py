#!/usr/bin/env python3
import sys

import requests


def main(day):
    resp = requests.get(f"https://adventofcode.com/2021/day/{day}/input", cookies={
        "session": "53616c7465645f5f2c3d9ac0f64aa95a29c20967fbbbe38bed2632502ffc69b90880964c11f9bc793f4df8a2b138c0e5;"})
    filename = f"day-{day}.txt"
    print("Writing:", filename)
    with open(filename, "w") as fo:
        fo.write(resp.text)


if __name__ == '__main__':
    main(sys.argv[1])
