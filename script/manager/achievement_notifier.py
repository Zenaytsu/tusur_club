# script/manager/achievement_notifier.py
import pygame
import time

class AchievementNotifier:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        
        # Шрифт для уведомлений
        self.notification_font_size = max(20, int(self.HEIGHT * 0.025))
        try:
            self.font = pygame.font.Font("Verdana", self.notification_font_size)
        except:
            self.font = pygame.font.SysFont("Verdana", self.notification_font_size, bold=True)
        
        # Очередь уведомлений
        self.notifications = []
        self.current_notification = None
        self.notification_start_time = 0
        self.notification_duration = 3  # секунды
        
        # Размеры уведомления
        self.notification_width = int(self.WIDTH * 0.4)
        self.notification_height = int(self.HEIGHT * 0.1)
        self.notification_x = self.WIDTH - self.notification_width - 20
        self.notification_y = 20

    def add_notification(self, achievement_name, achievement_description):
        """Добавляет уведомление в очередь"""
        self.notifications.append({
            "name": achievement_name,
            "description": achievement_description,
            "timestamp": time.time()
        })
        print(f"[ACHIEVEMENT] Получено: {achievement_name} - {achievement_description}")

    def update(self):
        """Обновляет состояние уведомлений"""
        current_time = time.time()
        
        # Если текущее уведомление закончилось, берем следующее
        if (self.current_notification and 
            current_time - self.notification_start_time > self.notification_duration):
            self.current_notification = None
        
        # Если нет текущего уведомления и есть в очереди, показываем следующее
        if not self.current_notification and self.notifications:
            self.current_notification = self.notifications.pop(0)
            self.notification_start_time = current_time

    def draw(self):
        if not self.current_notification:
            return
            
        notification_surface = pygame.Surface((self.notification_width, self.notification_height), pygame.SRCALPHA)
        
        bg_color = (60, 56, 141, 230)  # Синий с прозрачностью
        pygame.draw.rect(notification_surface, bg_color, (0, 0, self.notification_width, self.notification_height), border_radius=15)
        
        pygame.draw.rect(notification_surface, (255, 255, 255, 255), 
                        (0, 0, self.notification_width, self.notification_height), 
                        3, border_radius=15)
        
        title_text = self.font.render("ДОСТИЖЕНИЕ ПОЛУЧЕНО!", True, (255, 255, 255))
        
        # Позиционирование текста
        title_rect = title_text.get_rect(center=(self.notification_width // 2, 20))
        
        notification_surface.blit(title_text, title_rect)
        
        # Отображаем уведомление на экране
        self.screen.blit(notification_surface, (self.notification_x, self.notification_y))

    def is_showing_notification(self):
        return self.current_notification is not None