import pygame
import math


def circle_collision(pos1, radius1, pos2, radius2):
    """Проверка столкновения двух кругов"""
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    distance = math.sqrt(dx * dx + dy * dy)
    return distance < (radius1 + radius2)


def draw_glow_circle(surface, color, pos, radius, alpha=128):
    """Рисование круга со свечением"""
    glow_surface = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
    
    # Рисуем 3 слоя свечения
    for i in range(3, 0, -1):
        glow_alpha = alpha // (4 - i)
        pygame.draw.circle(glow_surface, (*color, glow_alpha), 
                          (radius * 2, radius * 2), radius * i)
    
    # Основной круг
    pygame.draw.circle(glow_surface, color, (radius * 2, radius * 2), radius)
    surface.blit(glow_surface, (pos[0] - radius * 2, pos[1] - radius * 2))


def draw_glow_polygon(surface, color, points, alpha=128):
    """Рисование многоугольника со свечением"""
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    
    width = int(max_x - min_x + 40)
    height = int(max_y - min_y + 40)
    glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Смещаем точки
    offset_points = [(p[0] - min_x + 20, p[1] - min_y + 20) for p in points]
    
    # Рисуем 3 слоя свечения
    center_x = sum(p[0] for p in offset_points) / len(offset_points)
    center_y = sum(p[1] for p in offset_points) / len(offset_points)
    
    for i in range(3, 0, -1):
        glow_alpha = alpha // (4 - i)
        scale = 1 + (i * 0.1)
        scaled_points = [(center_x + (p[0] - center_x) * scale,
                         center_y + (p[1] - center_y) * scale)
                        for p in offset_points]
        pygame.draw.polygon(glow_surface, (*color, glow_alpha), scaled_points)
    
    # Основной многоугольник
    pygame.draw.polygon(glow_surface, color, offset_points)
    surface.blit(glow_surface, (min_x - 20, min_y - 20))
