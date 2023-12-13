# Advent of code

My attempt at solving the [Advent of code](https://adventofcode.com) puzzles.
2021 was the first year I actually went for it, and I am hooked.

I think I will try to solve these problems in multiple languages.
Starting with Python.

# Usage

- go to the project root
- create a virtualenv (one time only)

```shell
python3 -m venv venv
```

- activate it (every new session)

```shell
source "./venv/bin/activate"
```

- add the dependencies (one time only)

```shell
python3 -m pip install -r requirements.txt
```

# ivonet package

Contains many of the convenience methods / classes and functions I created while
solving these puzzles and use in the puzzles.

Just run the `enable_ivonet_package.sh` script from the root if this project in
a terminal.

it will:

- create e file called `ivonet.pth`in the virtual env `site-packages` folder.
- in that pth file it will place the location if this project root and that is
  it.
- now the ivonet package is accessible from all the years when running in the
  virtual environment.

# `.session` file

in order to download the input data from the adventofcode.com site you need to login in a browser
and get the session information from that browser.

- go into developer tools
- go to the network tab
- go to the `adventofcode.com` site
- Look for a cookie called `session`
- copy the value of that cookie (only the value)
- create a file called `.session` in the root of this project
- paste the value of the cookie in that file
- now the `aoc_input.py` script will be able to download the input data for you.

```shell
# python ./aoc_input.py <YEAR> <DAY>
python ./aoc_input.py 2023 14
```

# What is completed...

## 2023

- 26 stars

## 2022

- 38 stars

## 2021

- 50 stars!

## 2020

- 27 stars

## 2019

- 8 stars

## 2018

- 43 stars

## 2017

- 50 stars!

# 2016

- 50 stars!

## 2015

- 50 stars!

----

# Jupiter theme

## install

```text
pip install jupyterthemes
```

## Activate theme

```text
jt -f roboto -fs 12 -t monokai -T -N -kl -vim
```
