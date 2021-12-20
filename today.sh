#!/usr/bin/env bash

if [ -z "$VIRTUAL_ENV" ]; then
    echo "You are not within the virtual python environment"
    echo "Please activate it first."
    exit 1
fi

python aoc_description.py
python aoc_input.py
