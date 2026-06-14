import math
import pygame

def circle_collision(pos1, radius1, pos2, radius2):
    """
    Проверка коллизии двух кругов с использованием pygame.math.Vector2
    или обычных кортежей.
    
    Args:
        pos1 (tuple/Vector2): Координаты (x, y) центра первого круга
        radius1 (float): Радиус первого круга
        pos2 (tuple/Vector2): Координаты (x, y) центра второго круга
        radius2 (float): Радиус второго круга
        
    Returns:
        bool: True если круги сталкиваются, иначе False
    """
    # Конвертируем координаты в Vector2 для универсальности
    v1 = pygame.math.Vector2(pos1)
    v2 = pygame.math.Vector2(pos2)
    
    # Сравниваем квадрат дистанции с квадратом суммы радиусов 
    # для оптимизации (без вычисления квадратного корня)
    return v1.distance_squared_to(v2) <= (radius1 + radius2) ** 2
