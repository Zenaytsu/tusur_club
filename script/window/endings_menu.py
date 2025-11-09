import pygame
from script.manager.progress_manager import ProgressManager
from script.utils import scale_background

class EndingsMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.progress = ProgressManager()

        self.font = pygame.font.SysFont("arial", max(32, int(self.HEIGHT * 0.04)), bold=True)
        self.back_button = pygame.Rect(width//2 - 150, height - 100, 300, 60)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "back_to_menu"
        return None

    def draw(self):
        self.screen.fill((20, 20, 30))
        title = self.font.render("Концовки", True, (255, 255, 255))
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 60))

        y = 150
        for name, value in self.progress.data.items():
            text = f"{name}: {'✅ Пройдена' if value == 1 else '❌ Не пройдена'}"
            surf = self.font.render(text, True, (0, 255, 0) if value else (180, 50, 50))
            self.screen.blit(surf, (self.WIDTH//2 - surf.get_width()//2, y))
            y += 60

        pygame.draw.rect(self.screen, (100, 100, 255), self.back_button, border_radius=15)
        back_text = self.font.render("Назад", True, (255, 255, 255))
        self.screen.blit(back_text, back_text.get_rect(center=self.back_button.center))
    def reload_progress(self):
        self.progress.load_progress()

