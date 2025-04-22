import queue
import time
import random
import threading
import time
import sys
import math
from timeit import default_timer as timer
from datetime import timedelta

#################################
# Multiprocessing
# 1. asyncio
# 2. threading
# 3. multiprocessing
# 4. subprocess
###############################################


def example1():
  print('Running two things "at once" I/O bound')
  print('single threaded:')
  start = timer()
  print_numbers()
  print_letters()
  stop = timer()
  print(f'done in {timedelta(seconds=stop-start)} seconds.')

  print('multi-threaded:')
  start = timer()
  # Creating threads
  thread1 = threading.Thread(target=print_numbers)
  thread2 = threading.Thread(target=print_letters)

  # Starting threads
  thread1.start()
  thread2.start()

  # Joining threads
  thread1.join()
  thread2.join()
  stop = timer()
  print(f'done in {timedelta(seconds=stop-start)} seconds.')
  # Python v 3.13 or 3.14 will fix this


def print_numbers():
  for i in range(1, 6):
    time.sleep(1)
    print(i)


def print_letters():
  for c in 'abcdef':
    time.sleep(1)
    print(c)


###########################################


def example2():
  print('Is it faster? CPU Bound')
  print('single threaded:')
  start = timer()
  long_calculation()
  long_calculation()
  stop = timer()
  print(f'done in {timedelta(seconds=stop-start)} seconds.')

  print('multi-threaded:')
  start = timer()
  # Creating threads
  thread1 = threading.Thread(target=long_calculation())
  thread2 = threading.Thread(target=long_calculation())

  # Starting threads
  thread1.start()
  thread2.start()

  # Joining threads
  thread1.join()
  thread2.join()
  stop = timer()
  print(f'done in {timedelta(seconds=stop-start)} seconds.')


def long_calculation():
  for _ in range(6):
    sum = 0
    for i in range(100000):
      sum = sum + math.sqrt(i**2)
    print(sum)


###############################################


class BankAccount:

  def __init__(self):
    self.balance = 100  # initial balance
    self.lock = threading.Lock()

  def update(self, transaction, amount):
    with self.lock:  # short-hand for acquire() and release()
      print(f'{transaction}ing {amount}')
      self.balance += amount if transaction == 'deposit' else -amount
      print(f'New balance: {self.balance}')


account = BankAccount()


def banking_thread(transaction, amount):
  for _ in range(3):
    account.update(transaction, amount)
    time.sleep(1)


def example3():
  # Creating threads for different transactions
  thread1 = threading.Thread(target=banking_thread, args=('deposit', 50))
  thread2 = threading.Thread(target=banking_thread, args=('withdraw', 50))

  # Starting threads
  thread1.start()
  thread2.start()

  # Joining threads
  thread1.join()
  thread2.join()


###########################################

# Creating a queue instance with a maximum size to enforce backpressure
data_queue = queue.Queue(maxsize=10)


# Function for producers to produce data
def producer(name):
  for _ in range(5):
    item = random.randint(1, 100)
    data_queue.put(item)  # This will block if the queue is full
    print(f'Producer {name} produced {item}')
    time.sleep(random.random())


# Function for consumers to consume data
def consumer(name):
  while True:
    try:
      # Set timeout for get() to allow graceful exit after producers finish
      item = data_queue.get(timeout=3)
      print(f'Consumer {name} consumed {item}')
      data_queue.task_done()  # Signal that the item has been processed
    except queue.Empty:
      print(f'Consumer {name} exiting...')
      break


def example4():
  # Creating producer threads
  producer_threads = [
    threading.Thread(target=producer, args=(f'P{i}', )) for i in range(3)
  ]
  # same as: threading.Thread(target=producer, args=('P0',))
  #          threading.Thread(target=producer, args=('P1',))
  #          etc

  # Creating consumer threads
  consumer_threads = [
    threading.Thread(target=consumer, args=(f'C{i}', )) for i in range(2)
  ]

  # Starting producer and consumer threads
  for thread in producer_threads + consumer_threads:
    thread.start()

  # Waiting for all producer threads to finish
  for thread in producer_threads:
    thread.join()

  # Wait for the queue to be fully processed before allowing consumers to  exit
  data_queue.join()

  # Since the producers are done and the queue is empty, we can stop the consumers
  for thread in consumer_threads:
    thread.join()


######################################

if __name__ == '__main__':
  globals()[sys.argv[1]]()

