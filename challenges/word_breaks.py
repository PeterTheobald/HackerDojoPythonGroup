import time
import benchmark
from collections import deque

def find_words_naive(s, word_list):
    word_set = set(word_list)
    n = len(s)
    results = []
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

def find_words_naive_recursive(s, word_list):
    word_set = set(word_list)
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


def find_words_dp(s, word_list):
    word_set = set(word_list)
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

def wordBreakSam(s, word_list):
    """Return all possible word break combinations."""
    word_set = set(word_list)
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


def read_dict():
    words = []
    with open("ubuntu-wordlist.txt") as f:
        for line in f:
            word = line.strip()
            if word:
                words.append(word)
    return words

def main():
    NUM_RUNS = 10
    s = "nowhere"
    word_list = read_dict()
    algorithms = [
        {
            "title": "Naive Recursive Word Break",
            "method_fn": lambda wl: find_words_naive(s, wl),
            "setup_fn": lambda: word_list
        },
        {
            "title": "Naive Iterative Word Break",
            "method_fn": lambda wl: find_words_naive_recursive(s, wl),
            "setup_fn": lambda: word_list
        },
        {
            "title": "DP Word Break",
            "method_fn": lambda wl: find_words_dp(s, wl),
            "setup_fn": lambda: word_list
        },
        {
            "title": "Sam's Memoized Word Break",
            "method_fn": lambda wl: wordBreakSam(s, wl),
            "setup_fn": lambda: word_list
        },
    ]
    results = benchmark.run(algorithms, REPEAT=NUM_RUNS)
    print("\nExample results for each algorithm:")
    for res in results:
        print(f"{res['title']}: {res['last_result']}")

if __name__ == "__main__":
    main()
