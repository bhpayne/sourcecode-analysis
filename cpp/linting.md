

# clang-tidy

<https://www.reddit.com/r/cpp/comments/5b397d/what_c_linter_do_you_use/>
points to
<https://clang.llvm.org/extra/clang-tidy/>


"`clang-tidy` figures out dead code, unreachable code, code which is ambiguous in meaning, calls of virtual function from destructors which is bad, imprecise casting, and so on."


tip: try clang-tidy -fix, it'll auto rewrite your code to fix the lint problems. Doesn't always get it right, plus it can eat your code so don't run it unsupervised, but -fix is an amazing time saver)

tip 2: clang-tidy can be configured to lint all-MSVC projects with the right magic settings. Google did a really amazing job with this lint tool, even clang-tidy 3.7 wasn't a patch on clang-tidy 3.9 and clang-tidy 4.0 is looking even better again)

tip 3: cmake 3.6 and later can be asked to call clang-tidy magically for you with no further configuration if you're using either Makefiles or Ninja. And this works just fine on a MSVC only build)

# cppcheck

<https://cppcheck.sourceforge.io/>

