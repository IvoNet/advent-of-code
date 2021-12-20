#!/usr/bin/env python3
import os
import sys

import requests

YEAR = "YEAR_HERE"


def read_session():
    with open("../.session", "r") as session:
        return session.read().strip()


def md(name):
    try:
        os.mkdir(name)
    except IOError:
        pass


def touch(name):
    from pathlib import Path
    Path(name).touch()


def main(day):
    # Create the folder and make it a python package
    md(f"day_{day.zfill(2)}")
    touch(f"day_{day.zfill(2)}/__init__.py")

    # Get the puzzle input
    resp = requests.get(f"https://adventofcode.com/{YEAR}/day/{day}/input", cookies={"session": read_session()})
    filename = f"day_{day.zfill(2)}/day_{day.zfill(2)}.txt"
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
