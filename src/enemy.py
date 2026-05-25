import pygame
import random
import math
from config import *
from src.utils import draw_glow_circle, draw_glow_polygon


class Enemy:
    """Базовый класс врага"""
    
    def __init__(self, x, y, hp, speed, size, damage, score, enemy_type):
        """Инициализация врага"""
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.size = size
        self.damage = damage
        self.score = score
        self.type = enemy_type
        
    def update(self, dt, player_pos, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Обновление состояния врага (переопределяется в подклассах)"""
        pass
    
    def take_damage(self, amount):
        """Получение урона"""
        self.hp -= amount
        
    def is_dead(self):
        """Проверка смерти"""
        return self.hp <= 0
    
    def render(self, screen):
        """Отрисовка врага (переопределяется в подклассах)"""
        pass


class Asteroid(Enemy):
    """Астероид - медленный, прочный враг"""
    
    def __init__(self, x, y):
        super().__init__(x, y, ASTEROID_HP, ASTEROID_SPEED, ASTEROID_SIZE, 
                        ASTEROID_DAMAGE, ASTEROID_SCORE, "asteroid")
        
        # Случайное направление движения
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.math.Vector2(
            math.cos(angle) * self.speed,
            math.sin(angle) * self.speed
        )
        
        # Случайная скорость вращения для визуала
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)
        
        # Количество вершин для многоугольника (6-8)
        self.num_vertices = random.randint(6, 8)
        
    def update(self, dt, player_pos, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Обновление астероида"""
        # Движение в случайном направлении
        self.position += self.velocity * dt
        
        # Отскок от границ экрана
        if self.position.x < 0 or self.position.x > screen_width:
            self.velocity.x *= -1
        if self.position.y < 0 or self.position.y > screen_height:
            self.velocity.y *= -1
        
        # Вращение
        self.rotation += self.rotation_speed * dt
        
    def render(self, screen):
        """Отрисовка астероида"""
        # Рисуем многоугольник (имитация астероида)
        points = []
        for i in range(self.num_vertices):
            angle = (2 * math.pi / self.num_vertices) * i + self.rotation
            # Небольшая вариация радиуса для неровности
            radius = self.size * random.uniform(0.8, 1.0)
            x = self.position.x + math.cos(angle) * radius
            y = self.position.y + math.sin(angle) * radius
            points.append((x, y))
        
        draw_glow_polygon(screen, COLOR_ASTEROID, points, alpha=80)


class Drone(Enemy):
    """Дрон - быстрый враг, преследующий игрока"""
    
    def __init__(self, x, y):
        super().__init__(x, y, DRONE_HP, DRONE_SPEED, DRONE_SIZE, 
                        DRONE_DAMAGE, DRONE_SCORE, "drone")
        
    def update(self, dt, player_pos, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Обновление дрона"""
        # Вычисление расстояния до игрока
        dx = player_pos[0] - self.position.x
        dy = player_pos[1] - self.position.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Преследование игрока если в радиусе
        if distance < DRONE_CHASE_RANGE and distance > 0:
            # Нормализация направления
            self.velocity.x = (dx / distance) * self.speed
            self.velocity.y = (dy / distance) * self.speed
        else:
            # Замедление если далеко
            self.velocity *= 0.95
        
        # Обновление позиции
        self.position += self.velocity * dt
        
    def render(self, screen):
        """Отрисовка дрона"""
        # Рисуем ромб (квадрат повернутый на 45 градусов)
        points = [
            (self.position.x, self.position.y - self.size),  # Верх
            (self.position.x + self.size, self.position.y),  # Право
            (self.position.x, self.position.y + self.size),  # Низ
            (self.position.x - self.size, self.position.y),  # Лево
        ]
        
        draw_glow_polygon(screen, COLOR_DRONE, points, alpha=120)
        
        # Маленький круг в центре (ядро дрона)
        draw_glow_circle(screen, COLOR_DRONE, 
                        (int(self.position.x), int(self.position.y)), 
                        self.size // 3, alpha=150)
