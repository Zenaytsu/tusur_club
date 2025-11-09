import pygame

class BaseScene:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
    
    def handle_event(self, event):
        raise NotImplementedError("Subclasses must implement handle_event")
    
    def update(self):
        raise NotImplementedError("Subclasses must implement update")
    
    def draw(self):
        raise NotImplementedError("Subclasses must implement draw")
    
    def load_scene(self, scene_name):
        raise NotImplementedError("Subclasses must implement load_scene")