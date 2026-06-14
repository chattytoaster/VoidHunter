# Файл для звуковой системы

import pygame
import os

DEFAULT_SOUNDS = {
    "shoot": "shoot.wav",
    "explosion": "explosion.wav",
    "player_hit": "hit.wav",
    "pickup": "collect.wav",
}

SOUNDS_DIR = os.path.join("assets", "sounds")


class SoundManager:
    """Менеджер звуков"""

    def __init__(self, sounds_dir=SOUNDS_DIR, sound_map=None):
        """
        Args:
            sounds_dir (str): путь к папке со звуками
            sound_map (dict): словарь {имя_звука: имя_файла}. По умолчанию DEFAULT_SOUNDS
        """
        self.sounds = {}
        self.volume = 1.0
        self.enabled = True
        self.mixer_ready = False

        try:
            pygame.mixer.init()
            self.mixer_ready = True
        except pygame.error:
            # Например, нет звукового устройства (сервер/контейнер без аудио)
            self.mixer_ready = False

        if self.mixer_ready:
            sound_map = DEFAULT_SOUNDS if sound_map is None else sound_map
            for name, filename in sound_map.items():
                self.load_sound(name, os.path.join(sounds_dir, filename))

    def load_sound(self, name, filepath):
        """
        Загрузить звук из файла.

        Args:
            name (str): имя, под которым звук будет сохранен
            filepath (str): путь к файлу звука

        Returns:
            bool: True, если звук успешно загружен
        """
        if not self.mixer_ready:
            return False

        if not os.path.exists(filepath):
            return False

        try:
            sound = pygame.mixer.Sound(filepath)
            sound.set_volume(self.volume)
            self.sounds[name] = sound
            return True
        except pygame.error:
            return False

    def play(self, name):
        """
        Воспроизвести звук по имени. Если звука нет или звук выключен - ничего не делает.

        Args:
            name (str): имя звука (ключ из sound_map)
        """
        if not self.mixer_ready or not self.enabled:
            return

        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()

    def set_volume(self, volume):
        """
        Установить общую громкость для всех звуков.

        Args:
            volume (float): значение от 0.0 до 1.0
        """
        self.volume = max(0.0, min(1.0, volume))

        for sound in self.sounds.values():
            sound.set_volume(self.volume)

    def toggle_mute(self):
        """
        Включить/выключить звук.

        Returns:
            bool: новое состояние (True - звук включен)
        """
        self.enabled = not self.enabled
        return self.enabled
