# Snake - example videogame using Pygame
# @ControlAltPete 2025 for Hacker Dojo Python group
# V1 - move a block around the screen with arrows
# V2 - constantly moving, arrows change direction
# V3 - hitting the edge = GAME OVER
# V4 - snake has several segments, not just a single block
# V5 - drop food squares the snake can eat
# V6 - add score
# V7 - snake can't hit it's own tail

import pygame
import sys
import random

pygame.init()

# Screen and border settings
screen_width, screen_height = 640, 480
border_thickness = 5
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake with Tail, Food, and Score")

# Colors
SNAKE_COLOR = (0, 150, 0)
FOOD_COLOR = (0, 255, 0)
BG_COLOR = (0, 0, 0)
BORDER_COLOR = (255, 0, 0)
GAME_OVER_COLOR = (255, 0, 0)
SCORE_COLOR = (255, 255, 255)

# Each snake block is 30x30; we keep a small gap by moving in steps of (rect_size + gap).
rect_size = 30
gap = 2
step = rect_size + gap

font = pygame.font.SysFont(None, 48)
score_font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()
game_over = False
score = 0

# Generate valid positions aligned to our grid
valid_x_positions = list(range(border_thickness, screen_width - rect_size - border_thickness + 1, step))
valid_y_positions = list(range(border_thickness, screen_height - rect_size - border_thickness + 1, step))

# Pick a starting position aligned to the valid grid (near bottom center)
start_x = valid_x_positions[len(valid_x_positions) // 2]
start_y = valid_y_positions[-2]

# Create an initial snake of length 4 (head + 3-tail), vertical alignment
snake_segments = [
    (start_x, start_y),
    (start_x, start_y + step),
    (start_x, start_y + 2 * step),
    (start_x, start_y + 3 * step),
]

# Initial direction is up
direction = (0, -1)

def draw_border():
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, screen_width, screen_height), border_thickness)

def end_game():
    screen.fill(BG_COLOR)
    text_surface = font.render("GAME OVER", True, GAME_OVER_COLOR)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()

def draw_score(scr):
    score_surface = score_font.render(f"Score: {scr}", True, SCORE_COLOR)
    score_rect = score_surface.get_rect(x=10, y=10)
    screen.blit(score_surface, score_rect)
    return score_rect

def get_new_food_pos():
    return (
        random.choice(valid_x_positions),
        random.choice(valid_y_positions)
    )

# Place the first food
food_pos = get_new_food_pos()

# Initial draw
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

# Draw initial score
score_rect = draw_score(score)

pygame.display.update()

running = True
while running:
    clock.tick(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            # Change direction if not opposite
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

        # Insert new head at the front
        snake_segments.insert(0, new_head)

        # If we ate the food
        if new_head == food_pos:
            score += 100
            old_food_pos = food_pos
            food_pos = get_new_food_pos()

            # Erase old food
            pygame.draw.rect(screen, BG_COLOR, (old_food_pos[0], old_food_pos[1], rect_size, rect_size))

            # Draw new food
            pygame.draw.rect(screen, FOOD_COLOR, (food_pos[0], food_pos[1], rect_size, rect_size), border_radius=5)
            
            old_food_rect = pygame.Rect(old_food_pos[0], old_food_pos[1], rect_size, rect_size)
            new_food_rect = pygame.Rect(food_pos[0], food_pos[1], rect_size, rect_size)
        else:
            # Normal move, remove old tail
            snake_segments.pop()
            pygame.draw.rect(screen, BG_COLOR, (old_tail[0], old_tail[1], rect_size, rect_size))
            old_food_rect = None
            new_food_rect = None

        # Check self-collision (if head is in the rest of the body)
        if new_head in snake_segments[1:]:
            game_over = True
            end_game()
            continue

        # Draw new head
        pygame.draw.rect(screen, SNAKE_COLOR, (new_head[0], new_head[1], rect_size, rect_size), border_radius=5)

        # Redraw border
        draw_border()

        # Redraw score
        pygame.draw.rect(screen, BG_COLOR, score_rect)  # Erase old score
        score_rect = draw_score(score)

        # Prepare partial updates
        old_tail_rect = pygame.Rect(old_tail[0], old_tail[1], rect_size, rect_size)
        new_head_rect = pygame.Rect(new_head[0], new_head[1], rect_size, rect_size)
        border_rect = pygame.Rect(0, 0, screen_width, screen_height)
        
        update_list = [new_head_rect, border_rect, score_rect]

        if old_food_rect:
            update_list.append(old_food_rect)
        if new_food_rect:
            update_list.append(new_food_rect)
        # Add tail rect if it was popped
        if not (new_head == food_pos):
            update_list.append(old_tail_rect)

        pygame.display.update(update_list)

pygame.quit()
sys.exit()
