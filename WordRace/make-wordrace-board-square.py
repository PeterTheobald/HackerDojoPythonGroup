import math
import random
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import Color

# Light colors for top/bottom row fills
LIGHT_BLUE = Color(0.9, 0.9, 1)
LIGHT_RED = Color(1, 0.8, 0.8)

# Number of rows and columns
ROWS = 13
COLS = 10

# Each square will be 0.75 inches per side
SQUARE_SIZE = 0.8 * inch

# Page size in inches
PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 11 * inch

def load_letter_frequencies(filename):
    """
    Load letter frequencies from a file where each line has the format:
      A 12.9
    This means letter 'A' has a frequency value of 12.9.
    We'll convert these values into fractions that sum to 1.0.
    """
    letter_freq = []
    total = 0.0

    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().upper().split()
            if len(parts) != 2:
                continue
            letter, freq_str = parts
            freq_val = float(freq_str)
            letter_freq.append((letter, freq_val))
            total += freq_val

    # Normalize so frequencies sum to 1.0
    letter_freq = [(letter, freq_val / total) for (letter, freq_val) in letter_freq]
    return letter_freq

def pick_letter(letter_freq):
    """Randomly pick a letter based on normalized frequency distribution."""
    r = random.random()
    cumulative = 0.0
    for letter, freq in letter_freq:
        cumulative += freq
        if r <= cumulative:
            return letter
    return letter_freq[-1][0]  # Fallback for rounding errors

def fill_grid(letter_freq):
    """Fill a 13x10 grid row-by-row with random letters based on frequency."""
    grid = []
    for r in range(ROWS):
        row_letters = []
        for c in range(COLS):
            row_letters.append(pick_letter(letter_freq))
        grid.append(row_letters)
    return grid

def draw_square(c, x, y, size, fillColor=None):
    """
    Draw a square with top-left corner at (x, y), side length = size.
    fillColor can be None or a reportlab.lib.colors.Color.
    """
    if fillColor:
        c.setFillColor(fillColor)
    else:
        c.setFillColorRGB(1,1,1)  # default white
    
    c.setStrokeColorRGB(0,0,0)   # black outline
    c.rect(x, y, size, size, fill=1, stroke=1)

def main():
    # Load letter frequency data
    letter_freq = load_letter_frequencies("big-boggle-freqs.txt")

    # Prepare the PDF
    c = canvas.Canvas("square_grid.pdf", pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    # Create the grid of letters
    grid = fill_grid(letter_freq)

    # Calculate total grid width/height
    total_width = COLS * SQUARE_SIZE
    total_height = ROWS * SQUARE_SIZE

    # Offsets to center the grid on the page
    x0 = (PAGE_WIDTH - total_width) / 2
    y0 = (PAGE_HEIGHT - total_height) / 2

    # Draw squares and letters
    for r in range(ROWS):
        for col in range(COLS):
            letter = grid[r][col]
            # Compute top-left corner of this square
            x_offset = x0 + col * SQUARE_SIZE
            y_offset = y0 + (ROWS - 1 - r) * SQUARE_SIZE  # so row 0 is at top

            # Color the top row red (r=0) and bottom row blue (r=ROWS-1)
            fill_color = None
            if r == 0:
                fill_color = LIGHT_RED
            elif r == ROWS - 1:
                fill_color = LIGHT_BLUE

            # Draw the square
            draw_square(c, x_offset, y_offset, SQUARE_SIZE, fillColor=fill_color)

            # Put letter in center
            c.setFillColorRGB(0,0,0)
            c.setFont("Helvetica", 10)

            # Center in the square horizontally, approx. vertically
            text_x = x_offset + SQUARE_SIZE / 2
            text_y = y_offset + SQUARE_SIZE / 2 - 3
            if letter=='Q':
                c.drawCentredString(text_x, text_y, 'Qu')
            else:
                c.drawCentredString(text_x, text_y, letter)

    c.showPage()
    c.save()

if __name__ == "__main__":
    main()

