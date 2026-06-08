import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class MovingStar:
    """Класс для движущейся звезды"""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(-100, screen_width)
        self.y = random.randint(0, screen_height)
        self.radius = random.randint(1, 3)
        self.speed = random.uniform(20, 60)
        self.brightness = random.randint(100, 255)
        self.twinkle_speed = random.uniform(0.3, 1)
        self.twinkle_direction = 1

    def update(self, dt):
        self.x += self.speed * dt
        self.brightness += self.twinkle_speed * dt * 30 * self.twinkle_direction
        if self.brightness >= 255:
            self.brightness = 255
            self.twinkle_direction = -1
        elif self.brightness <= 80:
            self.brightness = 80
            self.twinkle_direction = 1
        if self.x > self.screen_width + 50:
            self.x = -50
            self.y = random.randint(0, self.screen_height)
            self.speed = random.uniform(20, 60)

    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)


class Menu:
    """Класс главного меню"""
    
    def __init__(self):
        self.font_title = pygame.font.Font(None, 74)
        self.font_button = pygame.font.Font(None, 36)
        
        self.white = (255, 255, 255)
        self.gray = (150, 150, 150)
        
        self.start_hover = False
        self.exit_hover = False
        
        # Используем константы из config
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        
        # Создаем звезды сразу
        self.stars = [MovingStar(self.screen_width, self.screen_height) for _ in range(150)]
        
        # Создаем кнопки
        self.start_button = pygame.Rect(
            self.screen_width // 2 - 100, 
            self.screen_height // 2 - 30, 
            200, 50
        )
        self.exit_button = pygame.Rect(
            self.screen_width // 2 - 100, 
            self.screen_height // 2 + 40, 
            200, 50
        )
    
    def update_stars(self, dt):
        """Обновление звезд"""
        for star in self.stars:
            star.update(dt)
    
    def handle_event(self, event, mouse_pos):
        """Обработка событий в меню"""
        # Обновляем hover при движении мыши
        if event.type == pygame.MOUSEMOTION:
            self.start_hover = self.start_button.collidepoint(mouse_pos)
            self.exit_hover = self.exit_button.collidepoint(mouse_pos)
        
        # Обработка клика
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(mouse_pos):
                return "start"
            elif self.exit_button.collidepoint(mouse_pos):
                return "exit"
        
        # Обработка клавиш
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return "start"
            elif event.key == pygame.K_ESCAPE:
                return "exit"
        
        return None
        
    def render(self, screen):
        """Отрисовка меню"""
        # Рисуем звезды
        for star in self.stars:
            star.draw(screen)
        
        # Заголовок
        title = self.font_title.render("VOID HUNTER", True, self.white)
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        screen.blit(title, title_rect)
        
        # Кнопка START
        start_color = self.gray if self.start_hover else self.white
        pygame.draw.rect(screen, start_color, self.start_button, 2)
        start_text = self.font_button.render("START", True, start_color)
        start_text_rect = start_text.get_rect(center=self.start_button.center)
        screen.blit(start_text, start_text_rect)
        
        # Кнопка EXIT
        exit_color = self.gray if self.exit_hover else self.white
        pygame.draw.rect(screen, exit_color, self.exit_button, 2)
        exit_text = self.font_button.render("EXIT", True, exit_color)
        exit_text_rect = exit_text.get_rect(center=self.exit_button.center)
        screen.blit(exit_text, exit_text_rect)
        
        # Подсказка
        hint = self.font_button.render("Press SPACE to start", True, self.gray)
        hint_rect = hint.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        screen.blit(hint, hint_rect)
