import pygame
import math
from OLD.config import *
from OLD.src.utils import draw_glow_circle


class Bullet:
    """Класс пули игрока"""
    
    def __init__(self, x, y, target_x, target_y, damage):
        """Инициализация пули"""
        self.position = pygame.math.Vector2(x, y)
        
        # Вычисление направления к цели
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            # Нормализация и умножение на скорость
            self.velocity = pygame.math.Vector2(
                (dx / distance) * BULLET_SPEED,
                (dy / distance) * BULLET_SPEED
            )
        else:
            self.velocity = pygame.math.Vector2(0, -BULLET_SPEED)
        
        self.damage = damage
        self.size = BULLET_SIZE
        self.lifetime = BULLET_LIFETIME
        
    def update(self, dt):
        """Обновление позиции пули"""
        self.position += self.velocity * dt
        self.lifetime -= dt
    
    def is_off_screen(self, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Проверка выхода за границы экрана"""
        return (self.position.x < -50 or self.position.x > screen_width + 50 or
                self.position.y < -50 or self.position.y > screen_height + 50)
    
    def is_expired(self):
        """Проверка истечения времени жизни"""
        return self.lifetime <= 0
    
    def render(self, screen):
        """Отрисовка пули"""
        draw_glow_circle(screen, COLOR_BULLET, 
                        (int(self.position.x), int(self.position.y)), 
                        self.size, alpha=150)
