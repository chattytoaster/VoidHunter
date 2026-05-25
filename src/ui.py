import pygame
from config import *


class HUD:
    """Класс для отображения пользовательского интерфейса"""
    
    def __init__(self):
        """Инициализация HUD"""
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.font_large = pygame.font.Font(None, UI_FONT_SIZE_LARGE)
        
    def render(self, screen, player, score, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Отрисовка всего UI"""
        self.render_hp(screen, player.hp, player.max_hp)
        self.render_score(screen, score, screen_width)
        self.render_charge_bar(screen, player.charge_level, player.cores_collected, screen_height)
        
    def render_hp(self, screen, hp, max_hp):
        """Отрисовка HP (сердечки)"""
        x = UI_MARGIN
        y = UI_MARGIN
        
        for i in range(max_hp):
            # Цвет сердца в зависимости от HP
            if i < hp:
                color = COLOR_HP_FULL
            else:
                color = (50, 50, 50)  # Темно-серый для потерянных HP
            
            # Рисуем простое сердце (два круга + треугольник)
            heart_size = HP_ICON_SIZE
            
            # Левый круг
            pygame.draw.circle(screen, color, 
                             (x + heart_size // 3, y + heart_size // 3), 
                             heart_size // 3)
            # Правый круг
            pygame.draw.circle(screen, color, 
                             (x + 2 * heart_size // 3, y + heart_size // 3), 
                             heart_size // 3)
            # Треугольник снизу
            points = [
                (x, y + heart_size // 3),
                (x + heart_size, y + heart_size // 3),
                (x + heart_size // 2, y + heart_size)
            ]
            pygame.draw.polygon(screen, color, points)
            
            x += heart_size + 10
    
    def render_score(self, screen, score, screen_width=SCREEN_WIDTH):
        """Отрисовка счета"""
        score_text = f"SCORE: {score}"
        text_surface = self.font.render(score_text, True, COLOR_UI_TEXT)
        
        # Позиция в правом верхнем углу
        x = screen_width - text_surface.get_width() - UI_MARGIN
        y = UI_MARGIN
        
        screen.blit(text_surface, (x, y))
    
    def render_charge_bar(self, screen, charge_level, cores_collected, screen_height=SCREEN_HEIGHT):
        """Отрисовка полосы заряда Void Cores"""
        x = UI_MARGIN
        y = screen_height - UI_MARGIN - CHARGE_BAR_HEIGHT - 40
        
        # Текст уровня заряда
        charge_text = f"VOID CHARGE: LVL {charge_level}/{VOID_CORE_MAX_LEVEL}"
        text_surface = self.font.render(charge_text, True, COLOR_UI_TEXT)
        screen.blit(text_surface, (x, y))
        
        # Полоса заряда
        bar_y = y + 30
        
        # Фон полосы
        pygame.draw.rect(screen, (50, 50, 50), 
                        (x, bar_y, CHARGE_BAR_WIDTH, CHARGE_BAR_HEIGHT))
        
        # Заполнение полосы
        if charge_level < VOID_CORE_MAX_LEVEL:
            # Прогресс до следующего уровня (от 0 до нужного количества)
            cores_needed = VOID_CORES_PER_LEVEL[charge_level + 1] - VOID_CORES_PER_LEVEL[charge_level]
            progress = cores_collected / cores_needed
            fill_width = int(CHARGE_BAR_WIDTH * min(progress, 1.0))
        else:
            # Максимальный уровень
            fill_width = CHARGE_BAR_WIDTH
        
        if fill_width > 0:
            # Градиент от фиолетового к яркому
            for i in range(fill_width):
                intensity = int(150 + (i / max(fill_width, 1)) * 105)
                color = (intensity, 0, 255)
                pygame.draw.line(screen, color, 
                               (x + i, bar_y), 
                               (x + i, bar_y + CHARGE_BAR_HEIGHT))
        
        # Обводка полосы
        pygame.draw.rect(screen, COLOR_CHARGE_BAR, 
                        (x, bar_y, CHARGE_BAR_WIDTH, CHARGE_BAR_HEIGHT), 2)
        
        # Подсказка о способности
        if charge_level > 0:
            hint_text = "Press Q for VOID FLASH"
            hint_surface = self.font.render(hint_text, True, COLOR_CHARGE_BAR)
            screen.blit(hint_surface, (x + CHARGE_BAR_WIDTH + 20, bar_y))
    
    def render_game_over(self, screen, final_score, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Отрисовка экрана Game Over"""
        # Затемнение фона
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Текст GAME OVER
        game_over_text = self.font_large.render("GAME OVER", True, COLOR_UI_TEXT)
        text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 80))
        screen.blit(game_over_text, text_rect)
        
        # Финальный счет
        score_text = self.font.render(f"Final Score: {final_score}", True, COLOR_UI_TEXT)
        score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 - 20))
        screen.blit(score_text, score_rect)
        
        # Подсказка перезапуска
        restart_text = self.font.render("Press R to Restart", True, COLOR_UI_TEXT)
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 40))
        screen.blit(restart_text, restart_rect)
        
        # Подсказка выхода
        exit_text = self.font.render("Press ESC to Exit", True, (150, 150, 150))
        exit_rect = exit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 80))
        screen.blit(exit_text, exit_rect)
