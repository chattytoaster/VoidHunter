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


class Meteorite(Enemy):
    """Метеорит - прочный и не преследует игрока"""

    def __init__(self, x, y):
        super().__init__(x, y, METEORITE_HP, METEORITE_SPEED, METEORITE_SIZE,
                         METEORITE_DAMAGE, METEORITE_SCORE, "meteorite")
        # Летит справа налево с небольшим вертикальным дрейфом
        drift_y = random.uniform(-0.22, 0.22) * self.speed
        self.velocity = pygame.math.Vector2(-self.speed, drift_y)
        self.rotation = 0
        self.rotation_speed = random.uniform(-1.5, 1.5)
        self.num_vertices = random.randint(8, 11)

    def update(self, dt, player_pos, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        self.position += self.velocity * dt
        # Легкий вертикальный отскок только по Y, без разворота по X
        if self.position.y < 0 or self.position.y > screen_height:
            self.velocity.y *= -1
        self.rotation += self.rotation_speed * dt

    def render(self, screen):
        points = []
        for i in range(self.num_vertices):
            angle = (2 * math.pi / self.num_vertices) * i + self.rotation
            radius = self.size * random.uniform(0.82, 1.0)
            points.append((
                self.position.x + math.cos(angle) * radius,
                self.position.y + math.sin(angle) * radius,
            ))
        draw_glow_polygon(screen, COLOR_METEORITE, points, alpha=70)


class EnemyBullet:
    def __init__(self, x, y, target_x, target_y):
        self.position = pygame.math.Vector2(x, y)
        direction = pygame.math.Vector2(target_x - x, target_y - y)
        if direction.length_squared() > 0:
            direction = direction.normalize()
        else:
            direction = pygame.math.Vector2(-1, 0)
        self.velocity = direction * ENEMY_BULLET_SPEED
        self.size = ENEMY_BULLET_SIZE
        self.damage = ENEMY_BULLET_DAMAGE
        self.lifetime = 3.0

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt

    def is_dead(self, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        if self.lifetime <= 0:
            return True
        return (
            self.position.x < -60 or self.position.x > screen_width + 60 or
            self.position.y < -60 or self.position.y > screen_height + 60
        )

    def render(self, screen):
        draw_glow_circle(
            screen,
            COLOR_ENEMY_BULLET,
            (int(self.position.x), int(self.position.y)),
            self.size,
            alpha=130,
        )


class Gunship(Enemy):
    """Редкий стреляющий корабль"""

    def __init__(self, x, y):
        super().__init__(x, y, GUNSHIP_HP, GUNSHIP_SPEED, GUNSHIP_SIZE,
                         GUNSHIP_DAMAGE, GUNSHIP_SCORE, "gunship")
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * self.speed
        self.fire_cooldown = random.uniform(0.4, GUNSHIP_FIRE_COOLDOWN)

    def update(self, dt, player_pos, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        self.position += self.velocity * dt
        if self.position.x < 0 or self.position.x > screen_width:
            self.velocity.x *= -1
        if self.position.y < 0 or self.position.y > screen_height:
            self.velocity.y *= -1
        self.fire_cooldown -= dt

    def try_shoot(self, player_pos):
        if self.fire_cooldown <= 0:
            self.fire_cooldown = GUNSHIP_FIRE_COOLDOWN
            return EnemyBullet(self.position.x, self.position.y, player_pos[0], player_pos[1])
        return None

    def render(self, screen):
        points = [
            (self.position.x + self.size, self.position.y),
            (self.position.x, self.position.y - self.size * 0.7),
            (self.position.x - self.size, self.position.y),
            (self.position.x, self.position.y + self.size * 0.7),
        ]
        draw_glow_polygon(screen, COLOR_GUNSHIP, points, alpha=110)
        draw_glow_circle(
            screen,
            COLOR_GUNSHIP,
            (int(self.position.x), int(self.position.y)),
            max(3, self.size // 4),
            alpha=120,
        )
