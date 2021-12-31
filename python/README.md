# Static (offline) source code analysis of Python

The file `static_offline_python_analysis.py` consumes one or more folders or files
and then analyses the API of each .py file.

`static_offline_python_analysis.py` uses Python's Abstract Syntax Tree (AST);
see <https://docs.python.org/3/library/ast.html>  
and <https://greentreesnakes.readthedocs.io/en/latest/>


The file `static_offline_python_analysis.py` produces a JSON file.
The JSON file could be used to compare with previous snapshots using `jsondiff`; see
<https://stackoverflow.com/a/39663267/1164295>

A report about the JSON file can generated using `analyze_json.py`.


# Survey of static (offline) analysis for Python

See <https://luminousmen.com/post/python-static-analysis-tools>

### MyPy - type checking of type hints
<http://mypy-lang.org/>

### Prospector
<https://prospector.landscape.io/en/master/>

Runs multiple tools, including dodgy, mccabe, pep8, profile-validator, pyflakes, pylint

```
prospector filename.py
```
Produces a report

### Pyflakes
<https://pypi.org/project/pyflakes/> and <https://pypi.org/project/autoflake/>

```
pyflakes filename.py
```

### Pylint

```
pylint filename.py
```
Produces a numeric rating (out of 10). 

# Survey of Dynamic (requires execution) profiling and tracing for Python

<https://pycallgraph.readthedocs.io/en/master/> - creates call graph visualizations for Python applications.

<https://github.com/jrfonseca/gprof2dot/> - convert the output from many profilers into a dot graph

<https://realpython.com/python-debugging-pdb/> - Python debugger

<https://pypi.org/project/memory-profiler/>

<https://coverage.readthedocs.io/en/stable/> - measures code coverage of Python programs. It monitors your program, noting which parts of the code have been executed, then analyzes the source to identify code that could have been executed but was not.

See <https://nedbatchelder.com/text/trace-function.html> for an explanation of coverage.py

Almost all of those capabilities rely on `sys.settrace()`. For an overview, see <https://pymotw.com/3/sys/tracing.html>

Problem: `sys.settrace()` and `inspect` both rely on running the code. If there are unresolved dependencies, the module won't import.
