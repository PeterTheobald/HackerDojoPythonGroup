import time
import matplotlib.pyplot as plt



def benchmark_two_sums(sample_func, label=None):
    sizes = [10, 100, 1000, 5000, 10000, 20000]
    times = []
    target = 123456
    for n in sizes:
        nums = generate_unique_sum_list(n, target)
        start = time.time()
        sample_func(nums, target)
        end = time.time()
        times.append(end - start)
        print(f"{label or sample_func.__name__}: n={n}, time={end-start:.6f}s")
    plt.plot(sizes, times, marker='o', label=label or sample_func.__name__)
import random

def generate_unique_sum_list(n, t):
    if n < 2:
        raise ValueError("List must have at least 2 elements.")
    # Pick two numbers that sum to t
    a = random.randint(1, t-1)
    b = t - a
    result = [a, b]
    # Fill the rest with numbers that cannot form t with any other
    forbidden = {a, b}
    while len(result) < n:
        # Pick a number not in forbidden and not forming t with any in result
        candidate = random.randint(-10*n, 10*n)
        if candidate in forbidden:
            continue
        if any(candidate + x == t for x in result): # compare to any([candidate + x == t for x in result])
            continue
        result.append(candidate)
        forbidden.add(t - candidate) # don't allow its complement
    random.shuffle(result)
    return result

#########################################

def pete_find_two_sums(nums, target):
    # O(n) solution that remembers seen numbers in a dictionary
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None


if __name__ == "__main__":
    plt.figure(figsize=(10,6))
    benchmark_two_sums(pete_find_two_sums)
    plt.xlabel('List size (n)')
    plt.ylabel('Execution time (seconds)')
    plt.title('Two Sums Scalability')
    plt.grid(True)
    plt.legend()
    plt.show()