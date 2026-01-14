# benchmark.py
# Simple benchmarking library for running several different algorithms and comparing
# their runtime
# ControlAltPete 2026

# ToDo: Add @decorator support for easy function benchmarking
#       instead of requiring dicts with 'algorithm_fn' and 'setup_fn' keys
# ToDo: Add correctness checking support and reporting (optional expected result input)
# ToDo: Add memory usage tracking
# ToDo: Add more detailed statistical analysis (min, max, stddev)

import heapq
import random
import time
from typing import Any, Callable, Dict, List, Optional


def run(
    algorithms: List[Dict[str, Any]], REPEAT: int = 1000, verbose: bool = True
) -> List[Dict[str, Any]]:
    """
    Run a benchmark on a list of algorithms.
    Each algorithm is a dict with keys:
        'algorithm_fn': function to benchmark (takes setup result as input)
        'title': string title for reporting
        'setup_fn': function to call before timing (no args, returns input for algorithm_fn)
    """
    results: List[Dict[str, Any]] = []
    best_idx = None
    best_total = float("inf")
    num_algos = len(algorithms)

    for idx, algo in enumerate(algorithms):
        title = algo.get("title", "Untitled")
        algorithm_fn = algo["algorithm_fn"]
        setup_fn = algo.get("setup_fn", lambda: None)

        if verbose:
            print(f"[{idx+1}/{num_algos}] Running: {title}...", end="", flush=True)

        try:
            # Setup timing
            t_setup0 = time.perf_counter()
            setup_data = setup_fn()
            t_setup1 = time.perf_counter()
            setup_time = t_setup1 - t_setup0
            # Warmup (optional, not timed)
            algorithm_fn(setup_data)
            # Timing
            result = None
            t0 = time.perf_counter()

            # Show progress every 10% or at key intervals
            progress_interval = max(1, REPEAT // 10)
            for i in range(REPEAT):
                result = algorithm_fn(setup_data)
                if verbose and (i + 1) % progress_interval == 0:
                    percent = (i + 1) / REPEAT * 100
                    print(
                        f"\r[{idx+1}/{num_algos}] Running: {title}... {percent:.0f}%",
                        end="",
                        flush=True,
                    )

            t1 = time.perf_counter()
            elapsed = t1 - t0
            avg = elapsed / REPEAT
            total_perf = setup_time + elapsed

            if verbose:
                print(f"\r[{idx+1}/{num_algos}] Running: {title}... Done ({elapsed:.2f}s)")

            results.append(
                {
                    "title": title,
                    "setup_time": setup_time,
                    "total_time": elapsed,
                    "avg_time": avg,
                    "last_result": result,
                    "total_perf": total_perf,
                    "error": None,
                }
            )
            if total_perf < best_total:
                best_total = total_perf
                best_idx = idx
        except Exception as e:
            if verbose:
                print(f"\r[{idx+1}/{num_algos}] Running: {title}... ERROR: {e}")
            results.append(
                {
                    "title": title,
                    "setup_time": 0,
                    "total_time": float('inf'),
                    "avg_time": float('inf'),
                    "last_result": None,
                    "total_perf": float('inf'),
                    "error": str(e),
                }
            )
    if verbose:
        print("\nBenchmark Results:")
        for i, res in enumerate(results):
            if res['error']:
                print(f"{res['title']:40} ERROR: {res['error']}")
            else:
                if i == best_idx:
                    highlight = " <-- BEST"
                elif best_total > 0:
                    ratio = res['total_perf'] / best_total
                    highlight = f" ({ratio:.2f}x slower)"
                else:
                    highlight = ""
                print(
                    f"{res['title']:40} setup: {res['setup_time']:0.4f}s  total: {res['total_time']:0.4f}s  avg: {res['avg_time']*1e6:0.2f}us{highlight}"
                )
    return results



## DEMO - HOW TO USE:

def bubble_sort(a):
    a = list(a)  # copy so we don't mutate the input
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a

def heap_sort(iterable):
    h = list(iterable)
    heapq.heapify(h)
    return [heapq.heappop(h) for _ in range(len(h))]

def quicksort(a):
    a = list(a)
    if len(a) <= 1:
        return a
    pivot = a[len(a) // 2]
    left = [x for x in a if x < pivot]
    mid = [x for x in a if x == pivot]
    right = [x for x in a if x > pivot]
    return quicksort(left) + mid + quicksort(right)


def make_numbers(n, *, low=0, high=1_000_000, seed=None):
    rng = random.Random(seed)
    return [rng.randint(low, high) for _ in range(n)]


# Algorithm metadata - List your algorithms to compare
demo_algorithms = [
    {
        "title": "Bubble sort",
        "algorithm_fn": bubble_sort,
        "setup_fn": lambda: demo_data,
        "description": "Bubble sort: repeatedly step through the list, swapping adjacent out-of-order elements until a full pass makes no swaps."
    },
    {
        "title": "Timsort (built-in sorted)",
        "algorithm_fn": sorted,
        "setup_fn": lambda: demo_data,
        "description": "Timsort is a stable hybrid sorting algorithm that finds naturally occurring runs in the data and then merges them efficiently (combining ideas from merge sort and insertion sort)"
    },
    {
        "title": "Heap sort",
        "algorithm_fn": heap_sort,
        "setup_fn": lambda: demo_data,
        "description": "Heap sort builds a heap data structure and repeatedly extracts the minimum element to produce a sorted list."
    },
    {
        "title": "Quicksort",
        "algorithm_fn": quicksort,
        "setup_fn": lambda: demo_data,
        "description": "Quicksort recursively partitions the list around a chosen pivot so that smaller elements go to one side and larger elements to the other, then sorts each side."
    },
]

if __name__ == "__main__":
    demo_data = make_numbers(10_000)
    expected_result = sorted(demo_data)
    results = run(demo_algorithms, REPEAT=100) # import benchmark; benchmark.run()
    
    print("\nCorrectness Check:")
    all_correct = True
    for res in results:
        is_correct = res['last_result'] == expected_result
        status = "✓ CORRECT" if is_correct else "✗ INCORRECT"
        print(f"{res['title']:40} {status}")
        if not is_correct:
            all_correct = False
    
    if not all_correct:
        print("\n⚠ WARNING: Some algorithms produced incorrect results!")

