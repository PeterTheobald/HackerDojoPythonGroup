Python speedup: 
1. Better algorithm beats everything else. Memoize lru_cache. Dicts have O(1) lookup, binary search has O(log n) lookup, linear search of a list has O(n) lookup. (see speed-n-...py)
2. list comprehension > loops. join strings is faster than repeatedly appending to strings with + or in a loop. map lists instead of looping over them.
3. Compiled library functions > hand written python. Look in collections, itertools, functools. Numpy for math. Pandas for tables of data.
4. For I/O bound problems, use asyncio, threading, multiprocessing (see speed-compare-IO.py)
5. profile to find where it is slow, don't waste effort optimizing where it wont make much difference. cProfile, line_profiler, memory_profiler
6. Compilers (see matrix-n-...py)
  1. cpython 3.12 (baseline)
  2. numpy library
  3. PyPy
  4. numba (numpy arrays, jit, gpu, parallel)
  5. cython (not cpython) needs code changes
  6. codon

*Note: diagram of matrix multiply* https://en.wikipedia.org/wiki/Matrix_multiplication#/media/File:Matrix_multiplication_diagram_2.svg

