import pygame
import sys
from script.window.disclaimer import Disclaimer
from script.scenes.game_scene import GameScene
from script.scenes.menu_scene import MenuScene
from script.scenes.endings_scene import EndingsScene
from script.manager.progress_manager import ProgressManager  # ДОБАВЬ ЭТОТ ИМПОРТ

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Novella")

# Инициализация менеджера прогресса (ДОБАВЬ ЭТУ СТРОКУ)
progress_manager = ProgressManager()

disclaimer = Disclaimer(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
main_menu = MenuScene(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
endings_menu = EndingsScene(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
game_scene = GameScene(screen, SCREEN_WIDTH, SCREEN_HEIGHT, progress_manager)  # ПЕРЕДАЙ PROGRESS_MANAGER

current_scene = disclaimer
current_state = "disclaimer"

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
        result = current_scene.handle_event(event)
        
        if current_state == "disclaimer":
            if result == "fade_out":
                pass
        elif current_state == "main_menu":
            if result == "start_game":
                current_state = "game"
                current_scene = game_scene
                game_scene.load_scene("male_story_begin")
            elif result == "show_endings":
                current_state = "endings"
                current_scene = endings_menu
                endings_menu.reload_progress()
        elif current_state == "endings":
            if result == "back_to_menu":
                current_state = "main_menu"
                current_scene = main_menu
        elif current_state == "game":
            if result == "back_to_menu":  # ИСПРАВЬ НА back_to_menu
                current_state = "main_menu"
                current_scene = main_menu
                # Пересоздаем game_scene с progress_manager
                game_scene = GameScene(screen, SCREEN_WIDTH, SCREEN_HEIGHT, progress_manager)
    
    update_result = current_scene.update()
    
    if current_state == "disclaimer" and update_result == "finished":
        current_state = "main_menu"
        current_scene = main_menu
    
    current_scene.draw()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()