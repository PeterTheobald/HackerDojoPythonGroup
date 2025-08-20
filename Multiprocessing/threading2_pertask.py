# Thread-per-task URL fetcher using requests; downloads the entire page
import threading, time, requests

def fetch_url(url: str) -> None:
    start = time.perf_counter()
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status() # if response code is 400/404/500 etc raise exception
        data = r.content  # full response body (bytes)
        status = r.status_code
    except Exception as e:
        print(f"{url} -> ERROR: {e}")
    else:
        dt = time.perf_counter() - start
        print(f"{url} -> {status} in {dt:.2f}s, size={len(data)} bytes")

def main(urls: list[str]) -> None:
    threads = []
    for u in urls:
        t = threading.Thread(target=fetch_url, args=(u,), daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/bytes/50000",
    ]
    main(urls)
