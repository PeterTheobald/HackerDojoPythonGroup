# Given a list of 1 million random integers with values from 0 to 999, find the number that appears the most.

import os
import sys
import sysconfig
import time
from collections import Counter

import numpy as np
from concurrent.futures import ThreadPoolExecutor
import statistics as stats
from typing import Callable, Iterable, Dict, List, Tuple

# Here are my solutions:

# Naiive first solution, slow O(n)
# Specifically loops x 1,000,000 once to build counter,
# then loops x 1000 to find max(counter)
# O(n)

def most_common_simple(l):
    counter={}
    for num in l:
        if num in counter:
            counter[num]+=1
        else:
            counter[num]=1
    return max(counter, key=lambda k: counter[k])

# Using Python's built in libraries:
# Also O(n) but calling highly optimized C functions

def most_common_counter(l):
    return Counter(l).most_common(1)[0][0]

# Even using built in Counter can be beat. Counter uses a dict
# internally. Dicts have a lot of overhead.
# Since we know ahead of time the numbers can only be 0-999,
# let's pre-allocate a 1,000 array of counters and directly
# increment them:

def most_common_array(nums: List[int]) -> int:
    # nums can only be 0-999
    counts = [0] * 1000
    for x in nums:
        counts[x] += 1
    return max(range(1000), key=counts.__getitem__)

# How could we beat that? Use numpy. numpy has this
# operation built in:

def most_common_numpy(nums):
    return int(np.bincount(nums, minlength=1000).argmax())

# How could we possibly beat highly optimized C solution?
# Multithreading. Break the list into p parts,
# where p matches the number of cpu cores we have.
# Calc the counters of each part,
# Merge the results and find the max count

def most_common_parallel(nums, p=None, k=1000) -> int:
    arr = np.asarray(nums, dtype=np.int32)
    chunks = np.array_split(arr, p or os.cpu_count() or 4)

    def hist(a): return np.bincount(a, minlength=k)

    totals = np.zeros(k, dtype=np.int64)
    with ThreadPoolExecutor(max_workers=len(chunks)) as ex:
        for h in ex.map(hist, (c for c in chunks if c.size)):
            np.add(totals, h, out=totals)   # no temporary stack
    return int(totals.argmax())


# Now wrap it all up in a framework that tries each of these
# and times them.

REPEAT=1000

def benchmark( fn: Callable, data: Iterable[int]) -> Tuple[int, float, float, float]:
    _ = fn(data) # call it once throw-away to warm up any caches etc.
    times = []
    result = None
    for _ in range(REPEAT):
        t_start = time.perf_counter()
        result = fn(data)
        t_end = time.perf_counter()
        times.append(t_end - t_start)
    return result, min(times), stats.mean(times), sum(times)

def is_nogil_python() -> bool:
    return sysconfig.get_config_var("Py_GIL_DISABLED") == 1 and not sys._is_gil_enabled()

def main():
    rng = np.random.default_rng()
    # nums_np= rng.integers(0, 1000, size=1_000_000, dtype=np.int32)
    nums_np= rng.integers(0, 1000, size=10_000_000, dtype=np.int32)
    nums_list = nums_np.tolist()

    if is_nogil_python():
        print(f'(Note: Running threaded algorithm in NOGIL Python, with {os.cpu_count()} cores)')
    else:
        print('Warning: Running threaded algorithm in crippled GIL Python')
        print('         try running with `uv run --python 3.14t most_common_number.py`')

    tests = [
        ("simple", most_common_simple, nums_list),
        ("counter", most_common_counter, nums_list),
        ("array", most_common_array, nums_list),
        ("numpy", most_common_numpy, nums_np),
        ("parallel", most_common_parallel, nums_np)
    ]
    for name, fn, data in tests:
        result, best_time, avg_time, total_time = benchmark( fn, data)
        print(f"{name:>10}  result={result:4d}, best time={best_time*1000:8.2f} ms, avg time={avg_time*1000:8.2f} ms, total_time={total_time*1000:10.2f} ms")


if __name__ == "__main__":
    main()

