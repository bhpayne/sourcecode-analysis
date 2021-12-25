#!/usr/bin/env python3

"""
inspired by https://stackoverflow.com/a/31005891/1164295
`ast` skips comments. To preserve commented lines, see https://docs.python.org/3/library/tokenize.html
"""

import ast # https://docs.python.org/3/library/ast.html
import sys
import glob
import os

def top_level_classes(body):
    return (f for f in body if isinstance(f, ast.ClassDef))

def top_level_functions(body):
    return (f for f in body if isinstance(f, ast.FunctionDef))

def top_level_comments(body):
    return (f for f in body if isinstance(f, ast.Expr))


def parse_ast_for_filename(filename: str):
    """
    >>> parse_ast_for_filename('file.py')
    """
    with open(filename, "rt") as file:
        return ast.parse(file.read(), filename=filename)



def docstring_in_module(tree, filename: str) -> None:
    """
    >>> 
    """    
    file_does_not_have_modulelevel_docstring = True
    for exp in top_level_comments(tree.body):
        if isinstance(exp.value, ast.Constant): # this skips commented lines and only finds module-level docstrings
            #print(exp.value.value)
            #print("   ",filename, "has module-level docstring\n")
            file_does_not_have_modulelevel_docstring = False
    if file_does_not_have_modulelevel_docstring:
        print("file",filename, "does NOT has module-level docstring")
    return   

def docstring_in_classes(tree, filename: str) -> None:
    """
    >>> docstring_in_classes(tree)
    """   
    for cl in top_level_classes(tree.body):
        class_does_not_have_docstring = True
        if isinstance(cl.body[0], ast.Expr):
            if isinstance(cl.body[0].value, ast.Constant):
                class_does_not_have_docstring = False
        if class_does_not_have_docstring:
            print('class "'+cl.name+'" in '+filename+' does NOT have docstring')            
    return    

def docstring_in_functions(tree, filename: str) -> None:
    """
    >>> docstring_in_functions(tree)
    """    
    for func in top_level_functions(tree.body):
        #print(func.name)
        function_does_not_have_docstring = True
        if isinstance(func.body[0], ast.Expr):
            if isinstance(func.body[0].value, ast.Constant):
                #print(func.body[0].value.value)
                function_does_not_have_docstring = False
        if function_does_not_have_docstring:
            print('function "'+func.name+'" in '+filename+' does NOT have docstring')
    return

def find_docstrings(tree, filename: str) -> None:
    docstring_in_module(tree, filename)
    docstring_in_classes(tree, filename)
    docstring_in_functions(tree, filename)
    return

if __name__ == "__main__":

    if len(sys.argv)!=2:
        print("ERROR: You need to pass either a folder name or a filename as argument")
        sys.exit(1)

    print(sys.argv[1])

    # https://pythonexamples.org/python-check-if-path-is-file-or-directory/
    if os.path.isfile(sys.argv[1]):
        tree = parse_ast_for_filename(sys.argv[1])
        find_docstrings(tree, sys.argv[1])

    elif os.path.isdir(sys.argv[1]):
        for filename in glob.glob(sys.argv[1]+"/**/*.py"):
            tree = parse_ast_for_filename(filename)
            find_docstrings(tree, filename)
    else:
        print(sys.argv[1],"is neither a file nor a folder")


