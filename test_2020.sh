#!/usr/bin/env bash
cd 2020
#ptw --runner "pytest --testmon" *.py

while true;
do
  python -m unittest discover -s . -p "*.py"
  echo -n "Press [ENTER] ro repeat test."
  read
done
