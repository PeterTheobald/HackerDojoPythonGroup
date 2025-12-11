import time
import benchmark
from collections import deque

# find all words matching the beginning of s, put them in a work queue
# then for each match in the work queue, find all words matching the rest of s, etc.
def find_words_naive(s, word_set):
    n = len(s)
    results = []
    # stack is a work queue of partially matched words
    stack = [(0, [])]  # (current index, current path)
    while stack:
        idx, path = stack.pop()
        if idx == n:
            results.append(' '.join(path))
            continue
        for i in range(idx+1, n+1):
            word = s[idx:i]
            if word in word_set:
                stack.append((i, path + [word]))
    return results

# Recursive version of the above
def find_words_naive_recursive(s, word_set):
    def helper(sub):
        if not sub:
            return [[]]
        results = []
        for i in range(1, len(sub)+1):
            word = sub[:i]
            if word in word_set:
                for rest in helper(sub[i:]):
                    results.append([word] + rest)
        return results
    return [ ' '.join(words) for words in helper(s) ]


def find_words_dp(s, word_set):
    n = len(s)
    # use Dynamic Programming (ie: remember previous results)
    # to remember previous words up to s[:i]
    # dp[i] = list of lists of words that can form s[:i]
    dp = [[] for _ in range(n+1)]
    dp[0] = [[]]  # base: empty string
    for i in range(1, n+1):
        for j in range(i):
            word = s[j:i]
            if word in word_set:
                for prev in dp[j]:
                    dp[i].append(prev + [word])
    return [ ' '.join(words) for words in dp[n] ]

def wordBreakSam(s, word_set):
    """Return all possible word break combinations."""
    memo = {}
    def backtrack(start):
        if start == len(s):
            return [""]
        if start in memo:
            return memo[start]
        result = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                rest_combinations = backtrack(end)
                for combination in rest_combinations:
                    if combination:
                        result.append(word + " " + combination)
                    else:
                        result.append(word)
        memo[start] = result
        return result
    return backtrack(0)


def find_words_dp_prefix(s, word_set):
    """DP approach: build from prefixes, storing all segmentations."""
    n = len(s)
    # dp[i] contains all possible segmentations of s[:i]
    dp = [[] for _ in range(n + 1)]
    dp[0] = [[]]  # empty prefix has one segmentation: empty list
    
    for i in range(1, n + 1):
        # Try all possible last words ending at position i
        for j in range(i):
            word = s[j:i]
            if word in word_set and dp[j]:  # if prefix s[:j] can be segmented
                for segmentation in dp[j]:
                    dp[i].append(segmentation + [word])
    
    return [' '.join(seg) for seg in dp[n]]


def find_words_dfs_memo(s, word_set):
    """DFS with memoization: explore all paths, cache results by index."""
    memo = {}
    
    def dfs(start_idx):
        if start_idx == len(s):
            return [[]]  # reached end, return one valid empty segmentation
        
        if start_idx in memo:
            return memo[start_idx]
        
        segmentations = []
        # Try all possible words starting at start_idx
        for end_idx in range(start_idx + 1, len(s) + 1):
            word = s[start_idx:end_idx]
            if word in word_set:
                # Recursively get all segmentations for the rest
                rest_segmentations = dfs(end_idx)
                for rest_seg in rest_segmentations:
                    segmentations.append([word] + rest_seg)
        
        memo[start_idx] = segmentations
        return segmentations
    
    return [' '.join(seg) for seg in dfs(0)]


def find_words_bfs_indices(s, word_set):
    """BFS approach: treat indices as nodes, find all paths from 0 to len(s)."""
    n = len(s)
    # Store all paths that reach each index
    paths_to_index = {0: [[]]}  # index 0 is reachable with empty path
    queue = deque([0])
    visited_order = [0]  # track order we visit indices
    
    while queue:
        idx = queue.popleft()
        if idx not in paths_to_index:
            continue
            
        # Try all possible words starting from this index
        for next_idx in range(idx + 1, n + 1):
            word = s[idx:next_idx]
            if word in word_set:
                # Extend all paths that reached idx with this word
                if next_idx not in paths_to_index:
                    paths_to_index[next_idx] = []
                    queue.append(next_idx)
                    visited_order.append(next_idx)
                
                for path in paths_to_index[idx]:
                    paths_to_index[next_idx].append(path + [word])
    
    if n in paths_to_index:
        return [' '.join(path) for path in paths_to_index[n]]
    return []


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

def build_trie(word_set):
    """Build a trie from the word set."""
    root = TrieNode()
    for word in word_set:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
    return root


def find_words_trie(s, trie_root):
    """Use trie for efficient word lookup during segmentation."""
    n = len(s)
    memo = {}
    
    def dfs(start_idx):
        if start_idx == n:
            return [[]]
        
        if start_idx in memo:
            return memo[start_idx]
        
        segmentations = []
        node = trie_root
        
        # Walk the trie while matching characters in s
        for end_idx in range(start_idx, n):
            char = s[end_idx]
            if char not in node.children:
                break  # no words with this prefix
            node = node.children[char]
            
            if node.is_word:
                word = s[start_idx:end_idx + 1]
                rest_segmentations = dfs(end_idx + 1)
                for rest_seg in rest_segmentations:
                    segmentations.append([word] + rest_seg)
        
        memo[start_idx] = segmentations
        return segmentations
    
    return [' '.join(seg) for seg in dfs(0)]


def find_words_length_pruned(s, word_data):
    """DFS with memoization + length-based pruning.
    Only check substrings of lengths that exist in the dictionary."""
    word_set, valid_lengths = word_data
    n = len(s)
    memo = {}
    
    def dfs(start_idx):
        if start_idx == n:
            return [[]]
        
        if start_idx in memo:
            return memo[start_idx]
        
        segmentations = []
        # Only check substring lengths that exist in dictionary
        for length in valid_lengths:
            end_idx = start_idx + length
            if end_idx > n:
                continue
            word = s[start_idx:end_idx]
            if word in word_set:
                rest_segmentations = dfs(end_idx)
                for rest_seg in rest_segmentations:
                    segmentations.append([word] + rest_seg)
        
        memo[start_idx] = segmentations
        return segmentations
    
    return [' '.join(seg) for seg in dfs(0)]


def prepare_word_data_with_lengths(word_list):
    """Prepare word set and extract valid word lengths."""
    word_set = set(word_list)
    valid_lengths = sorted(set(len(w) for w in word_set))
    return (word_set, valid_lengths)


def read_dict():
    words = []
    with open("ubuntu-wordlist.txt") as f:
        for line in f:
            word = line.strip()
            if word:
                words.append(word)
    return words

def main():
    NUM_RUNS = 1000000
    s = "nowhere"
    word_list = read_dict()
    
    algorithms = [
        {
            "title": "Naive Recursive Word Break",
            "method_fn": lambda ws: find_words_naive(s, ws),
            "setup_fn": lambda: set(word_list)
        },
        {
            "title": "Naive Iterative Word Break",
            "method_fn": lambda ws: find_words_naive_recursive(s, ws),
            "setup_fn": lambda: set(word_list)
        },
        {
            "title": "DP Word Break",
            "method_fn": lambda ws: find_words_dp(s, ws),
            "setup_fn": lambda: set(word_list)
        },
        {
            "title": "Sam's Memoized Word Break",
            "method_fn": lambda ws: wordBreakSam(s, ws),
            "setup_fn": lambda: set(word_list)
        },
        {
            "title": "DP on Prefixes",
            "method_fn": lambda ws: find_words_dp_prefix(s, ws),
            "setup_fn": lambda: set(word_list)
        },
        {
            "title": "DFS + Memoization",
            "method_fn": lambda ws: find_words_dfs_memo(s, ws),
            "setup_fn": lambda: set(word_list)
        },
        {
            "title": "BFS on Indices",
            "method_fn": lambda ws: find_words_bfs_indices(s, ws),
            "setup_fn": lambda: set(word_list)
        },
        {
            "title": "Trie-based Optimization",
            "method_fn": lambda trie: find_words_trie(s, trie),
            "setup_fn": lambda: build_trie(set(word_list))
        },
        {
            "title": "ChatGPTs best: Length-Pruned DFS+Memo",
            "method_fn": lambda data: find_words_length_pruned(s, data),
            "setup_fn": lambda: prepare_word_data_with_lengths(word_list)
        },
    ]
    results = benchmark.run(algorithms, REPEAT=NUM_RUNS)
    print("\nResults for each algorithm:")
    for res in results:
        print(f"{res['title']}: {res['last_result']}")

if __name__ == "__main__":
    main()
