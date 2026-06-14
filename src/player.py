import pygame
import math
from config import (
    COLOR_PLAYER, PLAYER_SPEED, PLAYER_HP, PLAYER_SIZE,
    SCREEN_WIDTH, SCREEN_HEIGHT
)

class Player:
    def __init__(self, x, y):
        """
        Инициализация игрока.
        
        Args:
            x (float): Начальная координата x
            y (float): Начальная координата y
        """
        self.pos = pygame.math.Vector2(x, y)
        self.hp = PLAYER_HP
        self.radius = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.charge_level = 0
        self.angle = 0.0  # Угол в радианах, указывает на курсор мыши

    def update(self, keys, mouse_pos, dt):
        """
        Обновление позиции игрока на основе нажатых клавиш, вращения к мыши,
        а также обработка логики стрельбы.
        
        Args:
            keys (sequence): Состояние всех клавиш клавиатуры от pygame.key.get_pressed()
            mouse_pos (tuple): (x, y) координаты мыши
            dt (float): Дельта времени в секундах
            
        Returns:
            bool: True если игрок хочет стрелять, иначе False
        """
        # --- Логика движения (WASD) ---
        movement = pygame.math.Vector2(0, 0)
        
        if keys[pygame.K_w]:
            movement.y -= 1
        if keys[pygame.K_s]:
            movement.y += 1
        if keys[pygame.K_a]:
            movement.x -= 1
        if keys[pygame.K_d]:
            movement.x += 1
            
        # Нормализуем движение по диагонали, чтобы скорость не превышала PLAYER_SPEED
        if movement.length_squared() > 0:
            movement = movement.normalize()
            
        self.pos += movement * self.speed * dt
        
        # Ограничиваем движение границами экрана
        self.pos.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.pos.x))
        self.pos.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.pos.y))
        
        # --- Логика вращения ---
        mouse_vec = pygame.math.Vector2(mouse_pos)
        direction_vec = mouse_vec - self.pos
        self.angle = math.atan2(direction_vec.y, direction_vec.x)
        
        # --- Логика стрельбы ---
        # Возвращает True, если нажат ПРОБЕЛ или левая кнопка мыши
        mouse_buttons = pygame.mouse.get_pressed()
        is_shooting = keys[pygame.K_SPACE] or mouse_buttons[0]
        
        return is_shooting

    def take_damage(self, amount):
        """
        Уменьшение здоровья (HP) игрока.
        
        Args:
            amount (int): Количество получаемого урона
        """
        self.hp -= amount
        
    def add_charge(self, amount=1):
        """
        Увеличение уровня заряда (VoidCore).
        
        Args:
            amount (int): Количество добавляемого заряда
        """
        self.charge_level += amount

    def render(self, screen):
        """
        Отрисовка игрока в виде треугольника, направленного в сторону мыши.
        
        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки
        """
        # Вычисление вершин треугольника на основе угла
        # Нос корабля
        p1_x = self.pos.x + math.cos(self.angle) * self.radius * 1.5
        p1_y = self.pos.y + math.sin(self.angle) * self.radius * 1.5
        
        # Левый нижний угол
        p2_x = self.pos.x + math.cos(self.angle + 2.5) * self.radius
        p2_y = self.pos.y + math.sin(self.angle + 2.5) * self.radius
        
        # Правый нижний угол
        p3_x = self.pos.x + math.cos(self.angle - 2.5) * self.radius
        p3_y = self.pos.y + math.sin(self.angle - 2.5) * self.radius
        
        points = [(p1_x, p1_y), (p2_x, p2_y), (p3_x, p3_y)]
        
        pygame.draw.polygon(screen, COLOR_PLAYER, points)