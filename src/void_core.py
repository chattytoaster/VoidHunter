# Файл для VoidCore класса
# Developer C должен реализовать класс VoidCore

import pygame
import math
from config import *


class VoidCore:
    """Класс собираемого ядра"""
    
    def __init__(self, x, y):
        # TODO: инициализировать позицию, размер, таймер для анимации
        pass
        
    def update(self, dt):
        """Обновление VoidCore"""
        # TODO: обновить таймер для анимации пульсации
        pass
        
    def is_collected(self, player_x, player_y, player_size):
        """Проверка сбора игроком"""
        # TODO: вычислить расстояние до игрока
        # TODO: проверить, меньше ли расстояние радиуса сбора
        return False
        
    def render(self, screen):
        """Отрисовка VoidCore"""
        # TODO: нарисовать пульсирующий круг pygame.draw.circle()
        pass
