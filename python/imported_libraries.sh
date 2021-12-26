#!/usr/bin/env bash

# this shell script is intended as a sanity check for 
# static_offline_python_analysis.py
# which is better 

find . -type f -name "*.py" |\       # find files then end in ".py" recursively
    xargs grep "^import\|^from" |\   # for each .py file, look for lines that start with "import" or "from"
    cut -d' ' -f2 |\                 # using " " as a delimiter, show only the second column
    sort | uniq  
