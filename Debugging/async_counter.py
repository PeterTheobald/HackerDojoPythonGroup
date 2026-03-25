import asyncio

state = {'count': 0}

async def worker(i):
    tmp = state['count']
    print(f"worker {i} read {tmp}")
    await asyncio.sleep(0)
    state['count'] = tmp + 1
    print(f"worker {i} wrote {state['count']}")

async def main():
    await asyncio.gather(*(worker(i) for i in range(5)))
    print(state)

asyncio.run(main())

