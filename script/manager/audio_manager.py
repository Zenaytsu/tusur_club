# script/manager/audio_manager.py
import pygame
import os
from script.utils import get_elzova_path

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.current_music = None
        self.music_volume = 0.5
        self.sound_volume = 0.7
        
    def load_sound(self, sound_name):
        if sound_name == "no_sound" or not sound_name:
            return None
            
        if sound_name in self.sounds:
            return self.sounds[sound_name]
            
        sound_path = get_elzova_path("sound", sound_name)
        if os.path.exists(sound_path):
            try:
                sound = pygame.mixer.Sound(sound_path)
                sound.set_volume(self.sound_volume)
                self.sounds[sound_name] = sound
                return sound
            except:
                return None
        else:
            return None
    
    def play_sound(self, sound_name):
        if sound_name == "no_sound" or not sound_name:
            return
            
        sound = self.load_sound(sound_name)
        if sound:
            sound.play()
    
    def play_music(self, music_name, loops=-1):
        if music_name == "no_sound" or not music_name:
            self.stop_music()
            return False
            
        if music_name == self.current_music:
            return False
            
        self.stop_music()
            
        music_path = get_elzova_path("sound", music_name)
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops)
                self.current_music = music_name
                return True
            except Exception as e:
                return False
        else:
            return False
    
    def stop_music(self):
        if self.current_music:
            pygame.mixer.music.stop()
            self.current_music = None
    
    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sound_volume(self, volume):
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)