# https://leetcode.com/problems/max-pair-sum-in-an-array/description/


class Simple_Solution:
  # ok solution. correct but slow O(n^2)
  def maxSum(self, nums: List[int]) -> int:
    max_sum = -1
    for i in range(len(nums)):
      for j in range(i + 1, len(nums)):
        sum = nums[i] + nums[j]
        if sum > max_sum and self.max_digit(nums[i]) == self.max_digit(
            nums[j]):
          max_sum = sum
    return max_sum

  def max_digit(self, num: int) -> int:
    return max(list(str(num)))


if __name__ == '__main__':
  s = Simple_Solution()
  print(s.maxSum([51, 71, 17, 24, 42]))
  print(s.maxSum([1, 2, 3, 4]))



# for a job interview, do better
class Better_Solution:
    def maxSum(self, nums: List[int]) -> int:
        # do better... for each num, calc max_digit and store in list w its siblings
        siblings={}
        for num in nums:
            maxd=self.max_digit( num)
            if maxd in siblings:
                siblings[maxd].append(num)
            else:
                siblings[maxd] = [num]
        # find the biggest sum from the siblings
        max_sum = -1
        for sibling_list in siblings.values():
            if len(sibling_list)>1:
                top_two = sorted(sibling_list, reverse=True)
                if top_two[0]+top_two[1] > max_sum:
                    max_sum = top_two[0]+top_two[1]
        return max_sum

    def max_digit(self, num: int) -> str:
        return max(list(str(num)))

# clean it up a bit
from collections import defaultdict

class Better_Solution:
    def maxSum(self, nums: List[int]) -> int:
        # do better... for each num, calc max_digit and store in list w its siblings
        siblings=defaultdict(list)
        for num in nums:
            maxd=max(list(str(num)))) # max digit
            siblings[maxd].append(num)
        # find the biggest sum from the siblings
        max_sum = -1
        for sibling_list in siblings.values():
            if len(sibling_list)>1:
                top_two = sorted(sibling_list, reverse=True)
                if top_two[0]+top_two[1] > max_sum:
                    max_sum = top_two[0]+top_two[1]
        return max_sum
