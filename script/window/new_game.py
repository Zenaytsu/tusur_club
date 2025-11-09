import pygame
import sys
import os
import pygame.mixer
pygame.mixer.init()

pygame.init()

WIDTH = 1280
HEIGHT = 720
TITLE = "Game"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

background_path = os.path.join("bg", "bg_start.png")
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

GREEN = (58, 74, 24)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.blit(background, (0, 0))
    
    pygame.display.flip()

pygame.quit()
sys.exit()