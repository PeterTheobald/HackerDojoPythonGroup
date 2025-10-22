Last week's challenge:

Python Challenge: Waiting for a warmer day

def wait_warmer( temps: list[int]) -> list[int]:
    # temps is a list of daily temperatures
    # return a list result: list[int]
    # where each item result[i] is the number of days you'd have to wait for a warmer day
    # if there is no warmer day after temp[i], then result[i]=0


first solution:

```
def petes_wait_warmer(temps: list[int]) -> list[int]:
    n = len(temps)
    res = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if temps[j] > temps[i]:
                res[i] = j - i
                break
    return res
```

What is the time complexity? 
For each item (the length of the input list) we have to scan the list.
So thats O( n * n) or O(n^2). Quadratic. Slow.
In practice it will run a little faster than `n*n` times because
- It starts each inner loop at i, not at the beginning, to scan the following days
- If it finds a warmer day right away it breaks out of that loop
But the worst case is a descending list of colder days like [104,103,102,101,100,99,98.. etc]
So it has to scan the entire list and never finds a warmer day
We use the 'worst case' to determine the O( )

next solution:

```
from typing import List

def sams_wait_warmer(temps: List[int]) -> List[int]:
    # Comment 1: Initialize result array with zeros and stack to store indices waiting for warmer days
    result = [0] * len(temps)
    remember = []
    
    # Comment 2: Iterate through temperatures, pop indices from stack when warmer day is found
    for i in range(len(temps)):
        while remember and temps[i] > temps[remember[-1]]:
            prev_index = remember.pop()
            result[prev_index] = i - prev_index
        remember.append(i)
    
    return result
```

This improves on the algorithm by remembering days we haven't yet seen a warmer day,
and looping through the list JUST ONCE.

Each time through the loop we look at just ONE day.
If we see a day that is warmer than a previously remembered day we can "solve"
that previous day and all previous days that were cooler than this day.
Then we will remember this day for later when we find a warmer day.

The remembered list of previous days forms a "stack". We push days onto the stack,
and we pop them off in reverse order (latest first).
That way the stack will ALWAYS hold days in decreasing temperature order.
temp[remember[0]] > temp[remember[1]] > temp[remember[2]], etc.
When we find a warmer day we "pop" off all the days that were cooler.

Since we only loop through the list ONCE, this is O(n)
But we have traded space for time, since we now keep the remember list.


Note that the Order O(n^2) and O(n) is an indication of how the algorithm
performs with growing input sizes. But the exact run-time can vary depending
on what input is given. If we work on a list that is already in strictly
increasing temperature order or decreasing temperature order we will have
to do more or less work to find the next warmer day.

