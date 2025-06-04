import argparse
import asyncio
import time
import aiohttp

async def fetch(session, url):
    async with session.get(url) as resp:
        resp.raise_for_status()
        await resp.read()

async def run_load_test(url, n):
    start = time.perf_counter()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for _ in range(n)]
        await asyncio.gather(*tasks)
    total = time.perf_counter() - start
    print(f"Total elapsed time for {n} requests: {total:.4f}s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Async load test a webserver by requesting a URL multiple times"
    )
    parser.add_argument('url', help="The URL to request")
    parser.add_argument('-n', '--requests', type=int, default=100,
                        help="Number of concurrent requests (default: 100)")
    args = parser.parse_args()
    asyncio.run(run_load_test(args.url, args.requests))

