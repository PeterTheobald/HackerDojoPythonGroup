#import asyncio
#import threading
import os
import subprocess
#import multiprocessing

# r=os.system(cmd)
data = """Zebra
Banana
Apple
Automobile
"""
try:
  r = subprocess.run(['sort'],
                     capture_output=True,
                     text=True,
                     input=data,
                     timeout=1)
  print(r.stdout)
except subprocess.TimeoutExpired as e:
  print('I timed out!')

with subprocess.Popen(['adventure'],
                      text=True,
                      stdin=subprocess.PIPE,
                      stdout=subprocess.PIPE) as p:
  while p.poll() is None:
    print(p.stdout.read())
    p.stdin.write(input())

