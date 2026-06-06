import pygame
import os
from OLD.config import *


class SoundManager:
    """Менеджер звуковых эффектов"""
    
    def __init__(self):
        """Инициализация звуковой системы"""
        self.sounds = {}
        self.sound_enabled = True
        
        # Инициализация микшера
        try:
            pygame.mixer.init()
        except:
            self.sound_enabled = False
            return
        
        # Определяем базовую директорию (где находится main.py)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sounds_dir = os.path.join(base_dir, 'assets', 'sounds')
        
        # Загрузка звуков
        self.load_sound('shoot', os.path.join(sounds_dir, 'shoot.wav'))
        self.load_sound('explosion', os.path.join(sounds_dir, 'explosion.wav'))
        self.load_sound('collect', os.path.join(sounds_dir, 'collect.wav'))
        self.load_sound('void_flash', os.path.join(sounds_dir, 'void_flash.wav'))
        self.load_sound('hit', os.path.join(sounds_dir, 'hit.wav'))
        
    def load_sound(self, name, filepath):
        """Загрузка звукового файла"""
        if not self.sound_enabled:
            return
        
        try:
            if os.path.exists(filepath):
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(SOUND_VOLUME)
                self.sounds[name] = sound
            else:
                self.sounds[name] = None
        except:
            self.sounds[name] = None
    
    def play(self, name):
        """Воспроизведение звука"""
        if not self.sound_enabled:
            return
        
        if name in self.sounds and self.sounds[name] is not None:
            try:
                self.sounds[name].play()
            except:
                pass
