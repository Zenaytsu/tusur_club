class AnimationManager:
    def __init__(self, icon_manager, audio_manager):
        self.icon_manager = icon_manager
        self.audio_manager = audio_manager
        
        self.kiss_animation_active = False
        self.kiss_animation_count = 0
        self.max_kiss_animations = 3

    def update_animations(self):
        if hasattr(self.icon_manager, "update_animation"):
            self.icon_manager.update_animation()

    def handle_kiss_animation(self, current_scene, dialogue_index):
        if current_scene == "dom_Elcovoi":
            if dialogue_index == 10:
                self.icon_manager.start_zoom_animation("красопетка_1.png", "zoom_in")
                self.audio_manager.play_sound("kiss.mp3")
            elif dialogue_index == 12:
                self.kiss_animation_active = True
                self.kiss_animation_count = 0
                self.start_kiss_animation_cycle()

    def start_kiss_animation_cycle(self):
        if self.kiss_animation_active and self.kiss_animation_count < self.max_kiss_animations:
            self.icon_manager.start_zoom_animation("красопетка_1.png", "zoom_in")
            self.audio_manager.play_sound("pocelui.mp3")
            self.kiss_animation_count += 1

    def reset_kiss_animation(self):
        self.kiss_animation_active = False
        self.kiss_animation_count = 0
        if hasattr(self.icon_manager, 'animation_state'):
            self.icon_manager.animation_state = None