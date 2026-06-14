import pygame
import math
import os
import random
from config import (
    COLOR_DRONE, COLOR_METEORITE, 
    DRONE_SPEED, DRONE_SIZE, DRONE_HP,
    METEORITE_SPEED, METEORITE_SIZE, METEORITE_HP,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    IMAGE_DRONE, IMAGE_METEORITE
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
        self.angle = 0.0
        
        # Загрузка спрайта дрона
        self.image = None
        if os.path.exists(IMAGE_DRONE):
            try:
                self.image = pygame.image.load(IMAGE_DRONE).convert()
                self.image.set_colorkey((0, 0, 0))
                self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
            except Exception:
                pass

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
                self.angle = math.atan2(direction.y, direction.x)
                # Нормализуем направление и двигаемся
                self.pos += direction.normalize() * self.speed * dt

    def render(self, screen):
        """
        Отрисовка дрона (спрайт или векторный ромб).
        """
        if self.image:
            # Направление спрайта изначально вверх (-90 градусов корректировка)
            angle_degrees = -math.degrees(self.angle) - 90
            rotated_image = pygame.transform.rotate(self.image, angle_degrees)
            rect = rotated_image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
            screen.blit(rotated_image, rect)
        else:
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
        
        # Добавляем вращение метеорита
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(30, 90) * random.choice([-1, 1]) # скорость вращения
        
        # Загрузка спрайта метеорита
        self.image = None
        if os.path.exists(IMAGE_METEORITE):
            try:
                self.image = pygame.image.load(IMAGE_METEORITE).convert()
                self.image.set_colorkey((0, 0, 0))
                self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
            except Exception:
                pass

    def update(self, dt, player_pos=None):
        """
        Обновление движения метеорита и обработка отскоков от стен.
        
        Args:
            dt (float): Дельта времени в секундах
            player_pos (tuple): Не используется, оставлен для совместимости сигнатур
        """
        self.pos += self.vel * dt
        self.rotation += self.rotation_speed * dt
        
        # Отскок от верхнего и нижнего краев экрана
        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
            self.vel.y *= -1
            self.rotation_speed *= -1 # Меняем направление вращения при ударе
        elif self.pos.y + self.radius > SCREEN_HEIGHT:
            self.pos.y = SCREEN_HEIGHT - self.radius
            self.vel.y *= -1
            self.rotation_speed *= -1
            
        # Деактивация, если метеорит уходит далеко за правый край экрана
        if self.pos.x > SCREEN_WIDTH + self.radius * 2:
            self.active = False

    def render(self, screen):
        """
        Отрисовка метеорита (спрайт или векторный многоугольник).
        """
        if self.image:
            rotated_image = pygame.transform.rotate(self.image, self.rotation)
            rect = rotated_image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
            screen.blit(rotated_image, rect)
        else:
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
