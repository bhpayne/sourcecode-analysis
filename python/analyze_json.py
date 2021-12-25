#!/usr/bin/env python3

"""

"""

import sys
import glob
import argparse
import os
import json

def init_argparse() -> argparse.ArgumentParser:
    """
    from https://realpython.com/python-command-line-arguments/#argparse
    """
    parser = argparse.ArgumentParser(
        usage="%(prog)s [JSON FILE]",
        description="statistics of JSON FILE"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('JSON_file', nargs='*')
    return parser


def how_many_arguments_are_typed(assessment_dict:dict):
    """
    metric for code documentation
    """
    return

def how_many_functions_and_classes_and_modules_have_docstring(assessment_dict:dict):
    """
    metric for code documentation
    """
    return

def all_import(assessment_dict:dict):
    """
    this is useful for comparison with the "pip install" in Docker/Singularity
    since some packages may be imported in Docker/Singularity that are not longer relevant

    Just because a package is imported does not mean it gets used, so this check is not the be-all-end-all.
    """
    return

if __name__ == "__main__":

    parser = init_argparse()
    args = parser.parse_args()

    if len(sys.argv)<2:
        sys.exit("ERROR: You need to pass one or more JSON filenames as argument")


    for this_JSON_file in args.JSON_file:

        with open('result.json', 'r') as fp:
            assessment_dict = json.load(fp)

        # https://stackoverflow.com/a/12944035/1164295
        #print(json.dumps(assessment_dict, indent=4, sort_keys=True))
