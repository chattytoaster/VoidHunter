import pygame
import os
from config import BULLET_SPEED, BULLET_SIZE, COLOR_BULLET, SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_DAMAGE, IMAGE_BULLET
class Bullet:
    def __init__(self, x, y, direction_x, direction_y, charge=0):
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
        self.damage = BULLET_DAMAGE + (charge * 0.05)
        self.active = True
        
        # Загрузка спрайта пули
        self.image = None
        if os.path.exists(IMAGE_BULLET):
            try:
                self.image = pygame.image.load(IMAGE_BULLET).convert()
                self.image.set_colorkey((0, 0, 0))
                self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
            except Exception:
                pass

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
        Отрисовка пули (спрайт или простой круг).
        
        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки
        """
        if self.image:
            rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
            screen.blit(self.image, rect)
        else:
            pygame.draw.circle(
                screen, 
                COLOR_BULLET, 
                (int(self.pos.x), int(self.pos.y)), 
                self.radius
            )
