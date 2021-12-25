#!/usr/bin/env python3

"""
inspired by https://stackoverflow.com/a/31005891/1164295
`ast` skips comments. To preserve commented lines, see https://docs.python.org/3/library/tokenize.html

WARNING: this script does NOT work with python 3.7
This file DOES work with Python 3.9
The cause is changes in https://docs.python.org/3/library/ast.html that occurred in 3.8 with ast.Str

This is similar to
https://github.com/YoloSwagTeam/ast2json/blob/master/ast2json/ast2json.py
except I don't keep the body of the function or the module or the class.

To troubleshoot, I find the following snippet useful:
import ast
with open('find_missing_docstring.py','r') as file_handle:
    tree = ast.parse(file_handle.read(), filename='find_missing_docstring.py')
"""

import ast # https://docs.python.org/3/library/ast.html
import sys
import glob
import os
import argparse # https://realpython.com/python-command-line-arguments/#argparse
import json


# https://realpython.com/python3-object-oriented-programming/
class Dog:
    pass

class Cat:
    # Class attribute
    species = "Canis familiaris"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    # Instance method
    def description(self):
        return f"{self.name} is {self.age} years old"

    # Another instance method
    def speak(self, sound):
        return f"{self.name} says {sound}"

class JackRussellTerrier(Cat):
    """
    great!
    """
    def speak(self, sound="Arf"):
        return f"{self.name} says {sound}"

class Dachshund(Dog):
    pass


def init_argparse() -> argparse.ArgumentParser:
    """
    from https://realpython.com/python-command-line-arguments/#argparse
    """
    parser = argparse.ArgumentParser(
        usage="%(prog)s [FILE or FOLDER]",
        description="determine whether modules, classes, and functions have a docstring"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('file_or_folder', nargs='*')
    return parser

def top_level_classes(body):
    return (f for f in body if isinstance(f, ast.ClassDef))

def top_level_functions(body):
    return (f for f in body if isinstance(f, ast.FunctionDef))

def top_level_comments(body):
    return (f for f in body if isinstance(f, ast.Expr)) # specific to Python 3.9+


def parse_ast_for_filename(filename: str):
    """
    >>> parse_ast_for_filename('file.py')
    """
    with open(filename, "rt") as file:
        return ast.parse(file.read(), filename=filename)

def docstring_in_module(tree) -> dict:
    """
    >>> docstring_in_module
    """
    for exp in top_level_comments(tree.body):
        if isinstance(exp.value, ast.Constant): # this skips commented lines and only finds module-level docstrings
            #print(exp.value.value)
            #print("   ",filename, "has module-level docstring\n")
            return {'has docstring':True} # has module-level docstring
    return {'has docstring':False}

def docstring_in_classes(tree) -> dict:
    """
    >>> docstring_in_classes(tree)
    """
    classes_dict = {}
    for cl in top_level_classes(tree.body):
        classes_dict[cl.name] = {'keywords':[ast.dump(_) for _ in cl.keywords]}
        classes_dict[cl.name] = {'bases':[ast.dump(_) for _ in cl.bases]}
        if isinstance(cl.body[0], ast.Expr):
            if isinstance(cl.body[0].value, ast.Constant):
                classes_dict[cl.name]['has docstring']=True
        else:
            classes_dict[cl.name]['has docstring']=False

        # functions within that class
        classes_dict[cl.name]['functions'] = docstring_in_functions(cl)
    return classes_dict

def docstring_in_functions(tree) -> list:
    """
    >>> docstring_in_functions(tree)
    """
    functions_dict = {}
    for func in top_level_functions(tree.body):
        functions_dict[func.name]={}
        functions_dict[func.name]['args'] = ast.dump(func.args)
        functions_dict[func.name]['decorators'] = [ast.dump(_) for _ in func.decorator_list]
        try:
            functions_dict[func.name]['type comment'] = ast.dump(func.type_comment)
        except TypeError:
            functions_dict[func.name]['type comment'] = None
        try:
            functions_dict[func.name]['returns'] = ast.dump(func.returns)
        except TypeError:
            functions_dict[func.name]['returns'] = None
        if isinstance(func.body[0], ast.Expr):
            if isinstance(func.body[0].value, ast.Constant):
                #print(func.body[0].value.value)
                functions_dict[func.name]['has docstring']=True
        else:
            #print('function "'+func.name+'" in '+filename+' does NOT have docstring')
            functions_dict[func.name]['has docstring']=False
    return functions_dict


if __name__ == "__main__":

    parser = init_argparse()
    args = parser.parse_args()

    if len(sys.argv)<2:
        print("ERROR: You need to pass either a folder name or a filename as argument")
        sys.exit(1)

    assessment_dict = {}

    for file_or_folder in args.file_or_folder:

        # https://pythonexamples.org/python-check-if-path-is-file-or-directory/
        if os.path.isfile(file_or_folder):
            tree = parse_ast_for_filename(file_or_folder)
            assessment_dict[file_or_folder] = {}
            assessment_dict[file_or_folder]['module'] = docstring_in_module(tree)
            assessment_dict[file_or_folder]['function'] = docstring_in_functions(tree)
            assessment_dict[file_or_folder]['class'] = docstring_in_classes(tree)

        elif os.path.isdir(file_or_folder):
            for filename in glob.glob(file_or_folder+"/**/*.py"):
                assessment_dict[file_or_folder] = {}

                tree = parse_ast_for_filename(filename)
                find_docstrings(tree, filename)
        else:
            print(file_or_folder,"is neither a file nor a folder")

    print(assessment_dict)
    # if write to file,
    with open('result.json', 'w') as fp:
        json.dump(assessment_dict, fp, indent=4, sort_keys=True) # sort_keys enabled to create a consistent ordering that enables comparison between changes
    # else write to stdout
    json.dump(assessment_dict, sys.stdout, indent=4, sort_keys=True)
