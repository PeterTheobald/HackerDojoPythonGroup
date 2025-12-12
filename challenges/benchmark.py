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
            }
        )
        if total_perf < best_total:
            best_total = total_perf
            best_idx = idx
    if verbose:
        print("\nBenchmark Results:")
        for i, res in enumerate(results):
            highlight = " <-- BEST" if i == best_idx else ""
            print(
                f"{res['title']:40} setup: {res['setup_time']:0.4f}s  total: {res['total_time']:0.4f}s  avg: {res['avg_time']*1e6:0.2f}us{highlight}"
            )
    return results
