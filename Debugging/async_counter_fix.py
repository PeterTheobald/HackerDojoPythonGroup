import asyncio

state = {'count': 0}
lock = asyncio.Lock()

async def worker():
    async with lock:
        tmp = state['count']
        await asyncio.sleep(0)
        state['count'] = tmp + 1

async def main():
    await asyncio.gather(*(worker() for _ in range(100)))
    print(state)

asyncio.run(main())

