# source code analysis

## Dynamic (requires execution) profiling and tracing

<https://pycallgraph.readthedocs.io/en/master/> - creates call graph visualizations for Python applications.

<https://github.com/jrfonseca/gprof2dot/> - convert the output from many profilers into a dot graph

<https://realpython.com/python-debugging-pdb/> - Python debugger

<https://pypi.org/project/memory-profiler/>

<https://coverage.readthedocs.io/en/stable/> - measures code coverage of Python programs. It monitors your program, noting which parts of the code have been executed, then analyzes the source to identify code that could have been executed but was not.

See <https://nedbatchelder.com/text/trace-function.html> for an explanation of coverage.py

Almost all of those capabilities rely on `sys.settrace()`. For an overview, see <https://pymotw.com/3/sys/tracing.html>

Problem: `sys.settrace()` and `inspect` both rely on running the code. If there are unresolved dependencies, the module won't import. 

## Static (offline) analysis

<https://stackoverflow.com/a/31005891/1164295> led me to

### Python's Abstract Syntax Tree (AST)

<https://docs.python.org/3/library/ast.html>  

<https://greentreesnakes.readthedocs.io/en/latest/>
