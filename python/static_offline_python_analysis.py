#!/usr/bin/env python3

"""
inspired by https://stackoverflow.com/a/31005891/1164295
`ast` skips comments. To preserve commented lines, see https://docs.python.org/3/library/tokenize.html

WARNING: this script does NOT work with python 3.7
This file DOES work with Python 3.9
The cause is changes in https://docs.python.org/3/library/ast.html that occurred in 3.8 with ast.Str

CAVEAT: This script does not recursively assess classes and functions.
The current implementation is limited to modules, top-level classes, top-level functions, and functions within classes.
For example, functions within functions are not assessed.

CAVEAT: this script breaks if a Python2 file is passed in

This code is similar to
https://github.com/YoloSwagTeam/ast2json/blob/master/ast2json/ast2json.py
except I don't keep the body of the function or the module or the class.

To troubleshoot, the following snippet is useful:
import ast
with open('static_offline_python_analysis.py','r') as file_handle:
    tree = ast.parse(file_handle.read(), filename='static_offline_python_analysis.py')
"""

import sys
MIN_PYTHON = (3, 8) # https://stackoverflow.com/a/57446368/1164295
assert sys.version_info >= MIN_PYTHON, sys.exit("ERROR: Minimm version NOT met; requires Python "+str('.'.join([str(n) for n in MIN_PYTHON]))+" or newer.")

import subprocess
import ast # https://docs.python.org/3/library/ast.html
import glob
import os
import argparse # https://realpython.com/python-command-line-arguments/#argparse
import json



def init_argparse() -> argparse.ArgumentParser:
    """
    from https://realpython.com/python-command-line-arguments/#argparse
    """
    parser = argparse.ArgumentParser(
        usage="%(prog)s [one or more FILEs or FOLDERs]",
        description="determine whether modules, classes, and functions have a docstring"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('file_or_folder', nargs='*')
    return parser

def top_level_classes(body):
    """
    find classes in the AST body
    """
    return (f for f in body if isinstance(f, ast.ClassDef))

def top_level_functions(body):
    """
    find functions in the AST body
    """
    return (f for f in body if isinstance(f, ast.FunctionDef))

def top_level_comments(body):
    return (f for f in body if isinstance(f, ast.Expr)) # specific to Python 3.9+


def parse_ast_for_filename(filename: str) -> str:
    """
    >>> parse_ast_for_filename('file.py')
    """
    with open(filename, "rt") as file:
        return ast.parse(file.read(), filename=filename)

def analysis_of_module(tree) -> dict:
    """
    >>> analysis_of_module(tree)
    """
    for exp in top_level_comments(tree.body):
        if isinstance(exp.value, ast.Constant): # this skips commented lines and only finds module-level docstrings
            #print(exp.value.value)
            #print("   ",filename, "has module-level docstring\n")
            return {'has docstring':True} # has module-level docstring
    return {'has docstring':False}

def analysis_of_classes(tree) -> dict:
    """
    >>> analysis_of_classes(tree)
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
        classes_dict[cl.name]['functions'] = analysis_of_functions(cl)
    return classes_dict

def analysis_of_functions(tree) -> dict:
    """
    >>> analysis_of_functions(tree)
    """
    functions_dict = {}
    for func in top_level_functions(tree.body):
        functions_dict[func.name]={}
        # functions_dict[func.name]['args'] = ast.dump(func.args)
        #posonlyargs=[], args=[arg(arg='body')], kwonlyargs=[], kw_defaults=[], defaults
        functions_dict[func.name]['posonlyargs'] = [ast.dump(_) for _ in func.args.posonlyargs]
        args_dict = {}
        for this_arg in func.args.args:
            #print(this_arg.arg) # argument name is not important since argument names can change without breaking the API
            #print(this_arg.annotation.id) # variable type
            try:
                args_dict[this_arg.arg] = this_arg.annotation.id
            except AttributeError:
                args_dict[this_arg.arg] = None # argument type not specified
        functions_dict[func.name]['args'] = args_dict
        functions_dict[func.name]['kwonlyargs'] = [ast.dump(_) for _ in func.args.kwonlyargs]
        functions_dict[func.name]['kw_defaults'] = [ast.dump(_) for _ in func.args.kw_defaults]
        functions_dict[func.name]['defaults'] = [ast.dump(_) for _ in func.args.defaults]

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

def assess_file(filename: str) -> dict:
    tree = parse_ast_for_filename(filename)
    assessment_dict = {}
    assessment_dict['module'] = analysis_of_module(tree)
    assessment_dict['function'] = analysis_of_functions(tree)
    assessment_dict['class'] = analysis_of_classes(tree)

    # https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
    result = subprocess.run(['python3',file_or_folder,'--help'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    help_output_str = result.stdout.decode('utf-8')
    if len(help_output_str)>1:
        assessment_dict['module']['has --help'] = help_output_str.split('\n')
    else:
        assessment_dict['module']['has --help'] = None
    return assessment_dict

if __name__ == "__main__":

    parser = init_argparse()
    args = parser.parse_args()

    if len(sys.argv)<2:
        sys.exit("ERROR: You need to pass either a folder name or a filename as argument")

    assessment_dict = {}

    for file_or_folder in args.file_or_folder:

        # https://pythonexamples.org/python-check-if-path-is-file-or-directory/
        if os.path.isfile(file_or_folder):
            print("file:",file_or_folder)
            assessment_dict[file_or_folder] = assess_file(file_or_folder)

        elif os.path.isdir(file_or_folder):
            print("folder:",file_or_folder)
            # https://stackoverflow.com/questions/2186525/how-to-use-glob-to-find-files-recursively
            list_of_py_files = glob.glob(file_or_folder+"/**/*.py", recursive=True)
            print("all py files in folder:",list_of_py_files)
            for filename in list_of_py_files:
                print("filename in folder:",filename)
                assessment_dict[filename] = assess_file(filename)
        else:
            print(file_or_folder,"is neither a file nor a folder")

#    print(assessment_dict)
    # if write to file,
    with open('result.json', 'w') as fp:
        json.dump(assessment_dict, fp, indent=4, sort_keys=True) # sort_keys enabled to create a consistent ordering that enables comparison between changes
    # else write to stdout
    json.dump(assessment_dict, sys.stdout, indent=4, sort_keys=True)
