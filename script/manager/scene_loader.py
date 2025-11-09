# script/manager/scene_loader.py (модифицированный)
from script.scenario.story_data import story_data

class SceneLoader:
    def __init__(self, progress_manager, skip_manager, background_manager, 
                 icon_manager, audio_manager, achievement_notifier=None):
        self.progress_manager = progress_manager
        self.skip_manager = skip_manager
        self.background_manager = background_manager
        self.icon_manager = icon_manager
        self.audio_manager = audio_manager
        self.achievement_notifier = achievement_notifier
        
        self.current_scene = "male_story_begin"
        self.current_music = None
        self.music_changed = False

    def load_scene(self, scene_name):
        """Загружает сцену и определяет доступность кнопки скипа."""
        if scene_name not in story_data:
            print(f"[WARN] Scene '{scene_name}' not found in story_data")
            return

        # Загружаем свежие данные о прогрессе
        self.progress_manager.load_progress()

        # Настройка базовых параметров сцены
        scene = story_data[scene_name]
        self.current_scene = scene_name

        # Обновляем иконки и музыку
        self.icon_manager.set_current_icon(None)
        new_music = self.get_scene_music(scene)

        if new_music == "no_sound":
            self.audio_manager.stop_music()
            self.current_music = None
            self.music_changed = True
        elif new_music and new_music != self.current_music:
            self.audio_manager.play_music(new_music)
            self.current_music = new_music
            self.music_changed = True
        elif new_music is None:
            self.music_changed = False
        else:
            self.music_changed = False

        # Загружаем фон сцены
        if "bg" in scene:
            self.background_manager.load_background(scene["bg"])

        # Логика скипа
        self.skip_manager.calculate_skip_availability(scene_name, self.progress_manager)

    def get_scene_music(self, scene_data):
        if "song" in scene_data:
            return scene_data["song"]
        elif "sound" in scene_data:
            return scene_data["sound"]
        return None

    def mark_scene_completion(self, scene_name):
        """Отмечает завершение сцены в прогрессе"""
        # Основные концовки - отмечаем ТОЛЬКО настоящие финалы
        if scene_name in ["end_1", "MakSim", "dom_Elcovoi"]:
            self.progress_manager.mark_ending_completed(scene_name)
            # Показываем уведомление о достижении
            if self.achievement_notifier:
                achievement_info = self.get_achievement_info(scene_name)
                if achievement_info:
                    self.achievement_notifier.add_notification(achievement_info[0], achievement_info[1])
        
        # Дополнительные ветки - отмечаем ВСЕГДА при завершении сцены
        self.skip_manager.mark_branch_completed(scene_name, self.progress_manager)
        
        # Для branch_svidanie тоже показываем уведомление
        if scene_name == "branch_svidanie" and self.achievement_notifier:
            self.achievement_notifier.add_notification("Красавчик", "Не зассал позвать Ельцову на свидание")

    def get_achievement_info(self, scene_name):
        """Возвращает информацию о достижении по имени сцены"""
        achievement_map = {
            "cafe": ("Чашка кофе", "Сводить Ельцову в кафе"),
            "park": ("Прогулка в парке", "Сводить Ельцову в парк"),
            "dom_Elcovoi": ("Подъездный романтик", "Поцеловаться с Ельцовой у ее дома"),
            "MakSim": ("Знаешь ли ты...", "Вдоль ночных дорог, шла босиком не жалея ног"),
            "end_1": ("Сыкло", "Зассал позвать чиксу-Ельцову на свиданку")
        }
        return achievement_map.get(scene_name)