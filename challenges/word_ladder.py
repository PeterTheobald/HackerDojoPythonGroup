import heapq
import time
from collections import defaultdict, deque

### Breadth-First-Search
### trying every letter a-z in each position

def find_word_path_a_z(start_word, target_word, word_set):
    if target_word not in word_set:
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
                next_word = word[:i] + c + word[i+1:]
                if next_word in word_set and next_word not in visited:
                    visited.add(next_word)
                    queue.append(path + [next_word])
    return []

def find_word_path_a_z2(start, target, word_set):
    if target not in word_set:
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
                nxt = w[:i] + c + w[i+1:]
                if nxt in word_set and nxt not in visited:
                    visited.add(nxt)
                    prev[nxt] = w
                    q.append(nxt)
    return []

### Breadth-First-Search
### preprocessing word list into a graph

def build_neighbors(word_list):
    words = list(set(word_list)) # dedup
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

def find_word_path_graph(start_word, target_word, word_graph):

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

### Preprocess into graph, using JH's wildcard "*" marker idea
###
def build_buckets(words):
    buckets = defaultdict(list)
    for w in words:
        L = len(w)
        for i in range(L):
            pattern = w[:i] + "*" + w[i+1:]
            buckets[pattern].append(w)
    return buckets

def find_word_path_wildcard(start_word, target_word, buckets):
    queue = deque([start_word])
    visited = {start_word}
    prev = {start_word: None}
    used_patterns = set()  # per-search, don't mutate buckets

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
            pattern = word[:i] + "*" + word[i+1:]
            if pattern in used_patterns:
                continue
            used_patterns.add(pattern)

            for nxt in buckets.get(pattern, ()):
                if nxt not in visited:
                    visited.add(nxt)
                    prev[nxt] = word
                    queue.append(nxt)
    return []

def find_word_path_wildcardxx(start_word, target_word, buckets):
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

        L = len(word)
        for i in range(L):
            pattern = word[:i] + "*" + word[i+1:]
            neighbors = buckets.get(pattern, [])
            for nxt in neighbors:
                if nxt not in visited:
                    visited.add(nxt)
                    prev[nxt] = word
                    queue.append(nxt)
            # clear bucket so we don't process it again
            buckets[pattern] = []
    return []

#### A* algorithm
####

def _heuristic(word, target):
    # number of differing letters (Hamming distance)
    return sum(1 for a, b in zip(word, target) if a != b)

def find_word_path_astar(start_word, target_word, word_set):
    if target_word not in word_set:
        return []

    open_heap = []
    g_score = {start_word: 0}
    came_from = {}

    heapq.heappush(open_heap, (_heuristic(start_word, target_word), 0, start_word))

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
                nxt = word[:i] + c + word[i+1:]
                if nxt not in word_set:
                    continue

                tentative_g = g + 1
                if tentative_g < g_score.get(nxt, float("inf")):
                    g_score[nxt] = tentative_g
                    came_from[nxt] = word
                    f_nxt = tentative_g + _heuristic(nxt, target_word)
                    heapq.heappush(open_heap, (f_nxt, tentative_g, nxt))

    return []


def read_dict():
    words = []
    with open("ubuntu-wordlist.txt") as f:
        for line in f:
            word = line.strip()
            if word:
                words.append(word)
    return words

def build_set( word_list):
    return set(word_list)

def main():
    NUM_RUNS = 100 
#    start="cold"
#    end="warm"
    start="small"
    end="large"

    word_list=read_dict()
    word_list.append(start)
    word_list.append(end)
    # do all pre-processing once for each trial
    # 
    t0 = time.perf_counter()
    word_set=set(word_list)
    for _ in range(NUM_RUNS):
        result1 = find_word_path_a_z( start, end, word_set)
    t1 = time.perf_counter()
    # time
    word_set=set(word_list)
    for _ in range(NUM_RUNS):
        result2 = find_word_path_a_z2( start, end, word_set)
    t2 = time.perf_counter()
    #
    word_graph=build_neighbors(word_list)
    t2b = time.perf_counter()
    for _ in range(NUM_RUNS):
        result3 = find_word_path_graph( start, end, word_graph)
    t3 = time.perf_counter()
    # time
    word_bucket=build_buckets(word_list)
    t3b = time.perf_counter()
    for _ in range(NUM_RUNS):
        result4 = find_word_path_wildcard( start, end, word_bucket)
    t4 = time.perf_counter()
    # time
    word_set=set(word_list)
    for _ in range(NUM_RUNS):
        result5 = find_word_path_astar( start, end, word_set)
    t5 = time.perf_counter()

    # compute N, G, L 
    N = len(word_list)
    L = len(start)
    # each edge counted twice in the adjacency lists
    G = sum(len(v) for v in word_graph.values()) // 2
    print(f"solution 1 A-Z   time: {(t1-t0):0.4f} seconds O(26·N·L)~O(N·L)")
    print(f"solution 2 A-Z2 time: {(t2-t1):0.4f} seconds O(26·N·L)~O(N·L)")
    print(f"solution 3 graph time: {(t3-t2):0.4f} seconds O(N^2·L) + O(N·G)~O(N^2)")
    print(f"                       ({(t2b-t2):0.4f}s for build_graph, {(t3-t2b):0.4f}s for search graph)")
    print(f"solution 4 wildcard  : {(t4-t3):0.4f} seconds O(N·L^2)")
    print(f"                       ({(t3b-t3):0.4f}s for build_buckets, {(t4-t3b):0.4f}s for search graph)")
    print(f"solution 5 A*    time: {(t5-t4):0.4f} seconds O(N·L·log N)")
    print(f"Complexity N (word_list)={N}, L (word len)={L}, G (graph edges)={G}")
    print(f"example result 1:", result1)
    print(f"example result 2:", result2)
    print(f"example result 3:", result3)
    print(f"example result 4:", result4)
    print(f"example result 5:", result5)
    print()
    print("Note A* has worse worst-case O(NLlogN), but if it has a good heuristic")
    print("it searches words that 'look closer' first, searching less of the graph")
    print("In this case there is no good heuristic")

main()

