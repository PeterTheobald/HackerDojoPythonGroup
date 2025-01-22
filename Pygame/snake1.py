# Snake - example videogame using Pygame
# @ControlAltPete 2025 for Hacker Dojo Python group
# V1 - move a block around the screen


import pygame
import sys

pygame.init()
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

x, y = screen_width // 2, screen_height // 2
rect_width, rect_height = 30, 30
speed = 5

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x = max(0, x - speed)
    if keys[pygame.K_RIGHT]:
        x = min(screen_width - rect_width, x + speed)
    if keys[pygame.K_UP]:
        y = max(0, y - speed)
    if keys[pygame.K_DOWN]:
        y = min(screen_height - rect_height, y + speed)
    
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, rect_width, rect_height), border_radius=10)
    pygame.display.flip()

pygame.quit()
sys.exit()
