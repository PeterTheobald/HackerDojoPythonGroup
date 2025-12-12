import heapq
import time
from collections import defaultdict, deque
from typing import DefaultDict, Dict, List, Optional, Set

import benchmark

# LeetCode style challenge (from #127 https://leetcode.com/problems/word-ladder/)
# Given two words (beginWord and endWord), and a dictionary's word list,
# find the length of shortest transformation sequence from beginWord to endWord,
# such that:
# 1. Only one letter can be changed at a time.
# 2. Each transformed word must exist in the word list.
# Note that beginWord is not a transformed word.
# For example,
# Given:
# beginWord = "hit",
# endWord = "cog",
# wordList = ["hot","dot","dog","lot","log","cog"]
# As one shortest transformation is "hit" -> "hot" -> "dot" -> "dog" -> "cog",


# Simple Breadth-First-Search
### trying every letter a-z in each position
def find_word_path_a_z(start_word: str, target_word: str, words: Set[str]) -> List[str]:
    if target_word not in words:
        return []
    queue = deque([[start_word]])
    visited = {start_word}
    while queue:
        path = queue.popleft()
        word = path[-1]
        if word == target_word:
            return path
        for i in range(len(word)):
            for c in "abcdefghijklmnopqrstuvwxyz":
                if c == word[i]:
                    continue
                next_word = word[:i] + c + word[i + 1 :]
                if next_word in words and next_word not in visited:
                    visited.add(next_word)
                    queue.append(path + [next_word])
    return []


# slight variation using prev dict to reconstruct path
def find_word_path_a_z2(start: str, target: str, words: Set[str]) -> List[str]:
    if target not in words:
        return []
    q = deque([start])
    visited = {start}
    prev = {start: None}
    while q:
        w = q.popleft()
        if w == target:
            path = []
            while w is not None:
                path.append(w)
                w = prev[w]
            return path[::-1]
        for i in range(len(w)):
            for c in "abcdefghijklmnopqrstuvwxyz":
                if c == w[i]:
                    continue
                nxt = w[:i] + c + w[i + 1 :]
                if nxt in words and nxt not in visited:
                    visited.add(nxt)
                    prev[nxt] = w
                    q.append(nxt)
    return []


# Build full graph of words differing by one letter
# for use by find_word_path_graph
def build_full_graph(word_list: List[str]) -> Dict[str, List[str]]:
    words = list(set(word_list))
    neighbors = {w: [] for w in words}
    n = len(words)
    for i in range(n):
        for j in range(i + 1, n):
            w1, w2 = words[i], words[j]
            if len(w1) != len(w2):
                continue
            diff = 0
            for a, b in zip(w1, w2):
                if a != b:
                    diff += 1
                    if diff > 1:
                        break
            if diff == 1:
                neighbors[w1].append(w2)
                neighbors[w2].append(w1)
    return neighbors


# BFS on prebuilt graph
# the idea: finding neighbors is O(1) instead of O(26·L) trying every letter
def find_word_path_graph(
    start_word: str, target_word: str, word_graph: Dict[str, List[str]]
) -> List[str]:
    neighbors = word_graph
    if start_word not in neighbors or target_word not in neighbors:
        return []
    queue = deque([start_word])
    visited = {start_word}
    prev = {start_word: None}
    while queue:
        word = queue.popleft()
        if word == target_word:
            path = []
            while word is not None:
                path.append(word)
                word = prev[word]
            return path[::-1]
        for nxt in neighbors[word]:
            if nxt not in visited:
                visited.add(nxt)
                prev[nxt] = word
                queue.append(nxt)
    return []


# Build wildcard graph for use by find_word_path_wildcard
def build_wildcard_graph(words: List[str]) -> DefaultDict[str, List[str]]:
    buckets: DefaultDict[str, List[str]] = defaultdict(list)
    for w in words:
        L = len(w)
        for i in range(L):
            pattern = w[:i] + "*" + w[i + 1 :]
            buckets[pattern].append(w)
    return buckets


# BFS on wildcard graph
# the idea: finding neighbors is O(L) instead of O(26·L) trying every letter
# But the full graph in find_word_path_graph took a very long time to build,
# so this is a compromise: building buckets is O(N·L^2) instead of O(N^2·L)
# Using wildcard patterns as "neighbor gathering nodes" to find neighbors on the fly
# Eg: all the words "hot", "hit", "hat", "hut" connect via "h*t"
def find_word_path_wildcard(
    start_word: str, target_word: str, buckets: DefaultDict[str, List[str]]
) -> List[str]:
    queue = deque([start_word])
    visited = {start_word}
    prev = {start_word: None}
    used_patterns = set()
    while queue:
        word = queue.popleft()
        if word == target_word:
            path = []
            while word is not None:
                path.append(word)
                word = prev[word]
            return path[::-1]
        L = len(word)
        for i in range(L):
            pattern = word[:i] + "*" + word[i + 1 :]
            if pattern in used_patterns:
                continue
            used_patterns.add(pattern)
            for nxt in buckets.get(pattern, ()):
                if nxt not in visited:
                    visited.add(nxt)
                    prev[nxt] = word
                    queue.append(nxt)
    return []


# A* Search with Hamming distance heuristic
def _heuristic_hamming(word: str, target: str) -> int:
    return sum(1 for a, b in zip(word, target) if a != b)


# A* Search implementation
# Similar to BFS but instead of blindly exploring neighbors,
# we use a priority queue to explore the most promising nodes first
def find_word_path_astar(
    start_word: str, target_word: str, words: Set[str]
) -> List[str]:
    if target_word not in words:
        return []
    open_heap = []
    g_score = {start_word: 0}
    came_from = {}
    heapq.heappush(
        open_heap, (_heuristic_hamming(start_word, target_word), 0, start_word)
    )
    visited = set()
    letters = "abcdefghijklmnopqrstuvwxyz"
    while open_heap:
        f, g, word = heapq.heappop(open_heap)
        if word in visited:
            continue
        visited.add(word)
        if word == target_word:
            path = [word]
            while word in came_from:
                word = came_from[word]
                path.append(word)
            return path[::-1]
        for i in range(len(word)):
            for c in letters:
                if c == word[i]:
                    continue
                nxt = word[:i] + c + word[i + 1 :]
                if nxt not in words:
                    continue
                tentative_g = g + 1
                if tentative_g < g_score.get(nxt, float("inf")):
                    g_score[nxt] = tentative_g
                    came_from[nxt] = word
                    f_nxt = tentative_g + _heuristic_hamming(nxt, target_word)
                    heapq.heappush(open_heap, (f_nxt, tentative_g, nxt))
    return []


# A* Search with letter frequency heuristic
# Maybe searching most "common" words first helps?
def _heuristic_frequencies(word: str) -> float:
    # English letter frequency (ETAOIN SHRDLU...)
    # Source: https://en.wikipedia.org/wiki/Letter_frequency
    freq = {
        "e": 12.70,
        "t": 9.06,
        "a": 8.17,
        "o": 7.51,
        "i": 6.97,
        "n": 6.75,
        "s": 6.33,
        "h": 6.09,
        "r": 5.99,
        "d": 4.25,
        "l": 4.03,
        "c": 2.78,
        "u": 2.76,
        "m": 2.41,
        "w": 2.36,
        "f": 2.23,
        "g": 2.02,
        "y": 1.97,
        "p": 1.93,
        "b": 1.49,
        "v": 0.98,
        "k": 0.77,
        "j": 0.15,
        "x": 0.15,
        "q": 0.10,
        "z": 0.07,
    }
    # Heuristic: sum of letter frequencies in the word
    return sum(freq.get(c, 0) for c in word)


# A* Search implementation with frequency heuristic
def find_word_path_astar2(
    start_word: str, target_word: str, words: Set[str]
) -> List[str]:
    if target_word not in words:
        return []
    open_heap = []
    g_score = {start_word: 0}
    came_from = {}
    heapq.heappush(open_heap, (_heuristic_frequencies(start_word), 0, start_word))
    visited = set()
    letters = "abcdefghijklmnopqrstuvwxyz"
    while open_heap:
        f, g, word = heapq.heappop(open_heap)
        if word in visited:
            continue
        visited.add(word)
        if word == target_word:
            path = [word]
            while word in came_from:
                word = came_from[word]
                path.append(word)
            return path[::-1]
        for i in range(len(word)):
            for c in letters:
                if c == word[i]:
                    continue
                nxt = word[:i] + c + word[i + 1 :]
                if nxt not in words:
                    continue
                tentative_g = g + 1
                if tentative_g < g_score.get(nxt, float("inf")):
                    g_score[nxt] = tentative_g
                    came_from[nxt] = word
                    f_nxt = tentative_g + _heuristic_frequencies(nxt)
                    heapq.heappush(open_heap, (f_nxt, tentative_g, nxt))
    return []


# A* Search on wildcard graph, combines both ideas
def find_word_path_astar_wildcard(
    start_word: str, target_word: str, buckets: DefaultDict[str, List[str]]
) -> List[str]:
    open_heap = []
    g_score = {start_word: 0}
    came_from = {}
    # Hamming distance heuristic
    import heapq

    heapq.heappush(
        open_heap, (sum(a != b for a, b in zip(start_word, target_word)), 0, start_word)
    )
    visited = set()
    while open_heap:
        f, g, word = heapq.heappop(open_heap)
        if word in visited:
            continue
        visited.add(word)
        if word == target_word:
            path = [word]
            while word in came_from:
                word = came_from[word]
                path.append(word)
            return path[::-1]
        L = len(word)
        for i in range(L):
            pattern = word[:i] + "*" + word[i + 1 :]
            for nxt in buckets.get(pattern, ()):  # wildcard neighbors
                if nxt not in visited:
                    tentative_g = g + 1
                    if tentative_g < g_score.get(nxt, float("inf")):
                        g_score[nxt] = tentative_g
                        came_from[nxt] = word
                        f_nxt = tentative_g + sum(
                            a != b for a, b in zip(nxt, target_word)
                        )
                        heapq.heappush(open_heap, (f_nxt, tentative_g, nxt))
    return []


# Utility functions and main benchmarking


def read_wordlist() -> List[str]:
    words = []
    with open("ubuntu-wordlist.txt") as f:
        for line in f:
            word = line.strip()
            if word:
                words.append(word)
    return words


def build_set(word_list: List[str]) -> Set[str]:
    return set(word_list)


def main() -> None:
    NUM_RUNS = 50
    start = "small"
    end = "large"
    word_list = read_wordlist()
    word_list.append(start)
    word_list.append(end)
    algorithms = [
        {
            "title": "A-Z BFS   O(26·N·L)~O(N·L)",
            "method_fn": lambda ws: find_word_path_a_z(start, end, ws),
            "setup_fn": lambda: set(word_list),
        },
        {
            "title": "A-Z2 BFS  O(26·N·L)~O(N·L)",
            "method_fn": lambda ws: find_word_path_a_z2(start, end, ws),
            "setup_fn": lambda: set(word_list),
        },
        {
            "title": "Full Graph BFS O(N^2·L) + O(N·G)~O(N^2)",
            "method_fn": lambda g: find_word_path_graph(start, end, g),
            "setup_fn": lambda: build_full_graph(word_list),
        },
        {
            "title": "Wildcard Graph BFS O(N·L^2)",
            "method_fn": lambda b: find_word_path_wildcard(start, end, b),
            "setup_fn": lambda: build_wildcard_graph(word_list),
        },
        {
            "title": "A* Search hamming O(N·L·logN)",
            "method_fn": lambda ws: find_word_path_astar(start, end, ws),
            "setup_fn": lambda: set(word_list),
        },
        {
            "title": "A*2 Search frequencies O(N·L·logN)",
            "method_fn": lambda ws: find_word_path_astar2(start, end, ws),
            "setup_fn": lambda: set(word_list),
        },
        {
            "title": "both: A* & Wildcard O(N·L·logN)",
            "method_fn": lambda b: find_word_path_astar_wildcard(start, end, b),
            "setup_fn": lambda: build_wildcard_graph(word_list),
        },
    ]
    results = benchmark.run(algorithms, REPEAT=NUM_RUNS)
    print("\nResults for each algorithm:")
    for res in results:
        print(f"{res['title']}: {res['last_result']}")


if __name__ == "__main__":
    main()
