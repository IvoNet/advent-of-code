#!/usr/bin/env python3
import os
import re
import sys
import textwrap
from pathlib import Path
from shutil import copyfile

import requests
from bs4 import BeautifulSoup


def read_session():
    if not Path(".session").is_file():
        raise ValueError("Please create a '.session' file with the cookie in it (see readme)")
    with open(".session", "r") as session:
        return session.read().strip()


def md(name):
    try:
        os.mkdir(name)
    except IOError:
        pass


def wrap(string, max_width=80):
    return '\n'.join(textwrap.wrap(string, max_width))


def touch(name):
    Path(name).touch()


def create_folders(year, day):
    md(year)
    md(f"./{year}/day_{day.zfill(2)}")
    touch(f"./{year}/day_{day.zfill(2)}/__init__.py")


def get_web_page(year, day):
    # Get the puzzle input
    resp = requests.get(f"https://adventofcode.com/{year}/day/{day}", cookies={"session": read_session()})
    soup = BeautifulSoup(resp.text, "html.parser")
    text = ""
    for hit in soup.findAll(attrs={'class': 'day-desc'}):
        text += "\n"
        text += hit.text
    return text


def get_puzzle_description(year, day, filename):
    text = get_web_page(year, day)

    lines = text.splitlines()
    description = ""
    for line in lines:
        wip = re.split("(--- .+ ---)", line.strip())
        if len(wip) > 1:  # found title
            for x in wip:
                if x.startswith("---"):
                    description += f"\n{x}\n\n"
                    continue
                description += wrap(x)
                description += "\n"
            continue
        if len(line) > 80:
            line = wrap(line).replace(":", ":\n")
            description += f"{line}\n\n"
            continue
        line = line.replace(':', ':\n\n')
        description += f"{line}\n"
    description = description.replace("  ", " ").replace("  ", " ")
    print("Writing description      :", filename)
    with open(filename, 'w') as fo:
        fo.write(description)


def get_puzzle_input(year, day, filename):
    resp = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies={"session": read_session()})
    print("Writing puzzle input     :", filename)
    with open(filename, "w") as fo:
        fo.write(resp.text)


def get_solution_template(year, day, filename):
    if os.path.isfile(filename):
        print("Python solution file seems to already exists... leaving it.")
        return
    print("Writing solution template:", filename)
    copyfile("./template.py", filename)


def main(year, day):
    filename = f"./{year}/day_{day.zfill(2)}/day_{day.zfill(2)}"
    create_folders(year, day)
    get_puzzle_input(year, day, filename + ".input")
    get_puzzle_description(year, day, filename + ".txt")
    get_solution_template(year, day, filename + ".py")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        import datetime

        d = datetime.datetime.now()
        main(d.strftime("%Y"), d.strftime("%d"))
    else:
        main(sys.argv[1], sys.argv[2])  # python aoc_input.py year day
