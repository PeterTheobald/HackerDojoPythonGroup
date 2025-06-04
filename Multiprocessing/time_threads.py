# Run this in Python 3.13 (normal GIL locked threads) against Python 3.13t (GIL-less free-threaded) to compare
# uv run -p3.13 time_threads.py
# uv run -p3.13t time_threads.py

import threading
import time
import argparse

def cpu_bound_work(n):
    # simple CPU‐intensive task: sum of squares
    total = 0
    for i in range(n):
        total += i * i
    return total

def worker(n):
    cpu_bound_work(n)

def measure(num_threads, work_size):
    threads = []
    start = time.perf_counter()
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(work_size,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start
    print(f"Threads: {num_threads}, Work size: {work_size}, Time: {elapsed:.4f}s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Measure threading performance under GIL vs GIL-less Python"
    )
    parser.add_argument(
        "-t", "--threads", type=int, default=4,
        help="number of threads to spawn"
    )
    parser.add_argument(
        "-n", "--work", type=int, default=10_000_000,
        help="workload size per thread"
    )
    args = parser.parse_args()
    measure(args.threads, args.work)

