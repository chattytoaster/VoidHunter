import pygame
import math
from OLD.config import *


class VoidCore:
    """Класс собираемой энергетической сферы (Void Core)"""
    
    def __init__(self, x, y):
        """Инициализация Void Core"""
        self.position = pygame.math.Vector2(x, y)
        self.size = VOID_CORE_SIZE
        self.pulse_timer = 0
        self.collected = False
        
    def update(self, dt):
        """Обновление анимации пульсации"""
        self.pulse_timer += dt * 5  # Скорость пульсации
        
    def is_collected_by(self, player):
        """Проверка сбора игроком"""
        dx = player.position.x - self.position.x
        dy = player.position.y - self.position.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        return distance < (VOID_CORE_COLLECT_RANGE + player.size)
    
    def render(self, screen):
        """Отрисовка Void Core с пульсацией"""
        # Пульсирующий размер
        pulse = math.sin(self.pulse_timer) * 0.3 + 1.0  # От 0.7 до 1.3
        current_size = int(self.size * pulse)
        
        # Внешнее свечение (большой круг с прозрачностью)
        glow_surface = pygame.Surface((current_size * 6, current_size * 6), pygame.SRCALPHA)
        for i in range(3, 0, -1):
            alpha = 50 // i
            glow_color = (*COLOR_VOID_CORE, alpha)
            pygame.draw.circle(glow_surface, glow_color,
                             (current_size * 3, current_size * 3),
                             current_size * i)
        
        screen.blit(glow_surface, 
                   (self.position.x - current_size * 3, 
                    self.position.y - current_size * 3))
        
        # Основной круг
        pygame.draw.circle(screen, COLOR_VOID_CORE,
                          (int(self.position.x), int(self.position.y)),
                          current_size)
        
        # Яркое ядро
        pygame.draw.circle(screen, (255, 255, 255),
                          (int(self.position.x), int(self.position.y)),
                          max(1, current_size // 2))
