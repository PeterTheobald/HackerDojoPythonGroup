
import time

def run(algorithms, REPEAT=1000, verbose=True):
    """
    Run a benchmark on a list of algorithms.
    Each algorithm is a dict with keys:
        'method_fn': function to benchmark (takes setup result as input)
        'title': string title for reporting
        'setup_fn': function to call before timing (no args, returns input for method_fn)
    """
    results = []
    best_idx = None
    best_total = float('inf')
    for idx, algo in enumerate(algorithms):
        title = algo.get('title', 'Untitled')
        method_fn = algo['method_fn']
        setup_fn = algo.get('setup_fn', lambda: None)
        # Setup timing
        t_setup0 = time.perf_counter()
        setup_data = setup_fn()
        t_setup1 = time.perf_counter()
        setup_time = t_setup1 - t_setup0
        # Warmup (optional, not timed)
        method_fn(setup_data)
        # Timing
        result = None
        t0 = time.perf_counter()
        for _ in range(REPEAT):
            result = method_fn(setup_data)
        t1 = time.perf_counter()
        elapsed = t1 - t0
        avg = elapsed / REPEAT
        total_perf = setup_time + elapsed
        results.append({
            'title': title,
            'setup_time': setup_time,
            'total_time': elapsed,
            'avg_time': avg,
            'last_result': result,
            'total_perf': total_perf
        })
        if total_perf < best_total:
            best_total = total_perf
            best_idx = idx
    if verbose:
        print("\nBenchmark Results:")
        for i, res in enumerate(results):
            highlight = " <-- BEST" if i == best_idx else ""
            print(f"{res['title']:40} setup: {res['setup_time']:0.4f}s  total: {res['total_time']:0.4f}s  avg: {res['avg_time']*1e6:0.2f}us{highlight}")
    return results
