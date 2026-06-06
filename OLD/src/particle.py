import pygame
import random
import math
from OLD.config import *


class Particle:
    """Класс частицы для визуальных эффектов"""
    
    def __init__(self, x, y, color, velocity):
        """Инициализация частицы"""
        self.position = pygame.math.Vector2(x, y)
        self.velocity = velocity
        self.color = color
        self.lifetime = PARTICLE_LIFETIME
        self.max_lifetime = PARTICLE_LIFETIME
        self.size = random.randint(2, 4)
        
    def update(self, dt):
        """Обновление частицы"""
        self.position += self.velocity * dt
        self.lifetime -= dt
        # Замедление частицы
        self.velocity *= 0.95
        
    def is_dead(self):
        """Проверка времени жизни"""
        return self.lifetime <= 0
    
    def render(self, screen):
        """Отрисовка частицы"""
        # Вычисление прозрачности на основе оставшегося времени жизни
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        
        # Создание поверхности с прозрачностью
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        particle_color = (*self.color, alpha)
        pygame.draw.circle(particle_surface, particle_color, 
                          (self.size, self.size), self.size)
        
        screen.blit(particle_surface, 
                   (self.position.x - self.size, self.position.y - self.size))


def create_explosion(x, y, color, count=PARTICLE_COUNT_EXPLOSION):
    """Создать взрыв из частиц"""
    particles = []
    for i in range(count):
        # Случайный угол
        angle = random.uniform(0, 2 * math.pi)
        # Случайная скорость
        speed = random.uniform(PARTICLE_SPEED_MIN, PARTICLE_SPEED_MAX)
        
        velocity = pygame.math.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )
        
        particle = Particle(x, y, color, velocity)
        particles.append(particle)
    
    return particles
