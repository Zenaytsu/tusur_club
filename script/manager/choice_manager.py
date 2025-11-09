import pygame

class ChoiceManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        
        self.dialogue_font_size = max(24, int(self.HEIGHT * 0.035))
        try:
            self.dialogue_font = pygame.font.Font("Nunito-Bold.ttf", self.dialogue_font_size)
        except:
            self.dialogue_font = pygame.font.SysFont("arial", self.dialogue_font_size, bold=True)

    def draw_choices(self, choices):
        choice_width = int(self.WIDTH * 0.4)
        choice_height = int(self.HEIGHT * 0.08)
        
        choice_start_y = self.HEIGHT - int(self.HEIGHT * 0.55)
        
        for i, choice in enumerate(choices):
            choice_rect = pygame.Rect(
                (self.WIDTH - choice_width) // 2,
                choice_start_y + i * (choice_height + int(self.HEIGHT * 0.02)),
                choice_width,
                choice_height
            )
            
            border_color = (100, 100, 100)
            inner_color = (0, 0, 0)
            
            pygame.draw.rect(self.screen, inner_color, choice_rect, border_radius=20)
            pygame.draw.rect(self.screen, border_color, choice_rect, 3, border_radius=20)
            
            choice_text = self.format_choice_text(choice["text"], choice_width - 40)
            text_y = choice_rect.y + (choice_height - len(choice_text) * int(self.dialogue_font_size * 1.2)) // 2
            
            for line in choice_text:
                text_surface = self.dialogue_font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(centerx=choice_rect.centerx, y=text_y)
                self.screen.blit(text_surface, text_rect)
                text_y += int(self.dialogue_font_size * 1.2)

    def format_choice_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.dialogue_font.size(test_line)[0] < max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        lines.append(' '.join(current_line))
        return lines

    def handle_choice_click(self, pos, choices):
        choice_width = int(self.WIDTH * 0.4)
        choice_height = int(self.HEIGHT * 0.08)
        
        choice_start_y = self.HEIGHT - int(self.HEIGHT * 0.55)
        
        for i, choice in enumerate(choices):
            choice_rect = pygame.Rect(
                (self.WIDTH - choice_width) // 2,
                choice_start_y + i * (choice_height + int(self.HEIGHT * 0.02)),
                choice_width,
                choice_height
            )
            if choice_rect.collidepoint(pos):
                return choice["next"]
        return None