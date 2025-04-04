## Techniques for troubleshooting a memory leak in Python:

### Tools:

- tracemalloc – Track memory allocations.
- objgraph – Visualize object references and growth.
- gc - Monitor with gc module – Inspect uncollected objects and debug garbage collection.
- memory_profiler
- pympler
- guppy3 (includes heapy)

### Techniques:

Check for reference cycles – Especially with custom classes or closures.
Use weak references – With weakref to avoid unintended retention.
Track object counts over time – With sys.getobjects() or gc.get_objects().
Valgrind + Python Debug Build – For low-level leaks in C extensions.
