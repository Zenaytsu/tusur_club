import pygame

class SkipManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        
        self.skip_rect = None
        self.can_skip = False
        
        self.branch_mapping = {
            "male_story_begin": "branch_male_begin",
            "svidanie_male": "branch_svidanie", 
            "cafe": "branch_cafe",
            "park": "branch_park",
            "dom_Elcovoi": "branch_dom_Elcovoi"
        }
        
        self.scene_to_ending = {
            "cafe": "cafe",
            "park": "park",
            "dom_Elcovoi": "dom_Elcovoi",
            "svidanie_male": "dom_Elcovoi",
            "male_story_begin": "cafe",
            "end_1": "end_1",
            "MakSim": "MakSim"
        }

    def calculate_skip_availability(self, scene_name, progress_manager):
        ending_key = self.scene_to_ending.get(scene_name)
        
        linked_ending_done = bool(ending_key and progress_manager.data.get(ending_key, 0) == 1)
        
        branch_done = False
        if scene_name in self.branch_mapping:
            branch_key = self.branch_mapping[scene_name]
            branch_done = progress_manager.has_completed_branch(branch_key)
        
        any_ending_done = progress_manager.has_completed_any_ending()
        is_start_scene = scene_name in ["male_story_begin", "svidanie_male", "park", "cafe"]

        self.can_skip = linked_ending_done or branch_done or (any_ending_done and is_start_scene)

        print(
            f"[SKIP MANAGER] Scene:{scene_name} "
            f"ending_key:{ending_key} linked_done:{linked_ending_done} "
            f"branch_done:{branch_done} any_done:{any_ending_done} "
            f"is_start:{is_start_scene} can_skip:{self.can_skip}"
        )
        
        return self.can_skip

    def mark_branch_completed(self, scene_name, progress_manager):
        if scene_name in self.branch_mapping:
            branch_key = self.branch_mapping[scene_name]
            progress_manager.mark_branch_completed(branch_key)
            print(f"[SKIP MANAGER] Marked branch as completed: {branch_key}")

    def draw_skip_button(self):
        if not self.can_skip:
            return
            
        size = int(self.HEIGHT * 0.05)
        x = self.WIDTH - size * 2
        y = self.HEIGHT - size * 1.5
        self.skip_rect = pygame.Rect(x - 10, y - 10, size * 1.5, size * 1.5)
        
        points = [(x, y), (x, y + size), (x + size, y + size // 2)]
        pygame.draw.polygon(self.screen, (255, 255, 255), points)
        
    def is_skip_clicked(self, pos):
        return self.can_skip and self.skip_rect and self.skip_rect.collidepoint(pos)

    def skip_dialogues(self, game_scene, story_data):
        current_scene = game_scene.scene_loader.current_scene
        scene = story_data[current_scene]
        
        if "dialogue" not in scene:
            return

        print(f"[SKIP MANAGER] Skipping dialogues in scene: {current_scene}")
        
        self.mark_branch_completed(current_scene, game_scene.progress_manager)
        
        while True:
            if game_scene.dialogue_handler.dialogue_index >= len(scene["dialogue"]):
                if "choices" in scene and scene["choices"]:
                    game_scene.dialogue_handler.waiting_for_choice = True
                break
            
            if "choices" in scene and game_scene.dialogue_handler.dialogue_index >= len(scene["dialogue"]) - 1:
                game_scene.dialogue_handler.waiting_for_choice = True
                break
            
            game_scene.dialogue_handler.next_dialogue(current_scene)
            
            if game_scene.dialogue_handler.waiting_for_choice:
                break

        print(f"[SKIP MANAGER] Skip completed. Waiting for choice: {game_scene.dialogue_handler.waiting_for_choice}")