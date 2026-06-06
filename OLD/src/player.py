import pygame
import math
from OLD.config import *
from OLD.src.utils import draw_glow_polygon


class Player:
    """Класс игрока - управляемый космический корабль"""
    
    def __init__(self, x, y):
        """Инициализация игрока"""
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.angle = 0  # Угол поворота к мыши (в радианах)
        
        # Характеристики
        self.hp = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.size = PLAYER_SIZE
        
        # Система заряда Void Cores
        self.charge_level = 0
        self.cores_collected = 0
        
        # Таймеры
        self.shoot_cooldown = 0
        self.invulnerability_timer = 0
        
    def update(self, dt, keys, mouse_pos, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Обновление состояния игрока"""
        # Обновление таймеров
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= dt
        
        # Управление движением (WASD)
        acceleration = pygame.math.Vector2(0, 0)
        
        if keys[pygame.K_w]:
            acceleration.y -= PLAYER_ACCELERATION
        if keys[pygame.K_s]:
            acceleration.y += PLAYER_ACCELERATION
        if keys[pygame.K_a]:
            acceleration.x -= PLAYER_ACCELERATION
        if keys[pygame.K_d]:
            acceleration.x += PLAYER_ACCELERATION
        
        # Применение ускорения
        self.velocity += acceleration * dt
        
        # Применение трения (damping)
        self.velocity *= PLAYER_DAMPING
        
        # Ограничение максимальной скорости
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)
        
        # Обновление позиции
        self.position += self.velocity * dt
        
        # Ограничение границами экрана
        self.position.x = max(self.size, min(screen_width - self.size, self.position.x))
        self.position.y = max(self.size, min(screen_height - self.size, self.position.y))
        
        # Поворот к мыши (сохраняем угол для стрельбы)
        dx = mouse_pos[0] - self.position.x
        dy = mouse_pos[1] - self.position.y
        self.angle = math.atan2(dy, dx)
    
    def shoot(self, mouse_pos):
        """Попытка выстрела (возвращает True если выстрел произошел)"""
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = FIRE_RATE / (1 + self.charge_level * CHARGE_FIRE_RATE_BONUS)
            return True
        return False
    
    def take_damage(self, amount):
        """Получение урона"""
        if self.invulnerability_timer <= 0:
            self.hp -= amount
            self.invulnerability_timer = PLAYER_INVULNERABILITY_TIME
            return True
        return False
    
    def is_invulnerable(self):
        """Проверка неуязвимости"""
        return self.invulnerability_timer > 0
    
    def is_dead(self):
        """Проверка смерти"""
        return self.hp <= 0
    
    def collect_void_core(self):
        """Сбор Void Core"""
        self.cores_collected += 1
        
        # Проверка повышения уровня заряда
        if self.charge_level < VOID_CORE_MAX_LEVEL:
            if self.cores_collected >= VOID_CORES_PER_LEVEL[self.charge_level + 1]:
                self.charge_level += 1
                # Сбрасываем счетчик для следующего уровня
                self.cores_collected = 0
    
    def activate_void_flash(self):
        """Активация способности Void Flash"""
        if self.charge_level > 0:
            current_level = self.charge_level
            self.charge_level = 0
            self.cores_collected = 0  # Сбрасываем и счетчик ядер
            return current_level  # Возвращаем уровень заряда для расчета урона
        return 0
    
    def get_damage_multiplier(self):
        """Получить множитель урона от заряда"""
        return 1.0 + (self.charge_level * CHARGE_DAMAGE_BONUS)
    
    def render(self, screen):
        """Отрисовка игрока"""
        # Треугольник, направленный вправо
        points = [
            (self.position.x + self.size, self.position.y),  # Нос (вправо)
            (self.position.x - self.size * 0.7, self.position.y - self.size * 0.7),
            (self.position.x - self.size * 0.7, self.position.y + self.size * 0.7),
        ]
        
        # Мигание при неуязвимости
        if self.is_invulnerable():
            # Мигание каждые 0.1 секунды
            if int(self.invulnerability_timer * 10) % 2 == 0:
                draw_glow_polygon(screen, COLOR_PLAYER, points, alpha=100)
        else:
            draw_glow_polygon(screen, COLOR_PLAYER, points, alpha=100)
