import time
import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

URL = 'https://jsonplaceholder.typicode.com/posts'

# Number of requests to make
NUM_REQUESTS = 100


# Synchronous function to make a request
def fetch_sync(url):
    response = requests.get(url)
    return response.json()


# Asynchronous function to make a request
async def fetch_async(session, url):
    async with session.get(url) as response:
        return await response.json()


# Function to make requests using asyncio
async def fetch_all_async():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_async(session, URL) for _ in range(NUM_REQUESTS)]
        return await asyncio.gather(*tasks)


# Function to make requests using threading
def fetch_all_threading():
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_sync, URL) for _ in range(NUM_REQUESTS)
        ]
        return [future.result() for future in futures]


# Function to make requests using multiprocessing
def fetch_all_multiprocessing():
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_sync, URL) for _ in range(NUM_REQUESTS)
        ]
        return [future.result() for future in futures]


def measure_time(func):
    start_time = time.time()
    result = func()
    duration = time.time() - start_time
    return duration, result


def main():
    print("Starting synchronous requests...")
    duration_sync, _ = measure_time(
        lambda: [fetch_sync(URL) for _ in range(NUM_REQUESTS)])
    print(f"Synchronous: {duration_sync:.2f} seconds")

    print("Starting asyncio requests...")
    duration_async, _ = measure_time(lambda: asyncio.run(fetch_all_async()))
    print(f"Asyncio: {duration_async:.2f} seconds")

    print("Starting threading requests...")
    duration_threading, _ = measure_time(fetch_all_threading)
    print(f"Threading: {duration_threading:.2f} seconds")

    print("Starting multiprocessing requests...")
    duration_multiprocessing, _ = measure_time(fetch_all_multiprocessing)
    print(f"Multiprocessing: {duration_multiprocessing:.2f} seconds")


if __name__ == "__main__":
    main()
