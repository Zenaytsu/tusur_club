import pygame
import os
from script.utils import scale_background, get_elzova_path

class BackgroundManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        
        self.current_background = None
        self.next_background = None
        self.bg_transition = False
        self.bg_fade_alpha = 0
        self.bg_fade_speed = 5

    def update(self):
        if self.bg_transition:
            self.bg_fade_alpha += self.bg_fade_speed
            if self.bg_fade_alpha >= 255:
                self.current_background = self.next_background
                self.next_background = None
                self.bg_transition = False
                self.bg_fade_alpha = 0

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        if self.current_background:
            self.screen.blit(self.current_background, (0, 0))
        
        if self.bg_transition and self.next_background:
            self.next_background.set_alpha(self.bg_fade_alpha)
            self.screen.blit(self.next_background, (0, 0))
            self.next_background.set_alpha(255)

    def load_background(self, bg_name):
        if bg_name:
            bg_path = get_elzova_path("bg", bg_name)
            if os.path.exists(bg_path):
                new_bg = pygame.image.load(bg_path).convert()
                new_bg = scale_background(new_bg, self.WIDTH, self.HEIGHT)
                self.start_background_transition(new_bg)
    
    def start_background_transition(self, new_background):
        if self.current_background is None:
            self.current_background = new_background
        else:
            self.next_background = new_background
            self.bg_transition = True
            self.bg_fade_alpha = 0