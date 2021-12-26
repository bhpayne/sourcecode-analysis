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

def how_many_modules_have_help(assessment_dict: dict) -> dict:
    """
    metric for code documentation
    """
    count_of_candidates = 0
    count_of_help = 0
    what_is_missing_help = []
    for filename, filedict in assessment_dict.items():
        if filedict['module']['has --help']:
            count_of_help+=1
        else:
            what_is_missing_help.append(filename)
        count_of_candidates+=1

    return {'count of scripts that could have --help:':count_of_candidates,
            'count of scripts with --help:':count_of_help,
            'list of what is missing --help:':what_is_missing_help}

def how_many_functions_and_classes_and_modules_have_docstring(assessment_dict:dict) -> dict:
    """
    metric for code documentation
    """
    count_of_candidates = 0
    count_of_docstrings = 0
    what_is_missing_docstrings = []
    for filename, filedict in assessment_dict.items():
        for classname, classdict in filedict['class'].items():
            for functionname, functiondict in classdict['functions'].items():
                if functiondict['has docstring']:
                    count_of_docstrings+=1
                else:
                    what_is_missing_docstrings.append(filename+" class "+ classname+" function "+functionname)
                count_of_candidates+=1
            if classdict['has docstring']:
                count_of_docstrings+=1
            else:
                what_is_missing_docstrings.append(filename+" class "+ classname)
            count_of_candidates+=1
        for functionname, functiondict in classdict['functions'].items():
            if functiondict['has docstring']:
                count_of_docstrings+=1
            else:
                what_is_missing_docstrings.append(filename+" function "+functionname)
            count_of_candidates+=1
        if filedict['module']['has docstring']:
            count_of_docstrings+=1
        else:
            what_is_missing_docstrings.append(filename)
        count_of_candidates+=1

    return {'count of things that could have a docstring:':count_of_candidates,
            'count of things with a docstring:':count_of_docstrings,
            'list of what is missing docstrings:':what_is_missing_docstrings}

def all_import(assessment_dict:dict):
    """
    this is useful for comparison with the "pip install" in Docker/Singularity
    since some packages may be imported in Docker/Singularity that are not longer relevant

    Just because a package is imported does not mean it gets used, so this check is not the be-all-end-all.
    """
    all_imports_list = []
    for filename, filedict in assessment_dict.items():
        for imported_module in filedict['module']['imports']:
            all_imports_list.append(imported_module)
    return all_imports_list

def print_results(res_dict: dict) -> None:
    """
    >>> print_results(res_dict)
    """
    for str_to_print, result in res_dict.items():
        if isinstance(result, list):
            print(str_to_print)
            for item in result:
                print("   ",item)
        else:
            print(str_to_print, result)
    return

if __name__ == "__main__":

    parser = init_argparse()
    args = parser.parse_args()

    if len(sys.argv)<2:
        sys.exit("ERROR: You need to pass one or more JSON filenames as argument")


    for this_JSON_file in args.JSON_file:

        with open('result.json', 'r') as fp:
            assessment_dict = json.load(fp)

        all_imports = list(set(all_import(assessment_dict)))
        print("all imported modules:",all_imports)

        res_dict = how_many_functions_and_classes_and_modules_have_docstring(assessment_dict)
        print_results(res_dict)

        res_dict = how_many_modules_have_help(assessment_dict)
        print_results(res_dict)

        # https://stackoverflow.com/a/12944035/1164295
        #print(json.dumps(assessment_dict, indent=4, sort_keys=True))
