Big-O notation for comparing algorithmic scalability

Speedups like multi-threading and compilers like PyPy are good,
but to get the really meaningful speedups you need to choose the
right algorithm (and data structures).

Big-O notation is a way to characterize how fast and efficient an
algorithm. It works by describing how fast or slow it is as the amount
of work increases, ie: as it handles more items how much does it slow down?

I gave out a challenge last week, and we'll look at everyone's solutions
to it to compare algorithms.

When a function runs on a small input, it can be hard to tell which algorithm
is faster, as small differences in implementation affect the outcome. 
But as we increase the size of the input, the slower algorithms get MUCH
slower and the faster algorithms remain relatively faster.

So we compare algorithms with hypothetically huge inputs,
using n=the number of inputs, or the length of an input list

We see that algorithms with similar speeds on very small inputs, small n's,
have extremely different speeds with large inputs, large n's.
We can measure how much the algorithm slows down as n increases and
extrapolate how much it would slow down as n approaches infinity.
With large enough n's, we don't care about the exact programming language
or minor implementation details. The algorithm's scaling takes over
and dominates the shape of the graph.

If we graph the results we find that all algorithms naturally fall into
a few categories.
- Some algorithms are "linear" and grow directly slower as n increases,
the graph is a straight line.
- Some algorithms grow exponentially slower as n increases,
the graph is a curve going up rapidly, these algorithms are an order of magnitude
slower which is where the 'O' in big-O notation comes from "Order of Magnitude" or
"Order of Approximation".
- Some algorithms grow slower, but increase in efficiency the larger n gets.

We can make a graph of some simple expressions: 1, log(n), n, n^2 to see some sample
graphs. Most of our algorithm's growths will have a graph that has the same shape
as one of these. That is the "Order" or "O( )" of an algorithm, the expression with n that
has the same shaped curve of growth in time.

From best to worst:
- constant O(1)
- logarithmic O(log n)
- linear O(n)
- log-linear O(n log n)
- quadratic O(n^2)
- exponential O(2^n)
- factorial O(n!)

Generally speaking, an algorithm that has O(log(n)) is very fast, an algorithm that
has O(n) is medium, and an algorithm that has O(n^2) is very slow.
As inputs grow very large an O(n^2) algorithm isn't practically usable.
It takes an unreasonable length of time to complete.

All we care about is how to time to complete grows as n grows (ie: the shape of the graph).
If we compare an algorithm that takes O(n) and O(2n) we just throw away the constant 2. 
They grow at the same rate, their graphs have the same shaped curve.
They are both O(n)

We don't have to measure algorithms to figure out what their Order (time complexity) is.
We can look at how much work the algorithm does to determine what Order it is.

```
def get_value(d: dict, key: int):
  return d[key]
```
This is constant: O(1) because it returns the answer immediately in 1 operation
no matter how big the input `d` is.

```
def binary_search(arr: list, target: int):
    left = 0
    right = length(arr) - 1
    while left <= right:
        mid = floor((left + right) / 2)
        if arr[mid] == target:
            return true
        else if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return false
```
This is logarithmic: O(log n) because it cuts the array in half each time through the loop,
doing log(n) work.

```
def process_each_item(l: list):
  for i in l:
    do_work(i)
```
This has to do one piece of work for every n. So it is linear: O(n).

```
def every_combo(l: list):
  for i in l:
    for j in l:
      do_work(i, j)
```
This has to do work for every combination of every item in the list, n * n, So it is Quadratic: O(n^2)


Now let's analyze some examples based on last week's challenge:

Challenge:
The challenge is: You have a large list of numbers. Two of them add up to a target number.
There will only be TWO that add up to the target. Find those two numbers.

def find_two_sum( nums: list[int], target: int) -> tuple[int, int]:
  # return the two numbers that add up to target



