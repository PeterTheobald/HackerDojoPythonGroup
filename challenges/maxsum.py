from typing import List
import timeit
import time
from collections import defaultdict


class Solution1:

  def maxSum(self, nums: List[int]) -> int:
    # O(n^2)
    max_sum = -1
    for i in range(len(nums)):
      for j in range(i + 1, len(nums)):
        if nums[i] + nums[j] > max_sum and self.max_digit(
            nums[i]) == self.max_digit(nums[j]):
          max_sum = nums[i] + nums[j]
    return max_sum

  def max_digit(self, n):
    return max(list(str(n)))


class Solution2:

  def maxSum(self, nums: List[int]) -> int:
    # O(3nlog(n)) ~~ O(nlog(n))
    siblings = defaultdict(list)
    for n in nums:
      siblings[self.max_digit(n)].append(n)
    max_sum = -1
    for maxd in siblings:
      if len(siblings[maxd]) > 1:
        max1 = max(siblings[maxd])
        siblings[maxd].remove(max1)
        max2 = max(siblings[maxd])
        if max1 + max2 > max_sum:
          max_sum = max1 + max2
    return max_sum

  def max_digit(self, n):
    return max(list(str(n)))


class Solution3:

  def maxSum(self, nums: List[int]) -> int:
    # O(nlog(n))
    siblings = defaultdict(list)
    for n in nums:
      max_digit = max(list(str(n)))
      siblings[max_digit].append(n)
      if len(siblings[max_digit]) == 3:
        siblings[max_digit].sort(reverse=True)
        siblings[max_digit].pop()
    max_sum = -1
    for maxd in siblings:
      if len(siblings[maxd]) == 2:
        if siblings[maxd][0] + siblings[maxd][1] > max_sum:
          max_sum = siblings[maxd][0] + siblings[maxd][1]
    return max_sum


class Solution3tuple:

  def maxSum(self, nums: List[int]) -> int:
    # O(nlog(n))
    siblings = defaultdict(tuple)
    for n in nums:
      max_digit = max(list(str(n)))
      siblings[max_digit] = siblings[max_digit] + (n, )
      if len(siblings[max_digit]) == 3:
        siblings[max_digit] = tuple(
          sorted(siblings[max_digit], reverse=True)[:2])
    max_sum = -1
    for maxd in siblings:
      if len(siblings[maxd]) == 2:
        if siblings[maxd][0] + siblings[maxd][1] > max_sum:
          max_sum = siblings[maxd][0] + siblings[maxd][1]
    return max_sum


class Solution4:

  def maxSum(self, nums: List[int]) -> int:
    # O(nlog(n))
    siblings = defaultdict(lambda: (-1, -1))
    for n in nums:
      max_digit = max(list(str(n)))
      a = siblings[max_digit][0]
      b = siblings[max_digit][1]
      siblings[max_digit] = (((a, b) if b > n else (a, n)) if a > n else
                             (n, a)) if a > b else ((b, a) if a > n else
                                                    ((b, n) if b > n else
                                                     (n, b)))
    max_sum = -1
    for maxd in siblings:
      if len(siblings[maxd]) == 2:
        if siblings[maxd][0] + siblings[maxd][1] > max_sum:
          max_sum = siblings[maxd][0] + siblings[maxd][1]
    return max_sum


# this horrendous expression gets the max 2 items
#  siblings[max_digit]=(((a,b) if b>n else (a,n)) if a>n else (n,a)) if a>b else ((b,a) if a>n else ((b,n) if b>n else (n,b)))


def test1():
  s = Solution1()
  return s.maxSum([51, 71, 17, 24, 42])


def test2():
  s = Solution2()
  return s.maxSum([51, 71, 17, 24, 42])


def test3():
  s = Solution3()
  return s.maxSum([51, 71, 17, 24, 42])


def test3tuple():
  s = Solution3()
  return s.maxSum([51, 71, 17, 24, 42])


def test4():
  s = Solution4()
  return s.maxSum([51, 71, 17, 24, 42])


print(timeit.timeit(test1, number=99999))
print(timeit.timeit(test2, number=99999))
print(timeit.timeit(test3, number=99999))
print(timeit.timeit(test3tuple, number=99999))
print(timeit.timeit(test4, number=99999))
