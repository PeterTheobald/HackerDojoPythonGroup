import copy
import math
import random
from typing import (
    Dict,
    Generator,
    List,
    Optional,
    Set,
    Tuple,
)

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import Color

ROWS = 13
COLS = 10

HEX_DIAM = 0.9 * inch
SIDE = HEX_DIAM / 2.0

PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 11 * inch

X_SPACING = math.sqrt(3) * SIDE
Y_SPACING = 1.5 * SIDE

LIGHT_BLUE = Color(0.9, 0.9, 1)
LIGHT_RED = Color(1, 0.8, 0.8)

LONG_WORD_MULTIPLIER = 3.0


def load_start_frequencies(
    filename: str = "start-letter-freqs.txt",
) -> List[Tuple[str, float]]:
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
    if total > 0:
        freqs = [(ltr, val / total) for (ltr, val) in freqs]
    return freqs


def load_bigrams(filename: str = "bigram-freqs.txt") -> Dict[str, Dict[str, float]]:
    """
    Load bigram frequencies from a file where each line has:
       X Y 0.12
    We'll store them in a dict-of-dicts:
       bigram_freq[X][Y] = frequency
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


def load_dictionary(filename: str = "dict.txt") -> Tuple[Set[str], Set[str]]:
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
            w = line.strip().upper()
            if w:
                words.add(w)
                for i in range(1, len(w) + 1):
                    prefixes.add(w[:i])
    return words, prefixes


def pick_from_distribution(freq_pairs: List[Tuple[str, float]]) -> str:
    """
    freq_pairs is a list of (letter, probability),
    with probabilities summing to ~1.0.
    """
    r = random.random()
    accum = 0.0
    for letter, p in freq_pairs:
        accum += p
        if r <= accum:
            return letter
    return freq_pairs[-1][0]


def pick_start_letter(start_freq: List[Tuple[str, float]]) -> str:
    """
    Pick a letter using the "start letter" frequencies (already normalized).
    """
    return pick_from_distribution(start_freq)


def pick_letter_bigrams(
    bigram_freq: Dict[str, Dict[str, float]], neighbor_letters: List[str]
) -> str:
    """
    Given a set of neighbor letters, compute a weighted distribution of all
    possible letters based on the sum of bigram frequencies from each neighbor.
    """
    candidate_letters = set()
    for n in neighbor_letters:
        if n in bigram_freq:
            candidate_letters.update(bigram_freq[n].keys())

    if not candidate_letters:
        all_known_letters = set()
        for first in bigram_freq:
            all_known_letters.update(bigram_freq[first].keys())
        if not all_known_letters:
            return "A"
        candidate_letters = all_known_letters

    weights = []
    total_weight = 0.0
    for letter in candidate_letters:
        w = 0.0
        for n in neighbor_letters:
            w += bigram_freq.get(n, {}).get(letter, 0.0)
        if w > 0:
            weights.append((letter, w))
            total_weight += w

    if total_weight <= 0:
        return random.choice(sorted(candidate_letters))

    dist = [(letter, w / total_weight) for (letter, w) in weights]
    return pick_from_distribution(dist)


def get_neighbors(r: int, c: int) -> Generator[Tuple[int, int], None, None]:
    """
    Return up to 6 neighbors for hex cell (r,c) in a pointy-top layout.
    """
    offsets_even = [
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, 0),
        (1, 1),
    ]
    offsets_odd = [
        (-1, -1),
        (-1, 0),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
    ]
    if r % 2 == 0:
        neighbors = offsets_even
    else:
        neighbors = offsets_odd

    for dr, dc in neighbors:
        rr = r + dr
        cc = c + dc
        if 0 <= rr < ROWS and 0 <= cc < COLS:
            yield rr, cc


def evaluate_board(
    board: List[List[str]], words_set: Set[str], prefixes_set: Set[str]
) -> float:
    """
    Calculate a "score" for the board, defined as:
      - For each cell, do a depth-first search of all possible paths.
      - For each path that forms a word of length >=4, add the length of that word to the total
        times LONG_WORD_MULTIPLIER (plus row-based multipliers).
      - We track visited cells so we don't reuse a cell in the same word.
      - We prune whenever the partial word is not in prefixes_set.
      - Return the total score.
    """
    total_score = 0.0

    def dfs(
        r: int,
        c: int,
        visited: Set[Tuple[int, int]],
        current_word: str,
        starting_home_row: bool,
    ) -> None:
        nonlocal total_score

        if len(current_word) >= 4 and current_word in words_set:
            if starting_home_row:
                starting_row_multiplier = 3
            else:
                starting_row_multiplier = 1
            total_score += (
                len(current_word) * LONG_WORD_MULTIPLIER * starting_row_multiplier
            )

        for nr, nc in get_neighbors(r, c):
            if (nr, nc) not in visited:
                next_letter = board[nr][nc]
                next_word = current_word + next_letter
                if next_word in prefixes_set:
                    visited.add((nr, nc))
                    dfs(nr, nc, visited, next_word, starting_home_row)
                    visited.remove((nr, nc))

    for row_idx in range(ROWS):
        for col_idx in range(COLS):
            start_letter = board[row_idx][col_idx]
            if not start_letter:
                continue
            if start_letter not in prefixes_set:
                continue
            visited = set()
            visited.add((row_idx, col_idx))
            dfs(
                row_idx,
                col_idx,
                visited,
                start_letter,
                (row_idx == 0 or row_idx == ROWS - 1),
            )

    return total_score


def generate_initial_board(
    start_freq: List[Tuple[str, float]], bigram_freq: Dict[str, Dict[str, float]]
) -> List[List[str]]:
    """
    Create a new board of ROWS x COLS letters.
    Fill top row, bottom row, then fill the middle rows in a preset order.
    """
    board = [["" for _ in range(COLS)] for _ in range(ROWS)]

    for col in range(COLS):
        board[0][col] = pick_start_letter(start_freq)
    for col in range(COLS):
        board[ROWS - 1][col] = pick_start_letter(start_freq)

    fill_order = [1, 11, 2, 10, 3, 9, 4, 8, 5, 7, 6]
    for r in fill_order:
        if 0 <= r < ROWS:
            for col in range(COLS):
                if board[r][col] == "":
                    neighbor_letters = []
                    for nr, nc in get_neighbors(r, col):
                        if board[nr][nc]:
                            neighbor_letters.append(board[nr][nc])
                    chosen_letter = pick_letter_bigrams(bigram_freq, neighbor_letters)
                    board[r][col] = chosen_letter
    return board


def simulated_annealing(
    board: List[List[str]],
    bigram_freq: Dict[str, Dict[str, float]],
    dict_words: Set[str],
    dict_prefixes: Set[str],
    start_temp: float = 5.0,
    end_temp: float = 0.1,
    steps: int = 100,
) -> Tuple[List[List[str]], float]:
    """
    Simulated Annealing will randomize parts of the board looking for better boards.
    It will start with a "high temperature" and randomize many cells in order to explore
    more variety and find better global maximums.
    As the "temperature" drops it will randomize progressively fewer cells in order to
    explore minor variations of the better boards to find local maximums.
    """
    current_board = copy.deepcopy(board)
    best_board = copy.deepcopy(board)

    current_score = evaluate_board(current_board, dict_words, dict_prefixes)
    best_score = current_score

    for i in range(steps):
        frac = i / float(steps)
        T = start_temp + (end_temp - start_temp) * frac

        new_board = copy.deepcopy(current_board)

        n_changes = int(round(T * 5))
        for _ in range(n_changes):
            rr = random.randint(0, ROWS - 1)
            cc = random.randint(0, COLS - 1)
            neighbor_letters = []
            for nr, nc in get_neighbors(rr, cc):
                neighbor_letters.append(new_board[nr][nc])
            new_letter = pick_letter_bigrams(bigram_freq, neighbor_letters)
            new_board[rr][cc] = new_letter

        new_score = evaluate_board(new_board, dict_words, dict_prefixes)

        delta = new_score - current_score
        if delta > 0:
            current_board = new_board
            current_score = new_score
        else:
            prob = math.exp(delta / T) if T > 0 else 0
            if random.random() < prob:
                current_board = new_board
                current_score = new_score

        if current_score > best_score:
            best_score = current_score
            best_board = copy.deepcopy(current_board)

    return best_board, best_score


def print_board(b: List[List[str]]) -> None:
    """Print the board in a simple text format."""
    for line in b:
        print("".join(line))


def draw_hex(
    c: canvas.Canvas,
    x_center: float,
    y_center: float,
    side: float,
    fillColor: Optional[Color] = None,
) -> None:
    """
    Draw a pointy-top hex centered at (x_center, y_center).
    The 'side' is the distance from center to any vertex along one side.
    We offset the angle by -30 so that a vertex points straight up.
    """
    path = c.beginPath()
    for i in range(6):
        angle_deg = 60 * i - 30
        angle = math.radians(angle_deg)
        px = x_center + side * math.cos(angle)
        py = y_center + side * math.sin(angle)
        if i == 0:
            path.moveTo(px, py)
        else:
            path.lineTo(px, py)
    path.close()

    if fillColor:
        c.setFillColor(fillColor)
    else:
        c.setFillColorRGB(1, 1, 1)

    c.setStrokeColorRGB(0, 0, 0)
    c.drawPath(path, fill=1, stroke=1)


def draw_board(c: canvas.Canvas, board: List[List[str]]) -> None:
    """
    Draw the board as a hex grid onto the given Canvas.
    """
    total_width = (COLS - 1) * X_SPACING + 2 * SIDE
    total_height = (ROWS - 1) * Y_SPACING + 2 * SIDE

    x0 = (PAGE_WIDTH - total_width) / 2 + SIDE / 2
    y0 = (PAGE_HEIGHT - total_height) / 2 + SIDE / 2

    for r in range(ROWS):
        for col in range(COLS):
            letter = board[r][col]

            if r % 2 == 1:
                x_offset = x0 + col * X_SPACING + (X_SPACING / 2.0)
            else:
                x_offset = x0 + col * X_SPACING
            y_offset = y0 + r * Y_SPACING

            fill_color = None
            if r == 0:
                fill_color = LIGHT_RED
            elif r == ROWS - 1:
                fill_color = LIGHT_BLUE

            draw_hex(c, x_offset, y_offset, SIDE, fillColor=fill_color)

            if letter:
                c.setFillColorRGB(0, 0, 0)
                c.setFont("Helvetica", 10)
                if letter == "Q":
                    c.drawCentredString(x_offset, y_offset - 3, "Qu")
                else:
                    c.drawCentredString(x_offset, y_offset - 3, letter)


def main() -> None:
    start_freq = load_start_frequencies("start-letter-freqs.txt")
    bigram_freq = load_bigrams("bigram-freqs.txt")
    dict_words, dict_prefixes = load_dictionary("dict.txt")

    board = generate_initial_board(start_freq, bigram_freq)
    initial_score = evaluate_board(board, dict_words, dict_prefixes)
    print(f"Initial Score: {initial_score}")

    best_board, best_score = simulated_annealing(
        board,
        bigram_freq,
        dict_words,
        dict_prefixes,
        start_temp=5.0,
        end_temp=0.1,
        steps=100,
    )
    print(f"Best Score Found: {best_score}")

    c = canvas.Canvas("hex_grid.pdf", pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_board(c, best_board)
    c.showPage()
    c.save()

    print_board(best_board)
    final_score = evaluate_board(best_board, dict_words, dict_prefixes)
    print(f"Board Score: {final_score}")


if __name__ == "__main__":
    main()
