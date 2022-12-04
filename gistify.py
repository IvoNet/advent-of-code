#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 04/12/2022 11:38$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import json
import sys
from pathlib import Path

import requests

# Rename this one to
AOC_GIST = "AoC2022"

CREATE_AOC_GIST_PAYLOAD = '{"description":"%s","public":"true","files":{"README.md":{"content":"All can also be found here: https://github.com/IvoNet/advent-of-code"}}}' % AOC_GIST

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


def create_aoc_gist() -> str:
    resp = requests.post("https://api.github.com/gists",
                         headers=headers("application/vnd.github+json"),
                         data=CREATE_AOC_GIST_PAYLOAD)
    if resp.status_code == 201:
        print("Created gist")
        return json.loads(resp.text)['id']
    raise ValueError(f"Error creating gist: {resp.text}")


def get_aoc_id():
    for gist in get_gists():
        if gist['description'] == AOC_GIST:
            return gist['id']
    return create_aoc_gist()


def update_gist(gist_id, year, day):
    filename = f"./{year}/day_{day.zfill(2)}/day_{day.zfill(2)}"
    with open(f"{filename}.py", "r") as py:
        py_content = py.read()
        if not py_content:
            raise ValueError(f"File {filename}.py is empty or dose not exist.")
        outpy = f"{day}_1.py"
        payload = json.dumps({'files': {outpy: {"content": py_content},
                                        f"{day}_2.py": {"content": f"#see: {outpy}"}}})
        resp = requests.patch(f"https://api.github.com/gists/{gist_id}",
                              headers=headers("application/vnd.github+json"),
                              data=payload)
        if resp.status_code == 200:
            print("Updated gist:\nhttps://gist.github.com/IvoNet/{}".format(gist_id))
            return resp.text
        raise ValueError(f"Error updating gist: {resp.text}")


def main(year: str, day: str):
    aoc_id = get_aoc_id()
    update_gist(aoc_id, year, day)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        import datetime

        d = datetime.datetime.now()
        main(d.strftime("%Y"), d.strftime("%d"))
    else:
        main(sys.argv[1], sys.argv[2])  # python gistify.py year day
