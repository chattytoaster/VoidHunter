# Файл для классов игровых сущностей
# Developer B должен реализовать все классы

import pygame
import math
import random
from config import *


class Player:
    """Класс игрока - управляемый корабль"""
    
    def __init__(self, x, y):
        # TODO: инициализировать позицию, скорость, HP, размер
        pass
        
    def update(self, dt, keys, mouse_pos):
        """Обновление игрока"""
        # TODO: реализовать движение WASD
        # TODO: применить скорость к позиции
        # TODO: ограничить границами экрана
        pass
        
    def shoot(self, mouse_x, mouse_y):
        """Создать пулю в направлении мыши"""
        # TODO: создать объект Bullet и вернуть его
        pass
        
    def take_damage(self, amount):
        """Получить урон"""
        # TODO: уменьшить HP
        pass
        
    def is_dead(self):
        """Проверка смерти"""
        # TODO: вернуть True если HP <= 0
        return False
        
    def render(self, screen):
        """Отрисовка игрока"""
        # TODO: нарисовать треугольник pygame.draw.polygon()
        pass


class Drone:
    """Класс дрона - преследует игрока"""
    
    def __init__(self, x, y):
        # TODO: инициализировать позицию, HP, размер, скорость, урон, очки
        pass
        
    def update(self, dt, player_x, player_y):
        """Обновление дрона"""
        # TODO: вычислить направление к игроку
        # TODO: двигаться к игроку
        pass
        
    def take_damage(self, amount):
        """Получить урон"""
        # TODO: уменьшить HP
        pass
        
    def is_dead(self):
        """Проверка смерти"""
        # TODO: вернуть True если HP <= 0
        return False
        
    def render(self, screen):
        """Отрисовка дрона"""
        # TODO: нарисовать ромб pygame.draw.polygon()
        pass


class Meteorite:
    """Класс метеорита - летит прямо"""
    
    def __init__(self, x, y):
        # TODO: инициализировать позицию, скорость, HP, размер, урон, очки
        pass
        
    def update(self, dt):
        """Обновление метеорита"""
        # TODO: двигаться прямо
        # TODO: отскок от верха/низа экрана
        pass
        
    def take_damage(self, amount):
        """Получить урон"""
        # TODO: уменьшить HP
        pass
        
    def is_dead(self):
        """Проверка смерти"""
        # TODO: вернуть True если HP <= 0
        return False
        
    def render(self, screen):
        """Отрисовка метеорита"""
        # TODO: нарисовать круг pygame.draw.circle()
        pass


class Bullet:
    """Класс пули игрока"""
    
    def __init__(self, x, y, target_x, target_y):
        # TODO: инициализировать позицию, размер, урон
        # TODO: вычислить направление к цели (vx, vy)
        pass
        
    def update(self, dt):
        """Обновление пули"""
        # TODO: двигаться по направлению
        pass
        
    def is_off_screen(self, width, height):
        """Проверка вылета за экран"""
        # TODO: проверить границы экрана
        return False
        
    def render(self, screen):
        """Отрисовка пули"""
        # TODO: нарисовать круг pygame.draw.circle()
        pass
