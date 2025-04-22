import time
import random

print("Building large list...")
start_time = time.time()

# Generate a large list of random integers
data_size = 10_000_000
data = [random.randint(0, data_size) for _ in range(data_size)]
search_value = data[data_size // 2]

end_time = time.time()
list_build_time = end_time - start_time
print(f"List build time: {list_build_time:.6f} seconds")

print("Searching list...")
# List Search
start_time = time.time()
search_result = search_value in data
end_time = time.time()
list_search_time = end_time - start_time
print(f"List search time: {list_search_time:.6f} seconds O(n)")

# Binary Tree Implementation
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert_into_bst(root, value):
    if root is None:
        return TreeNode(value)
    if value < root.value:
        root.left = insert_into_bst(root.left, value)
    else:
        root.right = insert_into_bst(root.right, value)
    return root

def search_bst(root, value):
    if root is None or root.value == value:
        return root is not None
    if value < root.value:
        return search_bst(root.left, value)
    return search_bst(root.right, value)

print("Building binary tree...")
start_time = time.time()

# Build the binary search tree
bst_root = None
for val in data:
    bst_root = insert_into_bst(bst_root, val)

end_time = time.time()
tree_build_time = end_time - start_time
print(f"Binary Tree build time: {tree_build_time:.6f} seconds")

print("Searching binary tree...")
# Binary Tree Search
start_time = time.time()
search_result = search_bst(bst_root, search_value)
end_time = time.time()
bst_search_time = end_time - start_time
print(f"Binary tree search time: {bst_search_time:.6f} seconds O(log n)")

print("Building dictionary...")
start_time = time.time()

# Dictionary Search
data_dict = {val: True for val in data}

end_time = time.time()
dict_build_time = end_time - start_time
print(f"Dict build time: {dict_build_time:.6f} seconds")

print("Searching dictionary...")
start_time = time.time()
search_result = search_value in data_dict
end_time = time.time()
dict_search_time = end_time - start_time
print(f"Dictionary search time: {dict_search_time:.6f} seconds O(1)")


