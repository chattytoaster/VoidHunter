# Файл для звуковой системы
# Developer C должен реализовать класс SoundManager

import pygame
import os


class SoundManager:
    """Менеджер звуков"""
    
    def __init__(self):
        # TODO: инициализировать pygame.mixer
        # TODO: создать словарь для звуков
        # TODO: загрузить звуки из папки assets/sounds
        pass
        
    def load_sound(self, name, filepath):
        """Загрузить звук из файла"""
        # TODO: проверить существование файла
        # TODO: загрузить звук через pygame.mixer.Sound
        # TODO: сохранить в словарь self.sounds
        pass
    
    def play(self, name):
        """Воспроизвести звук"""
        # TODO: проверить наличие звука в словаре
        # TODO: воспроизвести звук через .play()
        pass
