from script.scenario.story_data import story_data

class DialogueHandler:
    def __init__(self, progress_manager, background_manager, icon_manager, 
                 audio_manager, scene_loader):
        self.progress_manager = progress_manager
        self.background_manager = background_manager
        self.icon_manager = icon_manager
        self.audio_manager = audio_manager
        self.scene_loader = scene_loader
        
        self.dialogue_index = 0
        self.waiting_for_choice = False
        self.end_shown = False
        
        self.kiss_animation_active = False
        self.kiss_animation_count = 0
        self.max_kiss_animations = 3

    def next_dialogue(self, current_scene):
        scene = story_data[current_scene]

        if "dialogue" in scene:
            if self.dialogue_index < len(scene["dialogue"]):
                dialogue = scene["dialogue"][self.dialogue_index]

                dialogue_music = None
                if "song" in dialogue:
                    dialogue_music = dialogue["song"]
                elif "sound" in dialogue:
                    dialogue_music = dialogue["sound"]

                if dialogue_music:
                    if dialogue_music == "no_sound":
                        self.audio_manager.stop_music()
                    elif dialogue_music != self.scene_loader.current_music:
                        self.audio_manager.play_music(dialogue_music)
                        self.scene_loader.current_music = dialogue_music

                if current_scene == "dom_Elcovoi":
                    if self.dialogue_index == 10:
                        self.icon_manager.start_zoom_animation("красопетка_1.png", "zoom_in")
                        self.audio_manager.play_sound("kiss.mp3")
                    elif self.dialogue_index == 12:
                        self.kiss_animation_active = True
                        self.kiss_animation_count = 0
                        self.start_kiss_animation_cycle()

                if "bg" in dialogue:
                    self.background_manager.load_background(dialogue["bg"])

                if "icon" in dialogue:
                    self.icon_manager.set_current_icon(dialogue["icon"])

                if "sound" in dialogue and ("song" not in dialogue and dialogue.get("sound") != dialogue_music):
                    self.audio_manager.play_sound(dialogue["sound"])
                if "effect" in dialogue:
                    self.audio_manager.play_sound(dialogue["effect"])

                self.dialogue_index += 1

                if self.dialogue_index >= len(scene["dialogue"]):
                    self.scene_loader.mark_scene_completion(current_scene)
                    
                    if current_scene in ["end_1", "MakSim", "dom_Elcovoi"]:
                        self.end_shown = True
            else:
                if "choices" in scene and scene["choices"]:
                    self.waiting_for_choice = True
        else:
            if "choices" in scene and scene["choices"]:
                self.waiting_for_choice = True

    def start_kiss_animation_cycle(self):
        """Запускает цикл анимации поцелуя"""
        if self.kiss_animation_active and self.kiss_animation_count < self.max_kiss_animations:
            self.icon_manager.start_zoom_animation("красопетка_1.png", "zoom_in")
            self.audio_manager.play_sound("pocelui.mp3")
            self.kiss_animation_count += 1

    def handle_choice_click(self, pos, current_scene, choice_manager):
        """Обрабатывает клик по выбору"""
        scene = story_data[current_scene]
        if "choices" in scene:
            next_scene = choice_manager.handle_choice_click(pos, scene["choices"])
            if next_scene:
                if current_scene in ["cafe", "park"] and next_scene in ["dom_Elcovoi", "MakSim"]:
                    self.progress_manager.mark_ending_completed(current_scene)
                    print(f"[DEBUG] Marked {current_scene} as completed ending (led to {next_scene})")
                
                return next_scene
        return None

    def reset_dialogue_state(self):
        self.dialogue_index = 0
        self.waiting_for_choice = False
        self.end_shown = False
        self.kiss_animation_active = False
        self.kiss_animation_count = 0