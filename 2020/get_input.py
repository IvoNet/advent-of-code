#!/usr/bin/env python3
import sys

import requests


def read_session():
    with open("../.session", "r") as session:
        return session.read().strip()


def main(day):
    resp = requests.get(f"https://adventofcode.com/2020/day/{day}/input", cookies={"session": read_session()})
    filename = f"day_{day}.txt"
    print("Writing:", filename)
    with open(filename, "w") as fo:
        fo.write(resp.text)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        import datetime

        d = datetime.datetime.now()
        main(d.strftime("%d"))
    else:
        main(sys.argv[1])
