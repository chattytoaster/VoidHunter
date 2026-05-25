import random
import math
from config import *
from src.enemy import Asteroid, Drone


class WaveSpawner:
    """Класс для управления волнами врагов"""
    
    def __init__(self):
        """Инициализация спавнера"""
        self.wave_timer = WAVE_INTERVAL
        self.wave_number = 0
        
    def update(self, dt, charge_level, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Обновление таймера волн"""
        self.wave_timer -= dt
        
        # Если время волны истекло
        if self.wave_timer <= 0:
            self.wave_timer = WAVE_INTERVAL
            self.wave_number += 1
            return self.spawn_wave(charge_level, screen_width, screen_height)
        
        return []
    
    def spawn_wave(self, charge_level, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Создание новой волны врагов"""
        # Вычисление количества врагов
        base_count = BASE_ENEMIES_PER_WAVE + (self.wave_number * ENEMIES_INCREASE_PER_WAVE)
        
        # Множитель от уровня заряда игрока
        charge_multiplier = 1.0 + (charge_level * CHARGE_SPAWN_MULTIPLIER)
        
        total_enemies = int(base_count * charge_multiplier)
        
        # Создание врагов
        enemies = []
        for i in range(total_enemies):
            # Случайный выбор типа врага
            if random.random() < ASTEROID_SPAWN_WEIGHT:
                # Астероид
                pos = self.get_spawn_position(screen_width, screen_height)
                enemies.append(Asteroid(pos[0], pos[1]))
            else:
                # Дрон
                pos = self.get_spawn_position(screen_width, screen_height)
                enemies.append(Drone(pos[0], pos[1]))
        
        return enemies
    
    def get_spawn_position(self, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Получить случайную позицию для спавна (за краями экрана)"""
        # Выбираем случайную сторону экрана
        side = random.randint(0, 3)
        
        if side == 0:  # Верх
            x = random.randint(0, screen_width)
            y = -SPAWN_MARGIN
        elif side == 1:  # Право
            x = screen_width + SPAWN_MARGIN
            y = random.randint(0, screen_height)
        elif side == 2:  # Низ
            x = random.randint(0, screen_width)
            y = screen_height + SPAWN_MARGIN
        else:  # Лево
            x = -SPAWN_MARGIN
            y = random.randint(0, screen_height)
        
        return (x, y)
    
    def reset(self):
        """Сброс спавнера"""
        self.wave_timer = WAVE_INTERVAL
        self.wave_number = 0
