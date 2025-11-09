import pygame
import os

def get_elzova_path(*path_parts):
    return os.path.join("src", "elzova", *path_parts)

def scale_background(image, target_width, target_height):
    img_width, img_height = image.get_size()
    
    target_ratio = target_width / target_height
    img_ratio = img_width / img_height
    
    scale_x = target_width / img_width
    scale_y = target_height / img_height
    scale = max(scale_x, scale_y)
    
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
    scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))
    
    x = (scaled_image.get_width() - target_width) // 2
    y = (scaled_image.get_height() - target_height) // 2
    
    result = scaled_image.subsurface((x, y, target_width, target_height)).copy()
    return result

def draw_text(surface, text, size, color, position, font_name=None):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)