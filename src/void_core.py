# Файл для VoidCore класса

import pygame
import math
import os
import config
from config import IMAGE_VOID_CORE


# Опциональные настройки (если их нет в config.py - используются значения по умолчанию)
VOID_CORE_SIZE = getattr(config, "VOID_CORE_SIZE", 8)
VOID_CORE_PICKUP_RADIUS = getattr(config, "VOID_CORE_PICKUP_RADIUS", VOID_CORE_SIZE + 15)
VOID_CORE_COLOR = getattr(config, "COLOR_VOID_CORE", (170, 80, 255))
VOID_CORE_GLOW_COLOR = getattr(config, "COLOR_VOID_CORE_GLOW", (220, 170, 255))
VOID_CORE_PULSE_SPEED = getattr(config, "VOID_CORE_PULSE_SPEED", 4.0)
VOID_CORE_LIFETIME = getattr(config, "VOID_CORE_LIFETIME", 3.0)


class VoidCore:
    """Класс собираемого ядра (Void Core)"""

    def __init__(self, x, y, sound_manager=None):
        """
        Args:
            x (float): x координата появления
            y (float): y координата появления
            sound_manager (SoundManager, optional): Менеджер звуков для воспроизведения звука сбора
        """
        self.pos = [x, y]
        self.radius = VOID_CORE_SIZE
        self.pickup_radius = VOID_CORE_PICKUP_RADIUS
        self.timer = 0.0
        self.life_timer = 0.0  # Таймер жизни ядра
        self.active = True
        self.sound_manager = sound_manager

        # Загрузка спрайта ядра
        self.image = None
        if os.path.exists(IMAGE_VOID_CORE):
            try:
                self.image = pygame.image.load(IMAGE_VOID_CORE).convert()
                self.image.set_colorkey((0, 0, 0))
            except Exception:
                pass

    def update(self, dt):
        """
        Обновление таймера анимации пульсации и проверка времени жизни.

        Args:
            dt (float): Delta time в секундах
        """
        self.timer += dt
        self.life_timer += dt
        
        # Если ядро прожило больше VOID_CORE_LIFETIME секунд - оно исчезает
        if self.life_timer >= VOID_CORE_LIFETIME:
            self.active = False

    def is_collected(self, player_x, player_y, player_size):
        """
        Проверка сбора игроком.

        Args:
            player_x (float): x координата игрока
            player_y (float): y координата игрока
            player_size (float): радиус/размер игрока

        Returns:
            bool: True, если игрок находится в радиусе сбора
        """
        dx = self.pos[0] - player_x
        dy = self.pos[1] - player_y
        distance = math.hypot(dx, dy)

        return distance <= (self.pickup_radius + player_size)

    def collect(self):
        """
        Собрать ядро. Воспроизводит звук и возвращает True если сбор успешен.
        
        Returns:
            bool: True (ядро собрано)
        """
        if self.sound_manager:
            self.sound_manager.play("pickup")
        
        self.active = False
        return True

    def render(self, screen):
        """
        Отрисовка пульсирующего ядра (спрайт или векторный круг) с эффектом сияния.

        Args:
            screen (pygame.Surface): поверхность экрана
        """
        if not self.active:
            return
            
        x, y = int(self.pos[0]), int(self.pos[1])

        # Коэффициент пульсации от 0 до 1 (плавная синусоида)
        pulse = (math.sin(self.timer * VOID_CORE_PULSE_SPEED) + 1) / 2

        # Внешнее полупрозрачное сияние
        glow_radius = int(self.radius * 2 + pulse * 6)
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        glow_alpha = int(50 + pulse * 70)
        pygame.draw.circle(
            glow_surface,
            (*VOID_CORE_GLOW_COLOR, glow_alpha),
            (glow_radius, glow_radius),
            glow_radius,
        )
        screen.blit(glow_surface, (x - glow_radius, y - glow_radius))

        # Основное тело ядра (пульсирует по размеру)
        core_radius = int(self.radius + pulse * 2)
        
        if self.image:
            scaled_image = pygame.transform.scale(self.image, (core_radius * 2, core_radius * 2))
            rect = scaled_image.get_rect(center=(x, y))
            screen.blit(scaled_image, rect)
        else:
            pygame.draw.circle(screen, VOID_CORE_COLOR, (x, y), core_radius)
            pygame.draw.circle(screen, (255, 255, 255), (x, y), max(1, int(self.radius * 0.35)))
