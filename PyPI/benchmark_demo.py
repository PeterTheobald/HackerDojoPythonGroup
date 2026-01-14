# benchmark_demo.py
# Demo showing how to use the benchmark library to compare sorting algorithms
# ControlAltPete 2026

import heapq
import random

import benchmark


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
    results = benchmark.run(demo_algorithms, REPEAT=100)
    
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

