import pygame

class DialogManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        
        self.dialogue_font_size = max(20, int(self.HEIGHT * 0.035))
        self.name_font_size = max(24, int(self.HEIGHT * 0.04))
        
        try:
            self.dialogue_font = pygame.font.Font("Verdana", self.dialogue_font_size)
            self.name_font = pygame.font.Font("Verdana", self.name_font_size)
        except:
            self.dialogue_font = pygame.font.SysFont("Verdana", self.dialogue_font_size, bold=False)
            self.name_font = pygame.font.SysFont("Verdana", self.name_font_size, bold=True)

    def draw_dialog_window(self, current_dialogue):
        border_color = current_dialogue["speaker"]["color"]
        speaker_name = current_dialogue["speaker"]["name"]
        
        dialog_width = int(self.WIDTH * 0.8)
        dialog_height = int(self.HEIGHT * 0.25)
        dialog_rect = pygame.Rect(
            (self.WIDTH - dialog_width) // 2,
            self.HEIGHT - dialog_height - int(self.HEIGHT * 0.02),
            dialog_width, 
            dialog_height
        )
        
        border_thickness = max(3, int(dialog_height * 0.015))
        
        pygame.draw.rect(self.screen, border_color, dialog_rect, border_radius=30)
        inner_rect = pygame.Rect(
            dialog_rect.x + border_thickness, 
            dialog_rect.y + border_thickness, 
            dialog_width - border_thickness * 2, 
            dialog_height - border_thickness * 2
        )
        pygame.draw.rect(self.screen, (30, 30, 30), inner_rect, border_radius=25)
        
        name_zone_height = int(dialog_height * 0.25)
        name_zone_rect = pygame.Rect(
            inner_rect.x,
            inner_rect.y,
            inner_rect.width,
            name_zone_height
        )
        
        text_zone_rect = pygame.Rect(
            inner_rect.x,
            inner_rect.y + name_zone_height,
            inner_rect.width,
            inner_rect.height - name_zone_height
        )
        
        if speaker_name:
            name_text = self.name_font.render(speaker_name, True, border_color)
            name_rect = name_text.get_rect()
            name_rect.bottomleft = (name_zone_rect.x + 40, name_zone_rect.bottom - 10)
            self.screen.blit(name_text, name_rect)
        
        text = current_dialogue["text"]
        self.draw_wrapped_text(text, text_zone_rect)

    def draw_wrapped_text(self, text, text_zone_rect):
        words = text.split(' ')
        lines = []
        current_line = []
        max_width = text_zone_rect.width - 80
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = self.dialogue_font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        line_height = int(self.dialogue_font_size * 1.3)
        text_y = text_zone_rect.y + 20
        
        for line in lines:
            text_surface = self.dialogue_font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(centerx=text_zone_rect.centerx, y=text_y)
            self.screen.blit(text_surface, text_rect)
            text_y += line_height
    def draw_skip_button(self):
        skip_width = int(self.WIDTH * 0.12)
        skip_height = int(self.HEIGHT * 0.05)
        skip_x = self.WIDTH - skip_width - int(self.WIDTH * 0.03)
        skip_y = self.HEIGHT - skip_height - int(self.HEIGHT * 0.03)

        self.skip_rect = pygame.Rect(skip_x, skip_y, skip_width, skip_height)

        pygame.draw.rect(self.screen, (255, 255, 255), self.skip_rect, border_radius=10)
        font = pygame.font.SysFont("Verdana", max(20, int(self.HEIGHT * 0.025)), bold=True)
        text = font.render("СКИП", True, (0, 0, 0))
        text_rect = text.get_rect(center=self.skip_rect.center)
        self.screen.blit(text, text_rect)
