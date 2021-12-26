# source code analysis for C++

<https://github.com/foonathan/cppast>

# Clang-based

background: <https://jonasdevlieghere.com/understanding-the-clang-ast/>

<https://stackoverflow.com/questions/18560019/how-to-view-clang-ast>

see <https://stackoverflow.com/questions/59102944/how-to-represent-clang-ast-in-json-format>

<https://github.com/JhnW/devana>

<https://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang>

<https://clang.llvm.org/docs/IntroductionToTheClangAST.html>

```
clang++ -cc1 -ast-dump test.cpp
```

<https://releases.llvm.org/3.3/tools/clang/docs/IntroductionToTheClangAST.html>
```
clang++ -cc1 -ast-dump-xml test.cpp
```
`-ast-dump-xml` only works with debug builds of clang.
<https://stackoverflow.com/a/5352066/1164295>


<https://www.nobugs.org/developer/parsingcpp/>

# GCC based

<https://www.gccxml.org/HTML/Index.html>

<https://github.com/CastXML/pygccxml>

