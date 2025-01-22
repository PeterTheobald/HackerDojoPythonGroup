# Snake - example videogame using Pygame
# @ControlAltPete 2025 for Hacker Dojo Python group
# V1 - move a block around the screen with arrows
# V2 - constantly moving, arrows change direction
# V3 - hitting the edge = GAME OVER
# V4 - snake has several segments, not just a single block
# V5 - drop food squares the snake can eat

import pygame
import sys
import random

pygame.init()

# Screen and border settings
screen_width, screen_height = 640, 480
border_thickness = 5
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake with Tail and Food (Aligned)")

# Colors
SNAKE_COLOR = (0, 150, 0)
FOOD_COLOR = (0, 255, 0)
BG_COLOR = (0, 0, 0)
BORDER_COLOR = (255, 0, 0)
GAME_OVER_COLOR = (255, 0, 0)

# Each snake block is 30x30; we keep a small gap by moving in steps of (rect_size + gap)
rect_size = 30
gap = 2
step = rect_size + gap

font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

game_over = False

# 1) Generate valid positions for the snake and food so the snake can land exactly on them
#    They must align to multiples of 'step' within the border.
valid_x_positions = list(range(border_thickness, screen_width - rect_size - border_thickness + 1, step))
valid_y_positions = list(range(border_thickness, screen_height - rect_size - border_thickness + 1, step))

# 2) Pick a starting position near the bottom that aligns to our valid grid
start_x = valid_x_positions[len(valid_x_positions) // 2]  # center horizontally
start_y = valid_y_positions[-2]  # near the bottom

# 3) Create an initial snake of length 4 (head + 3-tail), vertical alignment
#    Head at index 0, then tail below it
snake_segments = [
    (start_x, start_y),
    (start_x, start_y + step),
    (start_x, start_y + 2 * step),
    (start_x, start_y + 3 * step),
]

# 4) Initial direction is up
direction = (0, -1)  # dx=0, dy=-1

# Draw the border
def draw_border():
    pygame.draw.rect(
        screen,
        BORDER_COLOR,
        (0, 0, screen_width, screen_height),
        border_thickness
    )

# End game procedure
def end_game():
    screen.fill(BG_COLOR)
    text_surface = font.render("GAME OVER", True, GAME_OVER_COLOR)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()

# Generate a new food position on the valid grid
def get_new_food_pos():
    return (
        random.choice(valid_x_positions),
        random.choice(valid_y_positions)
    )

# Place the first food
food_pos = get_new_food_pos()

# Initial screen draw
screen.fill(BG_COLOR)
draw_border()
# Draw the entire initial snake
for seg_x, seg_y in snake_segments:
    pygame.draw.rect(
        screen,
        SNAKE_COLOR,
        (seg_x, seg_y, rect_size, rect_size),
        border_radius=5
    )
# Draw initial food
pygame.draw.rect(
    screen,
    FOOD_COLOR,
    (food_pos[0], food_pos[1], rect_size, rect_size),
    border_radius=5
)
pygame.display.update()

running = True
while running:
    clock.tick(5)  # Snake moves 5 steps per second
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            # Change direction if not opposite the current one
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

        # Check collision with borders
        if (new_head[0] < border_thickness or
            new_head[0] + rect_size > screen_width - border_thickness or
            new_head[1] < border_thickness or
            new_head[1] + rect_size > screen_height - border_thickness):
            game_over = True
            end_game()
            continue

        # Insert new head at front
        snake_segments.insert(0, new_head)

        # Check if we ate the food
        if new_head == food_pos:
            # Snake grows - don't pop tail
            old_food_pos = food_pos
            food_pos = get_new_food_pos()
            # Erase old food
            pygame.draw.rect(
                screen,
                BG_COLOR,
                (old_food_pos[0], old_food_pos[1], rect_size, rect_size)
            )
            # Draw new food
            pygame.draw.rect(
                screen,
                FOOD_COLOR,
                (food_pos[0], food_pos[1], rect_size, rect_size),
                border_radius=5
            )

            old_food_rect = pygame.Rect(old_food_pos[0], old_food_pos[1], rect_size, rect_size)
            new_food_rect = pygame.Rect(food_pos[0], food_pos[1], rect_size, rect_size)
        else:
            # Normal move: remove the old tail
            snake_segments.pop()
            # Erase old tail
            pygame.draw.rect(
                screen,
                BG_COLOR,
                (old_tail[0], old_tail[1], rect_size, rect_size)
            )
            old_food_rect = None
            new_food_rect = None

        # Draw the new head
        pygame.draw.rect(
            screen,
            SNAKE_COLOR,
            (new_head[0], new_head[1], rect_size, rect_size),
            border_radius=5
        )

        # Redraw border
        draw_border()

        # Prepare partial updates
        old_tail_rect = pygame.Rect(old_tail[0], old_tail[1], rect_size, rect_size)
        new_head_rect = pygame.Rect(new_head[0], new_head[1], rect_size, rect_size)
        border_rect = pygame.Rect(0, 0, screen_width, screen_height)

        update_list = [new_head_rect, border_rect]

        if old_food_rect:
            update_list.append(old_food_rect)
        if new_food_rect:
            update_list.append(new_food_rect)

        if not (new_head == food_pos):
            # Only add old tail rect if we actually popped it
            update_list.append(old_tail_rect)

        pygame.display.update(update_list)

pygame.quit()
sys.exit()
