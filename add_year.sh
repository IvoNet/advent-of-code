#!/usr/bin/env bash

if [ -z "$VIRTUAL_ENV" ]; then
    echo "You are not within the virtual python environment"
    echo "Please activate it first."
    exit 1
fi

if [ -z "$1" ]; then
  echo "Please provide a year as parameter"
  exit 1
fi

if [ -d "$1" ]; then
  echo "The year appears to already exist"
  exit 1
fi

mkdir -p "$1"
cp -v get_input.py "./$1/"
sed -i "" "s/YEAR_HERE/$1/g" "$1/get_input.py"

cd "$1" || exit 1

for i in {1..25}; do
  python get_input.py "$i"
done

cd - || exit 1

for i in {01..25}; do
  cp -v day_.py "$1/day_$i/day_$i.py"
done
