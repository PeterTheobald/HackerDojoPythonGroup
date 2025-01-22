# Snake - example videogame using Pygame
# @ControlAltPete 2025 for Hacker Dojo Python group
# V1 - move a block around the screen with arrows
# V2 - constantly moving, arrows change direction

import pygame
import sys

pygame.init()
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

rect_width, rect_height = 30, 30

# Start near the bottom middle
x = (screen_width - rect_width) // 2
y = screen_height - rect_height - 10

# Constant velocity upwards initially
dx, dy = 0, -5
speed = 5

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Change direction based on arrow key
            if event.key == pygame.K_UP:
                dx, dy = 0, -speed
            elif event.key == pygame.K_DOWN:
                dx, dy = 0, speed
            elif event.key == pygame.K_LEFT:
                dx, dy = -speed, 0
            elif event.key == pygame.K_RIGHT:
                dx, dy = speed, 0

    # Move the player
    x += dx
    y += dy

    # Stop at edges
    x = max(0, min(x, screen_width - rect_width))
    y = max(0, min(y, screen_height - rect_height))

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, rect_width, rect_height), border_radius=10)
    pygame.display.flip()

pygame.quit()
sys.exit()
