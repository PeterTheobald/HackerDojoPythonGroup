# Snake - example videogame using Pygame
# @ControlAltPete 2025 for Hacker Dojo Python group
# V1 - move a block around the screen with arrows
# V2 - constantly moving, arrows change direction
# V3 - hitting the edge = GAME OVER
# V4 - snake has several segments, not just a single block

import pygame
import sys

pygame.init()

# Screen and border settings
screen_width, screen_height = 640, 480
border_thickness = 5
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake with Tail")

# Snake block settings
rect_size = 30
padding = 2  # Small gap between segments
step = rect_size + padding  # Distance each segment moves to avoid overlap

# Initial snake: head + 3-tail (4 segments total), lined vertically
start_x = (screen_width - rect_size) // 2
start_y = screen_height - rect_size - 10
snake_segments = [
    (start_x, start_y),
    (start_x, start_y + step),
    (start_x, start_y + step * 2),
    (start_x, start_y + step * 3)
]

# Directions use grid steps (dx, dy)
direction = (0, -1)  # Start moving up

# Fonts and game states
font = pygame.font.SysFont(None, 48)
game_over = False

def draw_full_snake():
    for (sx, sy) in snake_segments:
        pygame.draw.rect(screen, (0, 255, 0),
                         (sx, sy, rect_size, rect_size),
                         border_radius=5)

def draw_border():
    pygame.draw.rect(screen, (255, 0, 0),
                     (0, 0, screen_width, screen_height),
                     border_thickness)

def end_game():
    screen.fill((0, 0, 0))
    text_surface = font.render("GAME OVER", True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()

clock = pygame.time.Clock()

screen.fill((0, 0, 0))
draw_border()
draw_full_snake()
pygame.display.update()

running = True
while running:
    clock.tick(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    if not game_over:
        old_tail = snake_segments[-1]
        head_x, head_y = snake_segments[0]
        dx, dy = direction
        new_head = (head_x + dx * step, head_y + dy * step)

        if (new_head[0] < border_thickness or
            new_head[0] + rect_size > screen_width - border_thickness or
            new_head[1] < border_thickness or
            new_head[1] + rect_size > screen_height - border_thickness):
            game_over = True
            end_game()
            continue

        snake_segments.insert(0, new_head)
        snake_segments.pop()

        pygame.draw.rect(screen, (0, 0, 0),
                         (old_tail[0], old_tail[1], rect_size, rect_size))

        pygame.draw.rect(screen, (0, 255, 0),
                         (new_head[0], new_head[1], rect_size, rect_size),
                         border_radius=5)

        draw_border()

        old_tail_rect = pygame.Rect(old_tail[0], old_tail[1], rect_size, rect_size)
        new_head_rect = pygame.Rect(new_head[0], new_head[1], rect_size, rect_size)
        border_rect = pygame.Rect(0, 0, screen_width, screen_height)
        # Visually update the screen, entire screen or just the specified parts
        pygame.display.update([old_tail_rect, new_head_rect, border_rect])

pygame.quit()
sys.exit()
