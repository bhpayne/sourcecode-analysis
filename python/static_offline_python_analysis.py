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
--> If maintaining this code is burdensome; switch to "ast2json" and ignore the body

To troubleshoot, the following snippet is useful:
import ast
with open('static_offline_python_analysis.py','r') as file_handle:
    tree = ast.parse(file_handle.read(), filename='static_offline_python_analysis.py')
tree.body
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
from matplotlib import pyplot as plt


def init_argparse() -> argparse.ArgumentParser:
    """
    https://docs.python.org/3/howto/argparse.html
    https://docs.python.org/3/library/argparse.html
    from https://realpython.com/python-command-line-arguments/#argparse
    """
    parser = argparse.ArgumentParser(
        usage="%(prog)s [one or more FILEs or FOLDERs]",
        description="determine whether modules, classes, and functions have a docstring"
    )
    # required positional argument
    parser.add_argument('file_or_folder',
                        nargs='*') # The number of command-line arguments that should be consumed.

    # optional argument
    parser.add_argument(
        "-v", "--version",
#        nargs=None,
        action="version",
        version = f"{parser.prog} version 1.0.0" # https://docs.python.org/3/library/argparse.html#prog
    )

    # optional argument
    parser.add_argument(
             '--output_json_filename',
             nargs=1,
             default=["result"],
             help="if output filename is not provided, defaults to 'result.json'")
    return parser

def top_level_classes(body):
    """
    find classes in the AST body

    >>> top_level_classes(body)
    """
    return (f for f in body if isinstance(f, ast.ClassDef))

def top_level_functions(body):
    """
    find functions in the AST body
    """
    return (f for f in body if isinstance(f, ast.FunctionDef))


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
    module_dict = {}
    for entry in tree.body:
        if isinstance(entry, ast.Expr): # specific to Python 3.9+
            if isinstance(entry.value, ast.Constant): # this skips commented lines and only finds module-level docstrings
                #print(entry.value.value)
                #print("   ",filename, "has module-level docstring\n")
                module_dict['has docstring']=True # has module-level docstring
                break #  terminates the current loop
            else:
                module_dict['has docstring']=False
            break #  terminates the current loop

    list_of_imports = []
    for entry in tree.body:
        if isinstance(entry, ast.Import):
            list_of_imports.append(entry.names[0].name)
        if isinstance(entry, ast.ImportFrom):
            list_of_imports.append(entry.module)

    module_dict['imports'] = list_of_imports

    # does module have  if __name__ == "__main__" ?
    # https://docs.python.org/3/library/__main__.html
    # Why this matters: enables the .py to be called by other scripts without executing
    module_dict['has __name__==__main__'] = False
    for entry in tree.body:
        if isinstance(entry, ast.If):
            if entry.test.left.id == "__name__" or entry.test.left.id == "__main__":
                module_dict['has __name__==__main__'] = True

    return module_dict

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
        except TypeError: # return type not specified
            functions_dict[func.name]['returns'] = 'not specified'
        if isinstance(func.body[0], ast.Expr):
            if isinstance(func.body[0].value, ast.Constant):
                #print(func.body[0].value.value)
                functions_dict[func.name]['has docstring']=True
        else:
            #print('function "'+func.name+'" in '+filename+' does NOT have docstring')
            functions_dict[func.name]['has docstring']=False
    return functions_dict

def assess_file(filename: str) -> dict:
    """
    filename: a valid path to a Python file
    """
    tree = parse_ast_for_filename(filename)
    assessment_dict = {}
    assessment_dict['module'] = analysis_of_module(tree)
    assessment_dict['function'] = analysis_of_functions(tree)
    assessment_dict['class'] = analysis_of_classes(tree)

    # https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
    result = subprocess.run(['python3',filename,'--help'],
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
    with open(args.output_json_filename[0]+'.json', 'w') as fp:
        json.dump(assessment_dict, fp, indent=4, sort_keys=True) # sort_keys enabled to create a consistent ordering that enables comparison between changes
    # else write to stdout
    json.dump(assessment_dict, sys.stdout, indent=4, sort_keys=True)
