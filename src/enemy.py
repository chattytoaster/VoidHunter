import pygame
import math
from config import (
    COLOR_DRONE, COLOR_METEORITE, 
    DRONE_SPEED, DRONE_SIZE, DRONE_HP,
    METEORITE_SPEED, METEORITE_SIZE, METEORITE_HP,
    SCREEN_WIDTH, SCREEN_HEIGHT
)

class Enemy:
    def __init__(self, x, y):
        """
        Базовый класс врага.
        
        Args:
            x (float): Начальная координата x
            y (float): Начальная координата y
        """
        self.pos = pygame.math.Vector2(x, y)
        self.hp = 1
        self.radius = 10
        self.active = True

    def take_damage(self, amount):
        """
        Уменьшение здоровья и деактивация врага, если HP <= 0.
        
        Args:
            amount (int): Количество получаемого урона
        """
        self.hp -= amount
        if self.hp <= 0:
            self.active = False

    def update(self, dt, player_pos=None):
        """
        Логика обновления, переопределяемая в дочерних классах.
        """
        pass

    def render(self, screen):
        """
        Логика отрисовки, переопределяемая в дочерних классах.
        """
        pass


class Drone(Enemy):
    def __init__(self, x, y):
        """
        Дрон — враг, который преследует игрока.
        """
        super().__init__(x, y)
        self.hp = DRONE_HP
        self.radius = DRONE_SIZE
        self.speed = DRONE_SPEED

    def update(self, dt, player_pos=None):
        """
        Обновление дрона для движения в сторону игрока.
        
        Args:
            dt (float): Дельта времени в секундах
            player_pos (tuple/Vector2): Координаты игрока (x, y)
        """
        if player_pos:
            target_vec = pygame.math.Vector2(player_pos)
            direction = target_vec - self.pos
            
            if direction.length_squared() > 0:
                # Нормализуем направление и двигаемся
                self.pos += direction.normalize() * self.speed * dt

    def render(self, screen):
        """
        Отрисовка дрона в виде ромба.
        """
        x, y = int(self.pos.x), int(self.pos.y)
        r = self.radius
        
        # Вершины ромба (верх, право, низ, лево)
        points = [
            (x, y - r),
            (x + r, y),
            (x, y + r),
            (x - r, y)
        ]
        pygame.draw.polygon(screen, COLOR_DRONE, points)


class Meteorite(Enemy):
    def __init__(self, x, y):
        """
        Метеорит — враг, который движется слева направо и отскакивает от верха/низа.
        """
        super().__init__(x, y)
        self.hp = METEORITE_HP
        self.radius = METEORITE_SIZE
        self.speed = METEORITE_SPEED
        # Направление движения по умолчанию: вправо с небольшим отклонением по вертикали
        self.vel = pygame.math.Vector2(self.speed, self.speed * 0.5)

    def update(self, dt, player_pos=None):
        """
        Обновление движения метеорита и обработка отскоков от стен.
        
        Args:
            dt (float): Дельта времени в секундах
            player_pos (tuple): Не используется, оставлен для совместимости сигнатур
        """
        self.pos += self.vel * dt
        
        # Отскок от верхнего и нижнего краев экрана
        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
            self.vel.y *= -1
        elif self.pos.y + self.radius > SCREEN_HEIGHT:
            self.pos.y = SCREEN_HEIGHT - self.radius
            self.vel.y *= -1
            
        # Деактивация, если метеорит уходит далеко за правый край экрана
        if self.pos.x > SCREEN_WIDTH + self.radius * 2:
            self.active = False

    def render(self, screen):
        """
        Отрисовка метеорита в виде простого многоугольника (неправильного восьмиугольника для "каменистого" вида).
        """
        x, y = int(self.pos.x), int(self.pos.y)
        r = self.radius
        
        # Вершины простой "каменистой" формы
        points = [
            (x - r*0.5, y - r),
            (x + r*0.5, y - r),
            (x + r, y - r*0.5),
            (x + r, y + r*0.5),
            (x + r*0.5, y + r),
            (x - r*0.5, y + r),
            (x - r, y + r*0.5),
            (x - r, y - r*0.5)
        ]
        pygame.draw.polygon(screen, COLOR_METEORITE, points)
