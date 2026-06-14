# Файл для системы спавна врагов

import random
import config
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WAVE_INTERVAL, BASE_ENEMIES_PER_WAVE
from enemy import Drone, Meteorite


# Опциональные настройки (если их нет в config.py - используются значения по умолчанию)
MAX_ENEMIES_PER_WAVE = getattr(config, "MAX_ENEMIES_PER_WAVE", 15)
METEORITE_UNLOCK_WAVE = getattr(config, "METEORITE_UNLOCK_WAVE", 2)

# На сколько пикселей враг появляется за границей экрана (чтобы не "выпрыгивал" внезапно)
SPAWN_MARGIN = 30


class Spawner:
    """Класс для управления волнами врагов"""

    def __init__(self):
        self.timer = 0.0
        self.wave_number = 0

    def update(self, dt):
        """
        Обновление таймера спавна.

        Returns:
            list: список новых врагов, если волна готова, иначе пустой список
        """
        self.timer += dt

        if self.timer >= WAVE_INTERVAL:
            self.timer = 0.0
            self.wave_number += 1
            return self.spawn_wave()

        return []

    def spawn_wave(self):
        """
        Создать волну врагов.

        Returns:
            list: список созданных объектов Drone/Meteorite
        """
        enemies = []

        # Количество врагов растет с номером волны, но не бесконечно
        num_enemies = min(BASE_ENEMIES_PER_WAVE + self.wave_number, MAX_ENEMIES_PER_WAVE)

        # Шанс метеоритов растет с волнами (появляются не сразу, для плавной сложности)
        meteorite_chance = min(0.15 + self.wave_number * 0.05, 0.6)

        for _ in range(num_enemies):
            x, y = self._random_edge_position()

            if self.wave_number >= METEORITE_UNLOCK_WAVE and random.random() < meteorite_chance:
                enemy = Meteorite(x, y)
            else:
                enemy = Drone(x, y)

            enemies.append(enemy)

        return enemies

    def _random_edge_position(self):
        """Случайная позиция чуть за краем экрана (сверху/справа/снизу/слева)"""
        side = random.randint(0, 3)

        if side == 0:  # сверху
            x = random.randint(0, SCREEN_WIDTH)
            y = -SPAWN_MARGIN
        elif side == 1:  # справа
            x = SCREEN_WIDTH + SPAWN_MARGIN
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # снизу
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + SPAWN_MARGIN
        else:  # слева
            x = -SPAWN_MARGIN
            y = random.randint(0, SCREEN_HEIGHT)

        return x, y

    def reset(self):
        """Сброс спавнера (например, при перезапуске игры)"""
        self.timer = 0.0
        self.wave_number = 0
