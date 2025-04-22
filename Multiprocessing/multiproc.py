#################################
# Multiprocessing
# 1. asyncio
# 2. threading
# 3. multiprocessing
# 4. subprocess
###############################################

########
# Remember threading:
#    create Thread
#    thread.start
#    thread.join
#
#    create Thread.lock
#    with lock: (acquire, release)
#
#    create Queue
#    queue.put
#    queue.get
#    queue.task_done

import multiprocessing


def worker():
  print("Worker Function Executing")


if __name__ == '__main__':
  # Create a process object
  p = multiprocessing.Process(target=worker)
  # Start the process
  p.start()
  # Wait for the process to finish
  p.join()
  print("Main Process Ends")

#############

from multiprocessing import Pool


def square_number(n):
  return n * n


if __name__ == '__main__':
  # Define the dataset
  numbers = [1, 2, 3, 4, 5]
  # Create a pool of workers
  with Pool(5) as p:
    results = p.map(square_number, numbers)
  print(results)

###########

from multiprocessing import Process, Queue


def worker(q, value):
  q.put(value**2)


if __name__ == '__main__':
  q = Queue()
  processes = [Process(target=worker, args=(q, i)) for i in range(5)]
  for p in processes:
    p.start()
  for p in processes:
    p.join()
  while not q.empty():
    print(q.get())

###################

import multiprocessing


def increment(shared_value):
  with shared_value.get_lock():  # Use the lock to prevent race conditions
    shared_value.value += 1


if __name__ == '__main__':
  # Shared integer
  counter = multiprocessing.Value('i', 0)

  # List of processes
  processes = [
    multiprocessing.Process(target=increment, args=(counter, ))
    for _ in range(10)
  ]

  # Start all processes
  for p in processes:
    p.start()

  # Wait for all processes to complete
  for p in processes:
    p.join()

  print(f"Counter value after all increments: {counter.value}")

#######################

import multiprocessing


def process_with_lock(lock, data):
  with lock:
    print(f"Process {multiprocessing.current_process().name} modifying data")
    data.value += 1  # Safely updating a shared value


def process_without_lock(data):
  print(f"Process {multiprocessing.current_process().name} modifying data")
  data.value += 1  # Unsafe update might lead to a race condition


if __name__ == '__main__':
  # Shared data
  shared_data = multiprocessing.Value('i', 0)  # 'i' indicates an integer

  # Lock object
  lock = multiprocessing.Lock()

  # Creating processes that use the lock
  processes = [
    multiprocessing.Process(target=process_with_lock, args=(lock, shared_data))
    for _ in range(5)
  ]

  # Start and join the processes
  for p in processes:
    p.start()
  for p in processes:
    p.join()

  print(f"Value of shared data with lock: {shared_data.value}")

  # Reset shared data
  shared_data.value = 0

  # Creating processes that do not use the lock
  processes = [
    multiprocessing.Process(target=process_without_lock, args=(shared_data, ))
    for _ in range(5)
  ]

  # Start and join the processes
  for p in processes:
    p.start()
  for p in processes:
    p.join()

  print(f"Value of shared data without lock: {shared_data.value}")

############
# multiprocessing.Array
############

# Deadlocks
# and Race Conditions
