import random
import time
import asyncio

def tic():
  return 'at %1.1f seconds' % (time.time() - start)
  
def task(pid):
  """Synchronous non-deterministic task."""
  time.sleep(random.randint(0, 5) * 0.5)
  print('Task %s done' % pid)


async def task_coro(pid):
  """Coroutine non-deterministic task"""
  await asyncio.sleep(random.randint(0, 5) * 0.5)
  print('Task %s done' % pid)


def synchronous():
  for i in range(1, 10):
    task(i)


async def asynchronous():
  tasks = [task_coro(i) for i in range(1, 10)]
  await asyncio.gather(*tasks)


print('Synchronous:')
start=time.time()
print(f'Start at {tic()}')
synchronous()
print(f'Done at {tic()}')

print('Asynchronous:')
start=time.time()
print(f'Start at {tic()}')
asyncio.run(asynchronous())
print(f'Done at {tic()}')
