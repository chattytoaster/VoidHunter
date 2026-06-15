# Файл для звуковой системы

import pygame
import os

DEFAULT_SOUNDS = {
    "shoot": "shoot.wav",
    "explosion": "explosion.wav",
    "player_hit": "hit.wav",
    "pickup": "collect.wav",
    "game_over": "game_over.wav",
}

SOUNDS_DIR = os.path.join("assets", "sounds")


class SoundManager:
    """Менеджер звуков"""

    def __init__(self, sounds_dir=SOUNDS_DIR, sound_map=None):
        self.sounds = {}
        self.volume = 1.0
        self.enabled = True
        self.mixer_ready = False
        self.sounds_dir = sounds_dir

        try:
            pygame.mixer.init()
            self.mixer_ready = True
            print("Sound mixer initialized")
        except pygame.error as e:
            print(f"Audio not available: {e}")

        if self.mixer_ready:
            sound_map = DEFAULT_SOUNDS if sound_map is None else sound_map
            for name, filename in sound_map.items():
                self.load_sound(name, os.path.join(sounds_dir, filename))

    def load_sound(self, name, filepath):
        if not self.mixer_ready:
            return False

        if not os.path.exists(filepath):
            print(f"Sound file not found: {filepath}")
            return False

        try:
            sound = pygame.mixer.Sound(filepath)
            sound.set_volume(self.volume)
            self.sounds[name] = sound
            print(f"Loaded sound: {name}")
            return True
        except pygame.error as e:
            print(f"Error loading {name}: {e}")
            return False

    def play(self, name):
        if not self.mixer_ready or not self.enabled:
            return

        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()
            print(f"Playing sound: {name}")

    def play_background_music(self, loop=True):
        """Воспроизвести фоновую музыку из файла game_sound.wav"""
        if not self.mixer_ready or not self.enabled:
            return

        music_path = os.path.join(SOUNDS_DIR, "game_sound.wav")

        if not os.path.exists(music_path):
            print(f"Background music not found: {music_path}")
            return

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            if loop:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.play()
            print("Playing background music: game_sound.wav")
        except pygame.error as e:
            print(f"Error playing background music: {e}")

    def set_volume(self, volume):
        """
        Установить общую громкость для всех звуков.

        Args:
            volume (float): значение от 0.0 до 1.0
        """
        self.volume = max(0.0, min(1.0, volume))

        for sound in self.sounds.values():
            sound.set_volume(self.volume)

        if self.mixer_ready:
            try:
                pygame.mixer.music.set_volume(self.volume * 0.5)
            except pygame.error:
                pass

    def toggle_mute(self):
        """
        Включить/выключить звук.

        Returns:
            bool: новое состояние (True - звук включен)
        """
        self.enabled = not self.enabled
        if self.mixer_ready:
            try:
                if not self.enabled:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            except pygame.error:
                pass
        return self.enabled

    def play_music(self, filename="game_sound.wav", loop=-1):
        """
        Воспроизведение фоновой музыки.
        
        Args:
            filename (str): имя файла музыки в папке assets/sounds
            loop (int): количество повторений (-1 для бесконечного цикла)
        """
        if not self.mixer_ready or not self.enabled:
            return
            
        filepath = os.path.join(self.sounds_dir, filename)
        if not os.path.exists(filepath):
            return
            
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(self.volume * 0.5)  # Делаем музыку тише эффектов
            pygame.mixer.music.play(loop)
        except pygame.error:
            pass

    def stop_music(self):
        """Остановка фоновой музыки"""
        if not self.mixer_ready:
            return
            
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass
