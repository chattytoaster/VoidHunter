import random
from OLD.config import *
from OLD.src.enemy import Drone, Meteorite, Gunship


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
        enemies = []

        for i in range(total_enemies):
            # Случайный выбор типа врага
            roll = random.random()
            pos = self.get_spawn_position(screen_width, screen_height)
            if roll < GUNSHIP_SPAWN_WEIGHT:
                enemies.append(Gunship(pos[0], pos[1]))
            elif roll < GUNSHIP_SPAWN_WEIGHT + METEORITE_SPAWN_WEIGHT:
                meteor_pos = self.get_offscreen_spawn_position(screen_width, screen_height)
                enemies.append(Meteorite(meteor_pos[0], meteor_pos[1]))
            else:
                enemies.append(Drone(pos[0], pos[1]))
        
        return enemies
    
    def get_spawn_position(self, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Получить случайную позицию для спавна на границе экрана"""
        side = random.randint(0, 3)

        edge_pad = 8
        if side == 0:  # Верх
            x = random.randint(edge_pad, screen_width - edge_pad)
            y = edge_pad
        elif side == 1:  # Право
            x = screen_width - edge_pad
            y = random.randint(edge_pad, screen_height - edge_pad)
        elif side == 2:  # Низ
            x = random.randint(edge_pad, screen_width - edge_pad)
            y = screen_height - edge_pad
        else:  # Лево
            x = edge_pad
            y = random.randint(edge_pad, screen_height - edge_pad)
        
        return (x, y)

    def get_offscreen_spawn_position(self, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Позиция за правой границей (для метеоритов)"""
        x = screen_width + SPAWN_MARGIN
        y = random.randint(40, max(40, screen_height - 40))
        return (x, y)
    
    def reset(self):
        """Сброс спавнера"""
        self.wave_timer = WAVE_INTERVAL
        self.wave_number = 0
