import pygame
from config import BULLET_SPEED, BULLET_SIZE, COLOR_BULLET, SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_DAMAGE

class Bullet:
    def __init__(self, x, y, direction_x, direction_y):
        """
        Инициализация пули.
        
        Args:
            x (float): Начальная координата x
            y (float): Начальная координата y
            direction_x (float): Компонент x нормализованного вектора направления
            direction_y (float): Компонент y нормализованного вектора направления
        """
        self.pos = pygame.math.Vector2(x, y)
        self.dir = pygame.math.Vector2(direction_x, direction_y)
        
        # Убеждаемся, что направление нормализовано
        if self.dir.length_squared() > 0:
            self.dir = self.dir.normalize()
            
        self.speed = BULLET_SPEED
        self.radius = BULLET_SIZE
        self.damage = BULLET_DAMAGE
        self.active = True

    def update(self, dt):
        """
        Обновление позиции пули.
        
        Args:
            dt (float): Дельта времени в секундах
        """
        # Движение в заданном направлении
        self.pos += self.dir * self.speed * dt
        
        # Проверка выхода пули за границы экрана
        if (self.pos.x < 0 or self.pos.x > SCREEN_WIDTH or
            self.pos.y < 0 or self.pos.y > SCREEN_HEIGHT):
            self.active = False

    def render(self, screen):
        """
        Отрисовка пули в виде простого круга.
        
        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки
        """
        pygame.draw.circle(
            screen, 
            COLOR_BULLET, 
            (int(self.pos.x), int(self.pos.y)), 
            self.radius
        )
