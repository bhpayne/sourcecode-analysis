#!/usr/bin/env bash


find /path/to/project/files/ -type f -name "*.c*" | xargs grep "^\s*class.*:"
