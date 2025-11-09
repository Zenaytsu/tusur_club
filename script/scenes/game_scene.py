import pygame
from .base_scene import BaseScene
from script.manager.scene_loader import SceneLoader
from script.manager.dialogue_handler import DialogueHandler
from script.manager.scene_renderer import SceneRenderer
from script.manager.achievement_notifier import AchievementNotifier
from script.manager.background_manager import BackgroundManager
from script.manager.icon_manager import IconManager
from script.manager.skip_manager import SkipManager
from script.manager.audio_manager import AudioManager
from script.manager.dialog_manager import DialogManager
from script.manager.choice_manager import ChoiceManager

class GameScene(BaseScene):
    def __init__(self, screen, width, height, progress_manager):
        super().__init__(screen, width, height)
        
        self.background_manager = BackgroundManager(screen, width, height)
        self.icon_manager = IconManager(screen, width, height)
        self.audio_manager = AudioManager()
        self.dialog_manager = DialogManager(screen, width, height)
        self.choice_manager = ChoiceManager(screen, width, height)
        self.skip_manager = SkipManager(screen, width, height)
        self.achievement_notifier = AchievementNotifier(screen, width, height)
        
        self.scene_loader = SceneLoader(
            progress_manager=progress_manager,
            skip_manager=self.skip_manager,
            background_manager=self.background_manager,
            icon_manager=self.icon_manager,
            audio_manager=self.audio_manager,
            achievement_notifier=self.achievement_notifier
        )
        
        # DialogueHandler
        self.dialogue_handler = DialogueHandler(
            progress_manager=progress_manager,
            background_manager=self.background_manager,
            icon_manager=self.icon_manager,
            audio_manager=self.audio_manager,
            scene_loader=self.scene_loader
        )
        
        # SceneRenderer
        self.scene_renderer = SceneRenderer(
            screen=screen,
            width=width,
            height=height,
            dialog_manager=self.dialog_manager,
            choice_manager=self.choice_manager,
            background_manager=self.background_manager,
            icon_manager=self.icon_manager,
            skip_manager=self.skip_manager
        )
        
        # Прогресс
        self.progress_manager = progress_manager
        
        # Загрузка начальной сцены
        self.scene_loader.load_scene("male_story_begin")
        self.dialogue_handler.reset_dialogue_state()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если показывается конец сцены, возвращаем в меню
            if self.dialogue_handler.end_shown:
                return "back_to_menu"
            
            # Обработка скипа
            if self.skip_manager.is_skip_clicked(event.pos):
                from script.scenario.story_data import story_data
                self.skip_manager.skip_dialogues(self, story_data)
                return None
            
            # Обработка выбора
            if self.dialogue_handler.waiting_for_choice:
                next_scene = self.dialogue_handler.handle_choice_click(
                    event.pos, 
                    self.scene_loader.current_scene, 
                    self.choice_manager
                )
                if next_scene:
                    self.scene_loader.load_scene(next_scene)
                    self.dialogue_handler.reset_dialogue_state()
                    return None
            
            # Обработка диалога (левая кнопка мыши)
            elif event.button == 1:  # Левая кнопка мыши
                current_scene = self.scene_loader.current_scene
                self.dialogue_handler.next_dialogue(current_scene)
                
                # Проверка завершения сцены
                if self.dialogue_handler.end_shown:
                    self.scene_loader.mark_scene_completion(current_scene)
        
        # Обработка клавиатуры
        elif event.type == pygame.KEYDOWN:
            # Пробел или Enter для продолжения диалога
            if event.key in [pygame.K_SPACE, pygame.K_RETURN] and not self.dialogue_handler.waiting_for_choice:
                current_scene = self.scene_loader.current_scene
                self.dialogue_handler.next_dialogue(current_scene)
                
                if self.dialogue_handler.end_shown:
                    self.scene_loader.mark_scene_completion(current_scene)
            
            # Escape для возврата в меню
            elif event.key == pygame.K_ESCAPE:
                return "back_to_menu"
        
        return None

    def update(self):
        # ДОБАВЬ ЭТУ СТРОКУ - обновление анимации фона
        self.background_manager.update()
        
        # Обновление уведомлений о достижениях
        self.achievement_notifier.update()
        
        # Обновление анимации поцелуя (если активна)
        if (self.dialogue_handler.kiss_animation_active and 
            self.dialogue_handler.kiss_animation_count < self.dialogue_handler.max_kiss_animations):
            # Таймер для следующей анимации поцелуя
            current_time = pygame.time.get_ticks()
            if hasattr(self, 'last_kiss_time'):
                if current_time - self.last_kiss_time > 1000:  # 1 секунда между анимациями
                    self.dialogue_handler.start_kiss_animation_cycle()
                    self.last_kiss_time = current_time
            else:
                self.last_kiss_time = current_time

    def draw(self):
        # Отрисовка игровой сцены
        self.scene_renderer.draw_game_scene(
            self.scene_loader.current_scene,
            self.dialogue_handler
        )
        
        self.achievement_notifier.draw()

    def load_scene(self, scene_name):
        self.scene_loader.load_scene(scene_name)
        self.dialogue_handler.reset_dialogue_state()

    def get_current_scene(self):
        return self.scene_loader.current_scene

    def cleanup(self):
        self.audio_manager.stop_music()
        self.audio_manager.stop_all_sounds()