# Файл для UI (меню и интерфейс)
# Developer C должен реализовать классы Menu и UI

import pygame
from config import *


class Menu:
    """Класс главного меню"""
    
    def __init__(self):
        # TODO: создать шрифты
        pass
        
    def handle_event(self, event):
        """Обработка событий в меню"""
        # TODO: если нажат SPACE - вернуть "start"
        # TODO: если нажат ESC - вернуть "exit"
        return None
        
    def render(self, screen):
        """Отрисовка меню"""
        # TODO: нарисовать заголовок игры
        # TODO: нарисовать подсказку "Press SPACE to start"
        pass


class UI:
    """Класс игрового интерфейса"""
    
    def __init__(self):
        # TODO: создать шрифты
        pass
        
    def render(self, screen, player, score):
        """Отрисовка игрового UI"""
        # TODO: нарисовать HP игрока
        # TODO: нарисовать счет
        pass
        
    def render_game_over(self, screen, score):
        """Отрисовка экрана Game Over"""
        # TODO: нарисовать "GAME OVER"
        # TODO: нарисовать финальный счет
        # TODO: нарисовать подсказку "Press R to restart"
        pass
