#!/usr/bin/env bash

# this shell script is intended as a sanity check for 
# static_offline_python_analysis.py
# which is better 

find . -type f -name "*.py" |\       # find files that end in ".py" recursively
    xargs grep --files-without-match "if\s*__name__\s*==\s*"   # for each .py file, look for files that do not contain "if __name__ =="

