import pygame
import os
from .base_scene import BaseScene
from script.utils import scale_background, get_elzova_path

class MenuScene(BaseScene):
    def __init__(self, screen, width, height):
        super().__init__(screen, width, height)
        
        bg_path = get_elzova_path("bg", "bg_start.png")
        if os.path.exists(bg_path):
            self.bg_start_img = pygame.image.load(bg_path).convert()
            self.bg_start_img = scale_background(self.bg_start_img, self.WIDTH, self.HEIGHT)
        else:
            self.bg_start_img = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.bg_start_img.fill((0, 0, 0))

        self.button_font_size = max(36, int(self.HEIGHT * 0.04))
        try:
            self.button_font = pygame.font.Font("Nunito-Bold.ttf", self.button_font_size)
        except:
            self.button_font = pygame.font.SysFont("arial", self.button_font_size)
        
        button_width = int(self.WIDTH * 0.3)
        button_height = int(self.HEIGHT * 0.1)
        
        self.button_color = (255, 255, 255)
        self.button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.button_rect.centerx = self.WIDTH // 2
        self.button_rect.bottom = self.HEIGHT - int(self.HEIGHT * 0.2)

        self.endings_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.endings_button_rect.centerx = self.WIDTH // 2
        self.endings_button_rect.bottom = self.HEIGHT - int(self.HEIGHT * 0.05)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                return "start_game"
            if self.endings_button_rect.collidepoint(event.pos):
                return "show_endings"
        return None

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.bg_start_img, (0, 0))
        
        pygame.draw.rect(self.screen, self.button_color, self.button_rect, border_radius=30)
        text = self.button_font.render("ИГРАТЬ", True, (60, 56, 141))
        text_rect = text.get_rect(center=self.button_rect.center)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, self.button_color, self.endings_button_rect, border_radius=30)
        text2 = self.button_font.render("ДОСТИЖЕНИЯ", True, (60, 56, 141))
        text2_rect = text2.get_rect(center=self.endings_button_rect.center)
        self.screen.blit(text2, text2_rect)

    def load_scene(self, scene_name):
        pass