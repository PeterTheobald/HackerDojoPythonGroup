# Benchmark

A simple, easy-to-use Python benchmarking library for comparing algorithm performance.

## Features

- 🚀 **Simple API** - Compare multiple algorithms with just a few lines of code
- 📊 **Detailed Results** - Get setup time, total time, average time, and performance comparisons
- 🔄 **Progress Tracking** - Real-time progress updates during long-running benchmarks
- 🛡️ **Error Handling** - Gracefully handles algorithm failures without stopping the entire benchmark
- 📈 **Performance Ratios** - Automatically shows how much slower each algorithm is compared to the best

## Installation

```bash
pip install benchmark
```

## Quick Start

```python
import benchmark

# Define your algorithms to compare
algorithms = [
    {
        "title": "Bubble Sort",
        "algorithm_fn": bubble_sort,
        "setup_fn": lambda: [3, 1, 4, 1, 5, 9, 2, 6]
    },
    {
        "title": "Python's sorted()",
        "algorithm_fn": sorted,
        "setup_fn": lambda: [3, 1, 4, 1, 5, 9, 2, 6]
    }
]

# Run the benchmark
results = benchmark.run(algorithms, REPEAT=1000)
```

## Usage

### Basic Example

```python
import benchmark

def algorithm1(data):
    return sorted(data)

def algorithm2(data):
    return list(reversed(sorted(data, reverse=True)))

algorithms = [
    {
        "title": "Standard sort",
        "algorithm_fn": algorithm1,
        "setup_fn": lambda: [5, 2, 8, 1, 9]
    },
    {
        "title": "Reverse then reverse",
        "algorithm_fn": algorithm2,
        "setup_fn": lambda: [5, 2, 8, 1, 9]
    }
]

results = benchmark.run(algorithms, REPEAT=10000, verbose=True)
```

### Output Example

```
[1/2] Running: Standard sort... Done (0.05s)
[2/2] Running: Reverse then reverse... Done (0.08s)

Benchmark Results:
Standard sort                       setup: 0.0000s  total: 0.0500s  avg: 5.00us <-- BEST
Reverse then reverse                setup: 0.0000s  total: 0.0800s  avg: 8.00us (1.60x slower)
```

## API Reference

### `benchmark.run(algorithms, REPEAT=1000, verbose=True)`

Run a benchmark comparing multiple algorithms.

**Parameters:**
- `algorithms` (List[Dict]): List of algorithm dictionaries with keys:
  - `algorithm_fn` (Callable): The function to benchmark
  - `title` (str): Display name for the algorithm
  - `setup_fn` (Callable, optional): Function called before timing to prepare test data
- `REPEAT` (int, default=1000): Number of times to run each algorithm
- `verbose` (bool, default=True): Whether to print progress and results

**Returns:**
- List[Dict]: Results for each algorithm containing:
  - `title`: Algorithm name
  - `setup_time`: Time spent in setup
  - `total_time`: Total execution time
  - `avg_time`: Average time per iteration
  - `last_result`: Result from the last iteration
  - `total_perf`: Combined setup + execution time
  - `error`: Error message if the algorithm failed, None otherwise

## Examples

See the included demo in `benchmark.py` which compares sorting algorithms:
- Bubble Sort
- Timsort (Python's built-in `sorted()`)
- Heap Sort
- Quicksort

## Requirements

- Python >= 3.7

## License

MIT License

## Author

ControlAltPete (peter@petertheobald.com)
