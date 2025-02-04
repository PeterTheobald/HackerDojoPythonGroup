import math
import random
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import Color

# Grid size
ROWS = 13
COLS = 10

# We'll define the "pointy-top" hex so that its top-to-bottom diameter is 0.75 inches
HEX_DIAM = 0.75 * inch
SIDE = HEX_DIAM / 2.0  # side length of the hex

# Page size in inches
PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 11 * inch

# Spacing for a pointy-top hex grid:
#  - Horizontal center-to-center: sqrt(3) * side
#  - Vertical center-to-center: 1.5 * side
X_SPACING = math.sqrt(3) * SIDE
Y_SPACING = 1.5 * SIDE

# Light colors for top/bottom row fills
LIGHT_BLUE = Color(0.9, 0.9, 1)
LIGHT_RED = Color(1, 0.8, 0.8)

def load_start_frequencies(filename="start-freq.txt"):
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

def load_bigrams(filename="bigrams.txt"):
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

def pick_from_distribution(freq_pairs):
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
    # Collect candidate letters from neighbors
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

    # Compute weight for each candidate letter
    weights = []
    total_weight = 0.0
    for letter in candidate_letters:
        w = 0.0
        for n in neighbor_letters:
            w += bigram_freq.get(n, {}).get(letter, 0.0)
        if w > 0:
            weights.append((letter, w))
            total_weight += w

    # If all weights are zero or no data, pick randomly from candidates
    if total_weight <= 0:
        return random.choice(sorted(candidate_letters))

    # Normalize to probabilities
    dist = [(letter, w / total_weight) for (letter, w) in weights]
    return pick_from_distribution(dist)

def get_neighbors(r, c):
    """
    Return up to 8 neighbors for hex cell (r,c) in a pointy-top layout.
    We'll assume "odd-r horizontal layout" or "even-r horizontal layout",
    but the offsets commonly used for pointy-top. 
    For a standard approach:
      Even-row:  neighbors = [(-1,0), (-1,1), (0,-1), (0,1), (1,0), (1,1), (-1,-1?), (1,-1?) ... etc]
      Odd-row:   neighbors = [(-1,-1), (-1,0), (0,-1), (0,1), (1,-1), (1,0)]
    We'll try the typical 'odd-r' approach:
    """
    offsets_even = [
        (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, 0),  (1, 1),
        # You can add or remove diagonals if you want 8 directions including NW/NE/SE/SW
        # but typically a hex has 6 neighbors. We'll allow up to 6 here. 
    ]
    offsets_odd = [
        (-1, -1), (-1, 0),
        (0, -1),            (0, 1),
        (1, -1),  (1, 0),
    ]
    # If you truly want 8 neighbors, that might not be a standard hex adjacency.
    # But let's assume 6 neighbors for typical hex grid:
    if r % 2 == 0:
        neighbors = offsets_even
    else:
        neighbors = offsets_odd

    for dr, dc in neighbors:
        rr = r + dr
        cc = c + dc
        if 0 <= rr < ROWS and 0 <= cc < COLS:
            yield rr, cc

def draw_hex(c, x_center, y_center, side, fillColor=None):
    """
    Draw a pointy-top hex centered at (x_center, y_center).
    The 'side' is the distance from center to any vertex along one side.
    We offset the angle by -30 so that a vertex points straight up.
    """
    path = c.beginPath()
    for i in range(6):
        angle_deg = 60 * i - 30  # -30 so top vertex is straight up
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

def main():
    # Load data
    start_freq = load_start_frequencies("start-freq.txt")
    bigram_freq = load_bigrams("bigrams.txt")

    # Prepare the PDF
    c = canvas.Canvas("hex_grid.pdf", pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    # We'll store letters in a 2D list
    grid = [["" for _ in range(COLS)] for _ in range(ROWS)]

    # Assign the top row (row = 0) from start frequencies
    for col in range(COLS):
        grid[0][col] = pick_start_letter(start_freq)

    # Assign the bottom row (row = ROWS-1) from start frequencies
    for col in range(COLS):
        grid[ROWS - 1][col] = pick_start_letter(start_freq)

    # Fill the remaining rows in the order: 1, 11, 2, 10, 3, 9, 4, 8, 5, 7, 6
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

                chosen_letter = pick_letter_bigrams(bigram_freq, neighbor_letters)
                grid[r][col] = chosen_letter

    # Now draw the hex grid
    # We'll compute total bounding box to center on page
    #  - width ~ (COLS - 1) * X_SPACING + (2 * SIDE)
    #  - height ~ (ROWS - 1) * Y_SPACING + (2 * SIDE)
    total_width = (COLS - 1) * X_SPACING + 2 * SIDE
    total_height = (ROWS - 1) * Y_SPACING + 2 * SIDE

    # Offsets to center the grid on the page
    x0 = (PAGE_WIDTH - total_width) / 2 + SIDE
    y0 = (PAGE_HEIGHT - total_height) / 2 + SIDE

    # Draw each cell
    for r in range(ROWS):
        for col in range(COLS):
            letter = grid[r][col]

            # For pointy-top hex coordinates:
            #   x_offset = x0 + col * X_SPACING (+ half X_SPACING if row is odd?)
            #   y_offset = y0 + r * Y_SPACING
            # But we only shift x for odd rows if we're using the "odd-r" approach
            if r % 2 == 1:
                x_offset = x0 + col * X_SPACING + (X_SPACING / 2.0)
            else:
                x_offset = x0 + col * X_SPACING
            y_offset = y0 + r * Y_SPACING

            # Fill color for top row vs bottom row
            fill_color = None
            if r == 0:
                fill_color = LIGHT_RED
            elif r == ROWS - 1:
                fill_color = LIGHT_BLUE

            draw_hex(c, x_offset, y_offset, SIDE, fillColor=fill_color)

            # Place the letter in the center
            if letter:
                c.setFillColorRGB(0, 0, 0)
                c.setFont("Helvetica", 10)
                # A small vertical offset can help center the text
                if letter=='Q':
                    c.drawCentredString(x_offset, y_offset - 3, 'Qu')
                else:
                    c.drawCentredString(x_offset, y_offset - 3, letter)

    c.showPage()
    c.save()

if __name__ == "__main__":
    main()
