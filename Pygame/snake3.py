# Snake - example videogame using Pygame
# @ControlAltPete 2025 for Hacker Dojo Python group
# V1 - move a block around the screen with arrows
# V2 - constantly moving, arrows change direction
# V3 - hitting the edge = GAME OVER

import pygame
import sys

pygame.init()
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

rect_width, rect_height = 30, 30
border_thickness = 5

# Start near bottom middle
x = (screen_width - rect_width) // 2
y = screen_height - rect_height - 10

# Initial constant velocity upwards
dx, dy = 0, -5
speed = 5

font = pygame.font.SysFont(None, 48)
game_over = False
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_UP:
                dx, dy = 0, -speed
            elif event.key == pygame.K_DOWN:
                dx, dy = 0, speed
            elif event.key == pygame.K_LEFT:
                dx, dy = -speed, 0
            elif event.key == pygame.K_RIGHT:
                dx, dy = speed, 0

    screen.fill((0, 0, 0))

    # Draw thin border
    pygame.draw.rect(screen, (255, 255, 255),
                     (0, 0, screen_width, screen_height), border_thickness)

    if not game_over:
        # Move the player
        x += dx
        y += dy

        # Check collision with border
        if (x < border_thickness or
            x + rect_width > screen_width - border_thickness or
            y < border_thickness or
            y + rect_height > screen_height - border_thickness):
            game_over = True

        # Draw player
        pygame.draw.rect(screen, (0, 255, 0),
                         (x, y, rect_width, rect_height), border_radius=5)
    else:
        # Display GAME OVER
        text_surface = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_width // 2,
                                                  screen_height // 2))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
