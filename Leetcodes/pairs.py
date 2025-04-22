from typing import *
from collections import defaultdict


# https://leetcode.com/problems/restore-the-array-from-adjacent-pairs/description/
class Solution:

  def restoreArray(self, adjacentPairs: List[List[int]]) -> List[int]:

    # Turn pairs into a graph. node[from]=[ to, to, to...]

    nodes = defaultdict(list)
    for pair in adjacentPairs:
      nodes[pair[0]].append(pair[1])
      nodes[pair[1]].append(pair[0])

    # The graph is actually just a doubly-linked list
    # Find either end with only one connected node
    for node in nodes:
      if len(nodes[node]) == 1:
        break
    assert len(
      nodes[node]
    ) == 1, "Error there must be two end nodes with only one connection"

    # traverse the list
    result = [node]
    node = nodes[node][0]
    while len(nodes[node]) == 2:  # stop when we reach the other end
      if nodes[node][0] == result[-1]:  # [0] points to the previous node
        result.append(node)
        node = nodes[node][1]
      else:  # [0] points to the next node
        result.append(node)
        node = nodes[node][0]
    result.append(node)  # append the end
    return result


def main():
  S = Solution()
  #print(S.restoreArray([[0, 1], [1, 2], [2, 3], [3, 4]]))
  print(S.restoreArray([[0, 1]]))


if __name__ == '__main__':
  main()
