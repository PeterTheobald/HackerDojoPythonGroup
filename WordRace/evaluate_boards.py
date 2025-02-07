import sys

COLS = 10
ROWS = 13


def load_dictionary(filename="dict.txt"):
    """
    Load a dictionary of valid words, one per line.
    Return two structures:
       1) A set of all valid words
       2) A set of all valid prefixes (for pruning)
    """
    words = set()
    prefixes = set()
    with open(filename, "r") as f:
        for line in f:
            w = line.strip().upper()  # convert to uppercase if needed
            if w:
                words.add(w)
                # Add all prefixes of w to prefix set
                for i in range(1, len(w) + 1):
                    prefixes.add(w[:i])
    return words, prefixes


def get_neighbors(r, c):
    """
    Return the 8 possible neighbors for cell (r,c) in a square grid:
      (r-1, c-1), (r-1, c), (r-1, c+1),
      (r,   c-1),           (r,   c+1),
      (r+1, c-1), (r+1, c), (r+1, c+1).
    Only yield valid positions within the grid.
    """
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            rr = r + dr
            cc = c + dc
            if 0 <= rr < ROWS and 0 <= cc < COLS:
                yield (rr, cc)


def evaluate_board(board, words_set, prefixes_set):
    """
    Calculate a "score" for the board, defined as:
      - For each cell, do a depth-first search of all possible paths.
      - For each path that forms a word of length >=4, add the length of that word to the total.
      - The standard Boggle-like approach:
         * We track visited cells in the path so we don't reuse a cell in the same word.
         * We prune whenever the partial word is not in prefixes_set.
      - Return the total score.
    """
    total_score = 0

    def dfs(r, c, visited, current_word):
        nonlocal total_score

        # If length >= 4 and it's a valid word, add its length
        if len(current_word) >= 4 and current_word in words_set:
            total_score += len(current_word)
            # We do NOT stop after finding a valid word, because longer expansions might yield
            # different longer words. So we keep going.

        # Explore neighbors
        for nr, nc in get_neighbors(r, c):
            if (nr, nc) not in visited:
                next_letter = board[nr][nc]
                next_word = current_word + next_letter
                # Prune if next_word isn't a prefix of any word
                if next_word in prefixes_set:
                    visited.add((nr, nc))
                    dfs(nr, nc, visited, next_word)
                    visited.remove((nr, nc))

    for r in range(ROWS):
        for c in range(COLS):
            start_letter = board[r][c]
            if not start_letter:
                continue
            # If even the first letter isn't a prefix, skip
            if start_letter not in prefixes_set:
                continue
            visited = set()
            visited.add((r, c))
            dfs(r, c, visited, start_letter)

    return total_score


def get_boards(filename):
    with open(filename) as f:
        # Gather non-blank, non-comment lines
        lines = [
            line.rstrip("\n").upper()
            for line in f
            if line.strip() and not line.startswith("#")
        ]
        # Group into boards of 13 lines each
        for i in range(0, len(lines), 13):
            board = [list(line) for line in lines[i : i + 13]]
            if len(board) < 13:
                break
            yield board


def print_board(b):
    for line in b:
        print("".join(line))


def main():
    if len(sys.argv) < 2:
        print("Usage: python evalate_boards.py board_file.txt")
        print(
            "Where board_file.txt has 10x13 grids of letters separated by a blank line"
        )
        sys.exit()

    words, prefixes = load_dictionary("dict.txt")

    total_score = 0
    num_scores = 0
    for b in get_boards(sys.argv[1]):
        print_board(b)
        score = evaluate_board(b, words, prefixes)
        total_score += score
        num_scores += 1
        print(f"Board Score={score}")
        print()
    print(f"Average board score {(total_score/num_scores):.0f}")


if __name__ == "__main__":
    main()
