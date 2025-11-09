# script/scenes/endings_scene.py
import pygame
from .base_scene import BaseScene
from script.manager.progress_manager import ProgressManager

class EndingsScene(BaseScene):
    def __init__(self, screen, width, height):
        super().__init__(screen, width, height)
        self.progress = ProgressManager()
        
        # Шрифты
        self.title_font_size = max(32, int(self.HEIGHT * 0.04))
        self.achievement_font_size = max(24, int(self.HEIGHT * 0.025))
        self.desc_font_size = max(18, int(self.HEIGHT * 0.02))
        
        try:
            self.title_font = pygame.font.Font("Verdana", self.title_font_size)
            self.achievement_font = pygame.font.Font("Verdana", self.achievement_font_size)
            self.desc_font = pygame.font.Font("Verdana", self.desc_font_size)
            self.button_font = pygame.font.Font("Verdana", self.achievement_font_size)
        except:
            self.title_font = pygame.font.SysFont("Verdana", self.title_font_size, bold=True)
            self.achievement_font = pygame.font.SysFont("Verdana", self.achievement_font_size, bold=True)
            self.desc_font = pygame.font.SysFont("Verdana", self.desc_font_size)
            self.button_font = pygame.font.SysFont("Verdana", self.achievement_font_size, bold=True)

        # Информация о достижениях
        self.achievement_info = {
            "branch_svidanie": ("Красавчик", "Не зассал позвать Ельцову на свидание", "src/icons/rose.png"),
            "cafe": ("Чашка кофе", "Сводить Ельцову в кафе", "src/icons/cup.png"),
            "end_1": ("Сыкло", "Зассал позвать чиксу-Ельцову на свиданку", "src/icons/ssiclo.png"),
            "park": ("Прогулка в парке", "Сводить Ельцову в парк", "src/icons/park.png"),
            "dom_Elcovoi": ("Подъездный романтик", "Поцеловаться с Ельцовой у ее дома", "src/icons/house.png"),
            "MakSim": ("Знаешь ли ты...", "Вдоль ночных дорог, шла босиком не жалея ног", "src/icons/MakSim.png"),
        }

        # Загрузка иконок
        self.achievement_icons = {}
        for key, (_, _, icon_path) in self.achievement_info.items():
            try:
                icon = pygame.image.load(icon_path).convert_alpha()
                self.achievement_icons[key] = icon
            except:
                self.achievement_icons[key] = pygame.Surface((100, 100), pygame.SRCALPHA)
                self.achievement_icons[key].fill((255, 255, 255))

        self.scroll_offset = 0
        self.max_scroll = 0
        self.is_scrolling = False
        self.scroll_speed = 30

        self.container_rect = pygame.Rect(
            self.WIDTH * 0.05, 
            self.HEIGHT * 0.02, 
            self.WIDTH * 0.9, 
            self.HEIGHT * 0.88
        )

        self.content_height = len(self.achievement_info) * (self.HEIGHT * 0.15 + 20) + 200
        self.scroll_area = pygame.Rect(
            self.container_rect.x,
            self.container_rect.y + 120,
            self.container_rect.width,
            self.container_rect.height - 140
        )

        button_width = 300
        button_height = 60
        self.back_button = pygame.Rect(
            self.WIDTH//2 - button_width//2, 
            self.container_rect.bottom + 20,
            button_width, 
            button_height
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "back_to_menu"
            
            if self.scroll_area.collidepoint(event.pos):
                if event.button == 4:
                    self.scroll_offset = min(0, self.scroll_offset + self.scroll_speed)
                elif event.button == 5:
                    self.scroll_offset = max(
                        -(self.content_height - self.scroll_area.height), 
                        self.scroll_offset - self.scroll_speed
                    )
        
        elif event.type == pygame.MOUSEMOTION:
            if self.is_scrolling and pygame.mouse.get_pressed()[0]:
                rel_y = event.rel[1]
                self.scroll_offset = max(
                    -(self.content_height - self.scroll_area.height),
                    min(0, self.scroll_offset + rel_y)
                )
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_scrolling = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll_offset = min(0, self.scroll_offset + self.scroll_speed)
            elif event.key == pygame.K_DOWN:
                self.scroll_offset = max(
                    -(self.content_height - self.scroll_area.height), 
                    self.scroll_offset - self.scroll_speed
                )
        
        return None

    def update(self):
        self.max_scroll = max(0, self.content_height - self.scroll_area.height)

    def draw(self):
        self.screen.fill((60, 56, 141))

        pygame.draw.rect(self.screen, (255, 255, 255), self.container_rect, border_radius=30)

        title_text = self.title_font.render("ДОСТИЖЕНИЯ", True, (60, 56, 141))
        title_rect = title_text.get_rect(center=(self.WIDTH // 2, self.container_rect.y + 60))
        self.screen.blit(title_text, title_rect)

        content_surface = pygame.Surface((self.scroll_area.width, self.content_height), pygame.SRCALPHA)
        content_surface.fill((255, 255, 255, 0))

        achievement_height = self.HEIGHT * 0.15
        achievement_width = self.scroll_area.width * 0.9
        start_y = 0
        gap = 20

        keys = ["cafe", "park", "dom_Elcovoi", "MakSim", "end_1", "branch_svidanie"]
        
        for i, key in enumerate(keys):
            if key in self.progress.data:
                value = self.progress.data.get(key, 0)
            else:
                value = self.progress.branch_flags.get(key, 0)
            
            original_name, original_description, original_icon_path = self.achievement_info.get(key, (key, "", ""))
            
            if value == 0:
                display_name = "???"
                display_description = "???"
                display_icon_path = "src/icons/hz.png"
            else:
                display_name = original_name
                display_description = original_description
                display_icon_path = original_icon_path
            
            color = (60, 56, 141) if value == 1 else (26, 24, 62)

            achievement_rect = pygame.Rect(
                self.scroll_area.width * 0.05,
                start_y + i * (achievement_height + gap),
                achievement_width,
                achievement_height
            )
            
            pygame.draw.rect(content_surface, color, achievement_rect, border_radius=30)

            # Увеличиваем иконки (с 0.6 до 0.75 от высоты блока)
            icon_size = int(achievement_height * 0.75)
            if value == 0:
                try:
                    icon = pygame.image.load("src/icons/hz.png").convert_alpha()
                except:
                    icon = pygame.Surface((100, 100), pygame.SRCALPHA)
                    icon.fill((200, 200, 200))
            else:
                icon = self.achievement_icons.get(key)
                if not icon:
                    try:
                        icon = pygame.image.load(display_icon_path).convert_alpha()
                    except:
                        icon = pygame.Surface((100, 100), pygame.SRCALPHA)
                        icon.fill((255, 255, 255))
            
            if icon:
                icon = pygame.transform.smoothscale(icon, (icon_size, icon_size))
                # Центрируем иконку по вертикали
                icon_rect = icon.get_rect(center=(
                    achievement_rect.x + achievement_rect.width * 0.15,
                    achievement_rect.centery
                ))
                content_surface.blit(icon, icon_rect)

            # Сдвигаем текст ближе к иконкам (с 0.3 до 0.25 от ширины блока)
            name_text = self.achievement_font.render(display_name, True, (255, 255, 255))
            name_rect = name_text.get_rect(
                midleft=(achievement_rect.x + achievement_rect.width * 0.25, 
                        achievement_rect.centery - 15)
            )
            
            desc_text = self.desc_font.render(display_description, True, (255, 255, 255))
            desc_rect = desc_text.get_rect(
                midleft=(achievement_rect.x + achievement_rect.width * 0.25, 
                        achievement_rect.centery + 15)
            )
            
            content_surface.blit(name_text, name_rect)
            content_surface.blit(desc_text, desc_rect)

        clipped_content = content_surface.subsurface(
            pygame.Rect(0, -self.scroll_offset, self.scroll_area.width, self.scroll_area.height)
        )
        
        self.screen.blit(clipped_content, self.scroll_area.topleft)

        if self.content_height > self.scroll_area.height:
            scrollbar_height = max(30, self.scroll_area.height * (self.scroll_area.height / self.content_height))
            scrollbar_y = self.scroll_area.y + (-self.scroll_offset / self.content_height) * self.scroll_area.height
            scrollbar_rect = pygame.Rect(
                self.scroll_area.right - 10,
                scrollbar_y,
                8,
                scrollbar_height
            )
            pygame.draw.rect(self.screen, (200, 200, 200), scrollbar_rect, border_radius=4)

        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button, border_radius=15)
        back_text = self.button_font.render("НАЗАД", True, (60, 56, 141))
        back_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_rect)

    def reload_progress(self):
        self.progress.load_progress()

    def load_scene(self, scene_name):
        pass