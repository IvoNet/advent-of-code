#!/usr/bin/env bash

if [ -z "$VIRTUAL_ENV" ]; then
  echo "You have either not created a virtual environment for this project"
  echo "or have not activated it yet."
  echo "How to:"
  echo "- create a virtual environment  : python3 -m venv venv"
  echo "- activate a virtual environment: source ./venv/bin/activate"
  echo "Please do so first..."
  exit 1
fi

sp=$(find "$VIRTUAL_ENV" -type d -name "site-packages")
pwd > "$sp/ivonet.pth"

echo "The ivonet package should now work within the virtual environment."
echo "Have fun."
