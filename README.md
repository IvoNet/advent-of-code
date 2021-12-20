# Advent of code

* [Advent of code](https://adventofcode.com)

# Usage

- go to the project root
- create a virtualenv (one time only)

```shell
python3.9 -m venv venv
```

- activate it (every new session)

```shell
source "./venv/bin/activate"
```

# ivonet package

To use the ivonet package please create e file called `ivonet.pth`
in the virtual env `site-packages` folder e.g.
in `PROJECT_DIR_HERE/venv/lib/python3.9/site-packages/ivonet.pth`
in that file put one string with the exact (fully qualified) path to the ivonet
package in the project. e.g. `/Users/YOUR_USERNAME/dev/advent-of-code/`
do not include the package name itself just the path to the folder where it
lives

now the ivonet package is accessible from all the years when running in the
virtual environment.

## Create a new year

```shell
mkdir YEAR_HERE
cd YEAR_HERE
mkdir day_{01..25}
find . -type d -name "day*" -exec touch "{}/__init__.py" \;
```

## 2021

* [Advent of code 2021](https://adventofcode.com/2021)
* [Ordina leader board](https://ordinaadventofcode.azurewebsites.net/Leaderboard/Ordina)

## Good links / Articles / Tools

* [Advent of Code: Solving Your Puzzles With Python](https://realpython.com/python-advent-of-code/)
* [pip install advent-of-code-data](https://pypi.org/project/advent-of-code-data/)
