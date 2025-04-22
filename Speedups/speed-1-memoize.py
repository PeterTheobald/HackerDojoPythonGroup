import time
from functools import lru_cache

# Recursive Fibonacci without memoization
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

# Recursive Fibonacci with memoization using lru_cache
@lru_cache(maxsize=None)
def fib_memoized(n):
    if n < 2:
        return n
    return fib_memoized(n-1) + fib_memoized(n-2)

def main():
    n = 40  # Choose a relatively large number to see the difference in performance

    # Measure time for the non-memoized version
    start_time = time.time()
    fib_result = fib(n)
    end_time = time.time()
    print(f"Non-memoized Fibonacci({n}) = {fib_result}, computed in {end_time - start_time:.4f} seconds")

    # Measure time for the memoized version
    start_time = time.time()
    fib_memoized_result = fib_memoized(n)
    end_time = time.time()
    print(f"Memoized Fibonacci({n}) = {fib_memoized_result}, computed in {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()

