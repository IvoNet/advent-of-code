#!/usr/bin/env bash
cd 2021
#ptw --runner "pytest --testmon" *.py

while true;
do
  python -m unittest discover -s . -p "day_$1.py"
  echo -n "Press [ENTER] ro repeat test."
  read
done
