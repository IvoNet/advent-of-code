#!/usr/bin/env bash
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Please start the virtual env first..."
    exit 1
fi
clear
python -m unittest discover -p tests.py -v
