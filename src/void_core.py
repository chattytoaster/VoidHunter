# Файл для VoidCore класса

import pygame
import math
import config


# Опциональные настройки (если их нет в config.py - используются значения по умолчанию)
VOID_CORE_SIZE = getattr(config, "VOID_CORE_SIZE", 8)
VOID_CORE_PICKUP_RADIUS = getattr(config, "VOID_CORE_PICKUP_RADIUS", VOID_CORE_SIZE + 15)
VOID_CORE_COLOR = getattr(config, "COLOR_VOID_CORE", (170, 80, 255))
VOID_CORE_GLOW_COLOR = getattr(config, "COLOR_VOID_CORE_GLOW", (220, 170, 255))
VOID_CORE_PULSE_SPEED = getattr(config, "VOID_CORE_PULSE_SPEED", 4.0)


class VoidCore:
    """Класс собираемого ядра (Void Core)"""

    def __init__(self, x, y):
        """
        Args:
            x (float): x координата появления
            y (float): y координата появления
        """
        self.pos = [x, y]
        self.radius = VOID_CORE_SIZE
        self.pickup_radius = VOID_CORE_PICKUP_RADIUS
        self.timer = 0.0
        self.active = True

    def update(self, dt):
        """
        Обновление таймера анимации пульсации.

        Args:
            dt (float): Delta time в секундах
        """
        self.timer += dt

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

    def render(self, screen):
        """
        Отрисовка пульсирующего ядра с эффектом сияния.

        Args:
            screen (pygame.Surface): поверхность экрана
        """
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
        pygame.draw.circle(screen, VOID_CORE_COLOR, (x, y), core_radius)

        # Яркий центр
        pygame.draw.circle(screen, (255, 255, 255), (x, y), max(1, int(self.radius * 0.35)))
