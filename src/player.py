import pygame
import math
import os
from config import (
    COLOR_PLAYER, PLAYER_SPEED, PLAYER_HP, PLAYER_SIZE,
    PLAYER_SHOOT_COOLDOWN, SCREEN_WIDTH, SCREEN_HEIGHT,
    IMAGE_PLAYER
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
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        self.shoot_timer = 0.0
        
        # Загрузка спрайта игрока
        self.image = None
        if os.path.exists(IMAGE_PLAYER):
            try:
                self.image = pygame.image.load(IMAGE_PLAYER).convert()
                self.image.set_colorkey((0, 0, 0))
                # Масштабируем спрайт до размера игрока
                self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
            except Exception:
                pass

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
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
            
        mouse_buttons = pygame.mouse.get_pressed()
        is_shooting = keys[pygame.K_SPACE] or mouse_buttons[0]
        
        can_shoot = is_shooting and self.shoot_timer <= 0
        if can_shoot:
            self.shoot_timer = self.shoot_cooldown
        
        return can_shoot

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
        Отрисовка игрока (спрайт или векторный треугольник).
        
        Args:
            screen (pygame.Surface): Поверхность экрана для отрисовки
        """
        if self.image:
            # pygame.transform.rotate поворачивает против часовой стрелки, поэтому преобразуем угол
            # и вычитаем 90 градусов, так как спрайт изначально направлен вверх
            angle_degrees = -math.degrees(self.angle) - 90
            rotated_image = pygame.transform.rotate(self.image, angle_degrees)
            rect = rotated_image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
            screen.blit(rotated_image, rect)
        else:
            # Резервная отрисовка треугольника
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

    def shoot(self, target_x, target_y):
        """
        Создание пули, направленной в сторону цели.
        
        Args:
            target_x (float): Координата x цели
            target_y (float): Координата y цели
            
        Returns:
            Bullet: Объект пули
        """
        from src.projectile import Bullet
        
        target = pygame.math.Vector2(target_x, target_y)
        direction = target - self.pos
        
        if direction.length_squared() > 0:
            direction = direction.normalize()
        else:
            direction = pygame.math.Vector2(math.cos(self.angle), math.sin(self.angle))
            
        # Спавним пулю на носу корабля
        spawn_pos = self.pos + direction * self.radius * 1.5
        
        return Bullet(spawn_pos.x, spawn_pos.y, direction.x, direction.y, self.charge_level)