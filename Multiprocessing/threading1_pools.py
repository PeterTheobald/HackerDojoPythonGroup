# /// script
# requires-python = "==3.14+freethreaded"
# dependencies = []
# ///

import concurrent.futures as cf
import time, random

def handle_request(record_id: int) -> tuple[int, float]:
    # Get record from the database across the network
    # just kidding, pretend we did
    t = random.uniform(0.1, 0.5)
    time.sleep(t)
    return record_id, t

if __name__ == "__main__":
    record_ids = range(10)

    # Fixed-size pool; submit tasks and collect results
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        workers = [pool.submit(handle_request, id) for id in record_ids]
        for w in cf.as_completed(workers):
            rec_id, latency = w.result()
            print(f"record {rec_id} took {latency:.3f}s")

