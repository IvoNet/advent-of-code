#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 04/12/2022 11:38$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Make a gist of the day's code.
"""

import json
from pathlib import Path

import requests

CREATE_AOC_GIST_PAYLOAD = '{"description":"%s","public":"true","files":{"README.md":{"content":"All can also be found here: https://github.com/IvoNet/advent-of-code"}}}'

PYTHON_FILE_PAYLOAD = """{'filename': '%s.py',
                       'language': 'Python',
                       'type': 'application/x-python'},"""


def api_token():
    if not Path(".gist").is_file():
        raise ValueError(
            "Please create a '.gist' file with the api token in it (see: https://github.com/settings/tokens)")
    with open(".gist", "r") as api_token:
        return api_token.read().strip()


def headers(accept="application/vnd.github+json", content_type="application/json"):
    return {'Authorization': f'token {api_token()}',
            'Accept': accept,
            'Content-Type': content_type}


def get_gists():
    resp = requests.get("https://api.github.com/gists",
                        headers=headers("application/vnd.github.v3+json"))
    return json.loads(resp.text)


def create_aoc_gist(title: str) -> str:
    resp = requests.post("https://api.github.com/gists",
                         headers=headers("application/vnd.github+json"),
                         data=CREATE_AOC_GIST_PAYLOAD % title)
    if resp.status_code == 201:
        print("Created gist")
        return json.loads(resp.text)['id']
    raise ValueError(f"Error creating gist: {resp.text}")


def get_aoc_id(title: str) -> str:
    for gist in get_gists():
        if gist['description'] == title:
            return gist['id']
    return create_aoc_gist(title)


def update_gist(gist_id, year, day, verbose=False):
    # noinspection DuplicatedCode
    filename = f"./{year}/day_{day.zfill(2)}/day_{day.zfill(2)}"
    with open(f"{filename}.py", "r") as py:
        py_content = py.read()
        if not py_content:
            raise ValueError(f"File {filename}.py is empty or dose not exist.")
        output_py_filename = f"{day}_1.py"
        payload = json.dumps({'files': {output_py_filename: {"content": py_content},
                                        f"{day}_2.py": {"content": f"\n\n__doc__= '''See {output_py_filename}'''"}}})
        resp = requests.patch(f"https://api.github.com/gists/{gist_id}",
                              headers=headers("application/vnd.github+json"),
                              data=payload)
        if verbose:
            print(resp.status_code)
        if resp.status_code == 200:
            print("Updated gist:\nhttps://gist.github.com/IvoNet/{}".format(gist_id))
            if verbose:
                print(resp.text)
            return resp.text
        raise ValueError(f"Error updating gist: {resp.text}")


def main(title: str, year: str, day: str, verbose=False):
    aoc_id = get_aoc_id(title)
    update_gist(aoc_id, year, day, verbose)


if __name__ == '__main__':
    print("Gistify (c) 2022 by Ivo Woltring")
    import argparse

    parser = argparse.ArgumentParser("python3 gistify.py")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-t', '--title', required=True, default="AoC2022", help="Title of the gist")
    parser.add_argument('-y', '--year', required=True, default="2022", help="The year you want to post")
    parser.add_argument('-d', '--day', required=True, help="The day you want to post")

    args = parser.parse_args()
    print("This may take a while...")

    main(args.title, args.year, args.day, verbose=args.verbose)
    print("Done.")
