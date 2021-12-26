#!/usr/bin/env bash

# this shell script is intended as a sanity check for 
# static_offline_python_analysis.py
# which is better 

find . -type f -name "*.py" |\       # find files then end in ".py" recursively
    xargs grep "^class\|^def"    # for each .py file, look for lines that start with "class" or "def"
