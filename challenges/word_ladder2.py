import time
from collections import defaultdict, deque
import heapq
import benchmark

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

def build_full_graph(word_list):
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

def build_wildcard_graph(words):
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

def _heuristic_hamming(word, target):
    return sum(1 for a, b in zip(word, target) if a != b)

def find_word_path_astar(start_word, target_word, word_set):
    if target_word not in word_set:
        return []
    open_heap = []
    g_score = {start_word: 0}
    came_from = {}
    heapq.heappush(open_heap, (_heuristic_hamming(start_word, target_word), 0, start_word))
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
                    f_nxt = tentative_g + _heuristic_hamming(nxt, target_word)
                    heapq.heappush(open_heap, (f_nxt, tentative_g, nxt))
    return []

def _heuristic_frequencies(word):
    # English letter frequency (ETAOIN SHRDLU...)
    # Source: https://en.wikipedia.org/wiki/Letter_frequency
    freq = {
        'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75,
        's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78,
        'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97,
        'p': 1.93, 'b': 1.49, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15,
        'q': 0.10, 'z': 0.07
    }
    # Heuristic: sum of letter frequencies in the word
    return sum(freq.get(c, 0) for c in word)

def find_word_path_astar2(start_word, target_word, word_set):
    if target_word not in word_set:
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
                nxt = word[:i] + c + word[i+1:]
                if nxt not in word_set:
                    continue
                tentative_g = g + 1
                if tentative_g < g_score.get(nxt, float("inf")):
                    g_score[nxt] = tentative_g
                    came_from[nxt] = word
                    f_nxt = tentative_g + _heuristic_frequencies(nxt)
                    heapq.heappush(open_heap, (f_nxt, tentative_g, nxt))
    return []

def find_word_path_astar_wildcard(start_word, target_word, buckets):
    open_heap = []
    g_score = {start_word: 0}
    came_from = {}
    # Hamming distance heuristic
    import heapq
    heapq.heappush(open_heap, (sum(a != b for a, b in zip(start_word, target_word)), 0, start_word))
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
            pattern = word[:i] + "*" + word[i+1:]
            for nxt in buckets.get(pattern, ()):  # wildcard neighbors
                if nxt not in visited:
                    tentative_g = g + 1
                    if tentative_g < g_score.get(nxt, float("inf")):
                        g_score[nxt] = tentative_g
                        came_from[nxt] = word
                        f_nxt = tentative_g + sum(a != b for a, b in zip(nxt, target_word))
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

def build_set(word_list):
    return set(word_list)

def main():
    NUM_RUNS = 50
    start = "small"
    end = "large"
    word_list = read_dict()
    word_list.append(start)
    word_list.append(end)
    algorithms = [
        {
            "title": "A-Z BFS   O(26·N·L)~O(N·L)",
            "method_fn": lambda ws: find_word_path_a_z(start, end, ws),
            "setup_fn": lambda: set(word_list)
        },
        {
            "title": "A-Z2 BFS  O(26·N·L)~O(N·L)",
            "method_fn": lambda ws: find_word_path_a_z2(start, end, ws),
            "setup_fn": lambda: set(word_list)
        },
        {
            "title": "Full Graph BFS O(N^2·L) + O(N·G)~O(N^2)",
            "method_fn": lambda g: find_word_path_graph(start, end, g),
            "setup_fn": lambda: build_full_graph(word_list)
        },
        {
            "title": "Wildcard Graph BFS O(N·L^2)",
            "method_fn": lambda b: find_word_path_wildcard(start, end, b),
            "setup_fn": lambda: build_wildcard_graph(word_list)
        },
        {
            "title": "A* Search hamming O(N·L·logN)",
            "method_fn": lambda ws: find_word_path_astar(start, end, ws),
            "setup_fn": lambda: set(word_list)
        },
        {
            "title": "A*2 Search frequencies O(N·L·logN)",
            "method_fn": lambda ws: find_word_path_astar2(start, end, ws),
            "setup_fn": lambda: set(word_list)
        },
        {
            "title": "both: A* & Wildcard O(N·L·logN)",
            "method_fn": lambda b: find_word_path_astar_wildcard(start, end, b),
            "setup_fn": lambda: build_wildcard_graph(word_list)
        },
    ]
    results = benchmark.run(algorithms, REPEAT=NUM_RUNS)
    print("\nExample results for each algorithm:")
    for res in results:
        print(f"{res['title']}: {res['last_result']}")

if __name__ == "__main__":
    main()
