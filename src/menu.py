import pygame
from config import *


class MenuItem:
    """Класс элемента меню"""
    
    def __init__(self, text, action, y_position):
        self.text = text
        self.action = action
        self.y_position = y_position
        self.is_hovered = False
        
    def check_hover(self, mouse_pos, text_rect):
        """Проверка наведения мыши"""
        self.is_hovered = text_rect.collidepoint(mouse_pos)
        return self.is_hovered


class MainMenu:
    """Класс главного меню"""
    
    def __init__(self):
        """Инициализация меню"""
        self.font_title = pygame.font.Font(None, 96)
        self.font_menu = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 28)
        
        # Пункты меню
        self.menu_items = [
            MenuItem("START GAME", "start", 0),
            MenuItem("EXIT", "exit", 1),
        ]
        
        self.selected_item = None
        
    def handle_event(self, event, mouse_pos):
        """Обработка событий меню"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Клик по пункту меню
            if self.selected_item:
                return self.selected_item.action
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Enter или пробел - начать игру
                return "start"
            if event.key == pygame.K_ESCAPE:
                # ESC - выход
                return "exit"
        
        return None
    
    def update(self, mouse_pos, screen_width, screen_height):
        """Обновление состояния меню"""
        # Вычисляем позиции пунктов меню
        start_y = screen_height // 2 + 40
        spacing = 80
        
        self.selected_item = None
        
        for i, item in enumerate(self.menu_items):
            item.y_position = start_y + i * spacing
            
            # Создаем временный rect для проверки наведения
            text_surface = self.font_menu.render(item.text, True, COLOR_UI_TEXT)
            text_rect = text_surface.get_rect(center=(screen_width // 2, item.y_position))
            
            if item.check_hover(mouse_pos, text_rect):
                self.selected_item = item
    
    def render(self, screen, screen_width, screen_height):
        """Отрисовка меню"""
        # Затемненный фон
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(200)
        overlay.fill((5, 5, 15))
        screen.blit(overlay, (0, 0))
        
        # Заголовок игры
        title_text = self.font_title.render("VOID HUNTER", True, COLOR_PLAYER)
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 120))
        
        # Эффект свечения для заголовка
        glow_surface = pygame.Surface((title_rect.width + 40, title_rect.height + 40), pygame.SRCALPHA)
        for i in range(3, 0, -1):
            alpha = 30 * i
            glow_text = self.font_title.render("VOID HUNTER", True, (*COLOR_PLAYER, alpha))
            glow_rect = glow_text.get_rect(center=(glow_surface.get_width() // 2, glow_surface.get_height() // 2))
            glow_surface.blit(glow_text, glow_rect)
        
        screen.blit(glow_surface, (title_rect.x - 20, title_rect.y - 20))
        screen.blit(title_text, title_rect)
        
        # Пункты меню
        for item in self.menu_items:
            if item.is_hovered:
                # Подсвеченный пункт
                color = COLOR_PLAYER
                text_surface = self.font_menu.render(f"> {item.text} <", True, color)
            else:
                # Обычный пункт
                color = COLOR_UI_TEXT
                text_surface = self.font_menu.render(item.text, True, color)
            
            text_rect = text_surface.get_rect(center=(screen_width // 2, item.y_position))
            screen.blit(text_surface, text_rect)
        
        # Подсказки управления
        controls = [
            "CONTROLS:",
            "WASD - Move",
            "Mouse - Aim",
            "LMB / Space - Shoot",
            "Q - Void Flash (when charged)",
        ]
        
        y_offset = screen_height - 180
        for i, control in enumerate(controls):
            if i == 0:
                text_surface = self.font_small.render(control, True, COLOR_CHARGE_BAR)
            else:
                text_surface = self.font_small.render(control, True, (150, 150, 150))
            text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset + i * 28))
            screen.blit(text_surface, text_rect)
