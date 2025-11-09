import pygame
import os
import time
from script.utils import scale_background, get_elzova_path

class Disclaimer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        
        disclaimer_path = get_elzova_path("bg", "dis.png")
        if os.path.exists(disclaimer_path):
            self.disclaimer_img = pygame.image.load(disclaimer_path).convert()
            self.disclaimer_img = scale_background(self.disclaimer_img, self.WIDTH, self.HEIGHT)
        else:
            self.disclaimer_img = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.disclaimer_img.fill((0, 0, 0))

        self.start_time = time.time()
        self.fade_alpha = 0
        self.fade_speed = 2
        self.finished = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.finished = True
            return "fade_out"
        return None
    
    def update(self):
        if not self.finished and time.time() - self.start_time > 5:
            self.finished = True
            return "fade_out"
        
        if self.finished:
            self.fade_alpha += self.fade_speed
            if self.fade_alpha >= 255:
                return "finished"
        
        return None
    
    def draw(self):
        """Отрисовка дисклеймера"""
        self.screen.blit(self.disclaimer_img, (0, 0))
        
        if self.finished:
            fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(fade_surface, (0, 0))