import math
import random
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import Color

# Light colors for top/bottom row fills
LIGHT_BLUE = Color(0.9, 0.9, 1)
LIGHT_RED = Color(1, 0.8, 0.8)

PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 11 * inch
HEX_DIAM = 0.9 * inch
SIDE = HEX_DIAM / 2
COLS = 10
ROWS = 13

def load_letter_frequencies(filename):
    """
    Load letter frequencies from a file where each line has the format:
      A 12.9
    This means letter 'A' has a frequency value of 12.9.
    convert these values into fractions that sum to 1.
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
    """Randomly pick a letter based on the normalized frequency distribution."""
    r = random.random()
    cumulative = 0.0
    for letter, freq in letter_freq:
        cumulative += freq
        if r <= cumulative:
            return letter
    return letter_freq[-1][0]  # Fallback in case of rounding errors

def fill_grid(letter_freq):
    """Fill the grid row-by-row with letters picked from the frequency distribution."""
    grid = []
    for r in range(ROWS):
        row_letters = []
        for c in range(COLS):
            row_letters.append(pick_letter(letter_freq))
        grid.append(row_letters)
    return grid

def draw_hex(c, x, y, side, fillColor=None):
    """Draw a pointy-top hexagon centered at (x, y)."""
    path = c.beginPath()
    for i in range(6):
        angle = math.radians(60 * i - 30)  # -30 so one vertex points straight up
        px = x + side * math.cos(angle)
        py = y + side * math.sin(angle)
        if i == 0:
            path.moveTo(px, py)
        else:
            path.lineTo(px, py)
    path.close()

    c.setFillColor(fillColor if fillColor else Color(1,1,1))
    c.setStrokeColorRGB(0,0,0)
    c.drawPath(path, fill=1, stroke=1)

def main():
    # Load frequencies from file (adjust filename if needed)
    letter_freq = load_letter_frequencies("big-boggle-freqs.txt")

    # Generate the grid of letters
    grid = fill_grid(letter_freq)

    # Create the PDF canvas
    c = canvas.Canvas("hex_grid.pdf", pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    # Calculate spacing for pointy-top hexagons
    x_spacing = math.sqrt(3) * SIDE
    y_spacing = 1.5 * SIDE

    # Compute total grid width/height in drawing space
    total_width = x_spacing * (COLS - 1) + 2 * SIDE
    total_height = y_spacing * (ROWS - 1) + 2 * SIDE

    # Offsets to center the grid on the page
    x0 = (PAGE_WIDTH - total_width) / 2 + SIDE/2
    y0 = (PAGE_HEIGHT - total_height) / 2 + SIDE/2

    # Draw the hexes and letters
    for r in range(ROWS):
        for col in range(COLS):
            letter = grid[r][col]
            x_offset = x0 + col * x_spacing + (x_spacing / 2 if r % 2 else 0)
            y_offset = y0 + r * y_spacing

            # Color the top row red, bottom row blue
            fill_color = None
            if r == 0:
                fill_color = LIGHT_RED
            elif r == ROWS - 1:
                fill_color = LIGHT_BLUE

            draw_hex(c, x_offset, y_offset, SIDE, fillColor=fill_color)

            # Place the letter in the center
            c.setFillColorRGB(0,0,0)
            c.setFont("Helvetica", 10)
            c.drawCentredString(x_offset, y_offset - 3, letter)
            if letter=='Q':
                c.drawCentredString(x_offset, y_offset - 3, 'Qu')
            else:
                c.drawCentredString(x_offset, y_offset - 3, letter)

    c.showPage()
    c.save()

if __name__ == "__main__":
    main()
