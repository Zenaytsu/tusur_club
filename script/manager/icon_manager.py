import pygame
import os
from script.utils import get_elzova_path

class IconManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.icons = {}
        self.current_icon = None
        self.current_icon_surface = None
        self.show_icon = True
        
        self.animation_state = None 
        self.animation_progress = 0
        self.animation_speed = 0.05
        self.original_icon = None
        self.animated_icon = None
        
    def load_icon(self, name):
        if name == "no_icon" or not name:
            return None
            
        if name in self.icons:
            return self.icons[name]
            
        icon_path = get_elzova_path("icons", name)
        if os.path.exists(icon_path):
            try:
                icon = pygame.image.load(icon_path)
                
                if name == "курточка.png":
                    icon_height = int(self.HEIGHT * 0.6)
                elif name in ["1_1.png", "красавица_стоит.png","1_4.png","курточка.png"]:
                    icon_height = int(self.HEIGHT * 0.65)
                elif name in ["1_2.png", "1_3.png", "красопетка.png"]:
                    icon_height = int(self.HEIGHT * 0.55)
                else:
                    icon_height = int(self.HEIGHT * 0.45)
                
                icon_width = int(icon_height * icon.get_width() / icon.get_height())
                scaled_icon = pygame.transform.smoothscale(icon, (icon_width, icon_height))
                self.icons[name] = scaled_icon
                return scaled_icon
            except:
                return None
        else:
            return None
    
    def start_zoom_animation(self, icon_name, animation_type):
        if icon_name == "no_icon" or not icon_name:
            return
            
        self.original_icon = self.load_icon(icon_name)
        if self.original_icon:
            self.animation_state = animation_type
            self.animation_progress = 0
            self.animated_icon = self.original_icon.copy()
    
    def update_animation(self):
        if self.animation_state and self.original_icon:
            self.animation_progress += self.animation_speed
            
            if self.animation_progress >= 1:
                self.animation_progress = 1
                if self.animation_state == "zoom_in":
                    self.animation_state = "zoom_out"
                    self.animation_progress = 0
                else:
                    self.animation_state = None
                    self.animated_icon = None
                    return
            if self.animation_state == "zoom_in":
                scale = 1 + self.animation_progress * 0.3
            else:  # zoom_out
                scale = 1.3 - self.animation_progress * 0.3
                
            original_rect = self.original_icon.get_rect()
            new_width = int(original_rect.width * scale)
            new_height = int(original_rect.height * scale)
            self.animated_icon = pygame.transform.smoothscale(self.original_icon, (new_width, new_height))
    
    def set_current_icon(self, icon_name):
        if icon_name == "no_icon" or not icon_name:
            self.show_icon = False
            self.current_icon = None
            self.current_icon_surface = None
            self.animation_state = None
        else:
            self.show_icon = True
            self.current_icon = icon_name
            self.current_icon_surface = self.load_icon(icon_name)
            self.animation_state = None
    
    def draw(self):
        if self.show_icon:
            if self.animation_state:
                self.update_animation()
                icon_to_draw = self.animated_icon
            else:
                icon_to_draw = self.current_icon_surface
                
            if icon_to_draw:
                if self.current_icon in ["1_2.png", "1_3.png", "1_4.png", "красопетка.png","курточка.png"]:
                    icon_x = self.WIDTH - icon_to_draw.get_width() - int(self.WIDTH * 0.1)
                else:
                    icon_x = self.WIDTH - icon_to_draw.get_width() - int(self.WIDTH * 0.02)
                
                icon_y = self.HEIGHT - icon_to_draw.get_height() - int(self.HEIGHT * 0.25)
                
                self.screen.blit(icon_to_draw, (icon_x, icon_y))