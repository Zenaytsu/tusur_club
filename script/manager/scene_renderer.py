import pygame
from script.scenario.story_data import story_data

class SceneRenderer:
    def __init__(self, screen, width, height, dialog_manager, choice_manager, 
                 background_manager, icon_manager, skip_manager):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.dialog_manager = dialog_manager
        self.choice_manager = choice_manager
        self.background_manager = background_manager
        self.icon_manager = icon_manager
        self.skip_manager = skip_manager

    def draw_game_scene(self, current_scene, dialogue_handler):
        self.background_manager.draw()
        self.icon_manager.draw()

        scene = story_data[current_scene]

        if "dialogue" in scene and dialogue_handler.dialogue_index > 0:
            current_dialogue = scene["dialogue"][dialogue_handler.dialogue_index - 1]
            self.dialog_manager.draw_dialog_window(current_dialogue)
        else:
            dummy = {"speaker": {"name": "", "color": (255, 255, 255)}, "text": ""}
            self.dialog_manager.draw_dialog_window(dummy)

        print(
            f"[DEBUG draw] Scene:{current_scene} can_skip:{self.skip_manager.can_skip} "
            f"waiting:{dialogue_handler.waiting_for_choice} end:{dialogue_handler.end_shown} idx:{dialogue_handler.dialogue_index}"
        )

        if (self.skip_manager.can_skip and not dialogue_handler.waiting_for_choice 
            and not dialogue_handler.end_shown):
            self.skip_manager.draw_skip_button()

        if (dialogue_handler.waiting_for_choice and "choices" in scene 
            and not dialogue_handler.end_shown):
            self.choice_manager.draw_choices(scene["choices"])

        if dialogue_handler.end_shown:
            self.draw_return_hint()

    def draw_return_hint(self):
        hint_font_size = max(16, int(self.HEIGHT * 0.02))
        try:
            hint_font = pygame.font.Font("Verdana", hint_font_size)
        except:
            hint_font = pygame.font.SysFont("Verdana", hint_font_size)

        hint_text = hint_font.render("Нажмите для возврата в главное меню", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 30))
        self.screen.blit(hint_text, hint_rect)