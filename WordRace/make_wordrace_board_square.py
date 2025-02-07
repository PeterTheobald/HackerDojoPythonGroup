import copy
import math
import random
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import Color

# Grid size (ROWS x COLS)
ROWS = 13
COLS = 10

# Each square cell size (in inches)
SQUARE_SIZE = 0.8 * inch

# Page size in inches
PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 11 * inch

# Light colors for top/bottom row fills
LIGHT_BLUE = Color(0.9, 0.9, 1)
LIGHT_RED = Color(1, 0.8, 0.8)

def load_start_frequencies(filename="start-letter-freqs.txt"):
    """
    Load "start letter" frequencies from a file, e.g.:
       A 3.2
    We'll normalize them to sum to 1.0 for random selection.
    """
    freqs = []
    total = 0.0
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().upper().split()
            if len(parts) != 2:
                continue
            letter, val_str = parts
            val = float(val_str)
            freqs.append((letter, val))
            total += val
    # Normalize
    if total > 0:
        freqs = [(ltr, val / total) for (ltr, val) in freqs]
    return freqs

def load_bigrams(filename="bigram-freqs.txt"):
    """
    Load bigram frequencies from a file where each line has:
       X Y 0.12
    meaning that if a neighbor's letter is X, the bigram X->Y has frequency 0.12.
    We'll store this in a dict-of-dicts:
       bigram_freq[X][Y] = 0.12
    """
    bigram_freq = {}
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().upper().split()
            if len(parts) != 3:
                continue
            first, second, freq_str = parts
            freq = float(freq_str)
            if first not in bigram_freq:
                bigram_freq[first] = {}
            bigram_freq[first][second] = freq
    return bigram_freq

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
                for i in range(1, len(w)+1):
                    prefixes.add(w[:i])
    return words, prefixes

def pick_from_distribution(freq_pairs):
    """
    freq_pairs is a list of (letter, probability),
    with probabilities summing to around 1.0.
    """
    r = random.random()
    accum = 0.0
    for letter, p in freq_pairs:
        accum += p
        if r <= accum:
            return letter
    # Fallback on rounding errors
    return freq_pairs[-1][0]

def pick_start_letter(start_freq):
    """
    Pick a letter using the "start letter" frequencies (already normalized).
    """
    return pick_from_distribution(start_freq)

def pick_letter_bigrams(bigram_freq, neighbor_letters):
    """
    Given a set of neighbor letters, compute a weighted distribution of all
    possible letters based on the sum of bigram frequencies from each neighbor.
    """
    # Collect all possible candidate letters from neighbors
    candidate_letters = set()
    for n in neighbor_letters:
        if n in bigram_freq:
            candidate_letters.update(bigram_freq[n].keys())

    # If no candidates, fallback to all known "second letters" or 'A'
    if not candidate_letters:
        all_known_letters = set()
        for first in bigram_freq:
            all_known_letters.update(bigram_freq[first].keys())
        if not all_known_letters:
            return 'A'
        candidate_letters = all_known_letters

    # Compute weight for each candidate letter by summing bigram_freq[n][letter]
    weights = []
    total_weight = 0.0
    for letter in candidate_letters:
        w = 0.0
        for n in neighbor_letters:
            w += bigram_freq.get(n, {}).get(letter, 0.0)
        if w > 0:
            weights.append((letter, w))
            total_weight += w

    # If all weights are zero or we have no data, pick randomly from candidates
    if total_weight <= 0:
        return random.choice(sorted(candidate_letters))

    # Convert weights to probabilities
    dist = [(letter, w / total_weight) for (letter, w) in weights]
    return pick_from_distribution(dist)

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
        for (nr, nc) in get_neighbors(r, c):
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

def generate_initial_board(start_freq, bigram_freq):
    # Create empty board
    board = [["" for _ in range(COLS)] for _ in range(ROWS)]

    # Fill top and bottom rows with start frequencies
    for col in range(COLS):
        board[0][col] = pick_start_letter(start_freq)
    for col in range(COLS):
        board[ROWS - 1][col] = pick_start_letter(start_freq)

    # Fill middle rows in a specific order
    fill_order = [1, 11, 2, 10, 3, 9, 4, 8, 5, 7, 6]
    for r in fill_order:
        if 0 <= r < ROWS:
            for col in range(COLS):
                if board[r][col] == "":
                    neighbor_letters = []
                    for (nr, nc) in get_neighbors(r, col):
                        if board[nr][nc]:
                            neighbor_letters.append(board[nr][nc])
                    chosen_letter = pick_letter_bigrams(bigram_freq, neighbor_letters)
                    board[r][col] = chosen_letter
    return board
    
def simulated_annealing(
    board, 
    bigram_freq, 
    dict_words, 
    dict_prefixes, 
    start_temp=5.0, 
    end_temp=0.1, 
    steps=100
):
    current_board = copy.deepcopy(board)
    best_board = copy.deepcopy(board)

    current_score = evaluate_board(current_board, dict_words, dict_prefixes)
    best_score = current_score

    for i in range(steps):
        # Simple linear cooling schedule
        frac = i / float(steps)
        T = start_temp + (end_temp - start_temp) * frac

        # Make a copy to modify
        new_board = copy.deepcopy(current_board)

        # Decide how many cells to randomly reselect (depends on T)
        # For example, reselect up to ~ T * 5 cells
        n_changes = int(round(T * 5))  
        for _ in range(n_changes):
            # pick a random row/col (but skip top/bottom row to keep them stable or not)
            rr = random.randint(0, ROWS - 1)
            cc = random.randint(0, COLS - 1)
            # re-generate letter using bigrams from neighbors
            neighbor_letters = []
            for (nr, nc) in get_neighbors(rr, cc):
                neighbor_letters.append(new_board[nr][nc])
            new_letter = pick_letter_bigrams(bigram_freq, neighbor_letters)
            new_board[rr][cc] = new_letter

        # Evaluate new board
        new_score = evaluate_board(new_board, dict_words, dict_prefixes)

        # Decide acceptance
        delta = new_score - current_score
        if delta > 0:
            # Better board, accept
            current_board = new_board
            current_score = new_score
        else:
            # Accept with probability e^(delta / T)
            prob = math.exp(delta / T) if T > 0 else 0
            if random.random() < prob:
                current_board = new_board
                current_score = new_score

        # Track best
        if current_score > best_score:
            best_score = current_score
            best_board = copy.deepcopy(current_board)

    return best_board, best_score

def print_board(b):
    for line in b:
        print( ''.join(line))
        
def draw_board(c, board):
    # Draw squares
    total_width = COLS * SQUARE_SIZE
    total_height = ROWS * SQUARE_SIZE
    x0 = (PAGE_WIDTH - total_width) / 2 # + SQUARE_SIZE/2
    y0 = (PAGE_HEIGHT - total_height) / 2 # + SQUARE_SIZE/2

    for r in range(ROWS):
        for col in range(COLS):
            letter = board[r][col]
            # Compute top-left corner of this square
            x_offset = x0 + col * SQUARE_SIZE
            # We draw row 0 at the top, so invert row index for the Y position
            y_offset = y0 + (ROWS - 1 - r) * SQUARE_SIZE

            # Color the top row red, bottom row blue
            fill_color = None
            if r == 0:
                fill_color = LIGHT_RED
            elif r == ROWS - 1:
                fill_color = LIGHT_BLUE

            # Draw the square
            c.setStrokeColorRGB(0, 0, 0)
            if fill_color:
                c.setFillColor(fill_color)
            else:
                c.setFillColorRGB(1, 1, 1)
            c.rect(x_offset, y_offset, SQUARE_SIZE, SQUARE_SIZE, fill=1, stroke=1)

            # Place the letter in the center
            if letter:
                c.setFillColorRGB(0, 0, 0)
                c.setFont("Helvetica", 10)
                text_x = x_offset + SQUARE_SIZE / 2
                text_y = y_offset + SQUARE_SIZE / 2 - 3
                if letter=='Q':
                    c.drawCentredString(text_x, text_y, 'Qu')
                else:
                    c.drawCentredString(text_x, text_y, letter)


def main():
    # Load data
    start_freq = load_start_frequencies("start-letter-freqs.txt")
    bigram_freq = load_bigrams("bigram-freqs.txt")
    dict_words, dict_prefixes = load_dictionary("dict.txt")

    """
    # We'll store letters in a 2D list
    grid = [["" for _ in range(COLS)] for _ in range(ROWS)]

    # Assign the top row (row 0) from start frequencies
    for col in range(COLS):
        grid[0][col] = pick_start_letter(start_freq)

    # Assign the bottom row (row 12) from start frequencies
    for col in range(COLS):
        grid[ROWS - 1][col] = pick_start_letter(start_freq)

    # Fill the remaining rows in the order: 1, 11, 2, 10, 3, 9, 4, 8, 5, 7, 6.
    fill_order = [1, 11, 2, 10, 3, 9, 4, 8, 5, 7, 6]

    for r in fill_order:
        if r < 0 or r >= ROWS:
            continue
        for col in range(COLS):
            if grid[r][col] == "":
                # Gather neighbor letters
                neighbor_letters = []
                for nr, nc in get_neighbors(r, col):
                    if grid[nr][nc] != "":
                        neighbor_letters.append(grid[nr][nc])
                chosen = pick_letter_bigrams(bigram_freq, neighbor_letters)
                grid[r][col] = chosen
    """

    # Generate initial board
    board = generate_initial_board(start_freq, bigram_freq)
    initial_score = evaluate_board(board, dict_words, dict_prefixes)
    print(f"Initial Score: {initial_score}")

    # Run simulated annealing
    best_board, best_score = simulated_annealing(
        board, 
        bigram_freq, 
        dict_words, 
        dict_prefixes, 
        start_temp=5.0, 
        end_temp=0.1, 
        steps=100
    )
    print(f"Best Score Found: {best_score}")

    # Prepare the PDF
    c = canvas.Canvas("square_grid.pdf", pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_board(c, best_board)
    c.showPage()
    c.save()

    print_board(best_board)
    score = evaluate_board(best_board, dict_words, dict_prefixes)
    print(f"Board Score: {score}")


if __name__ == "__main__":
    main()
