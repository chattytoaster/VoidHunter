# Файл для UI (меню и интерфейс)

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


# Файл для UI (меню и интерфейс)

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
        # Шрифты
        self.font_title = pygame.font.Font(None, 74)
        self.font_button = pygame.font.Font(None, 42)

        # Цвета
        self.white = (255, 255, 255)
        self.gray = (120, 120, 120)
        self.yellow = (255, 255, 100)  # Цвет при наведении
        self.blue = (100, 150, 255)  # Альтернативный цвет для кнопки Exit

        # Размеры экрана из config
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        # Размеры кнопок
        button_width = 220
        button_height = 55

        # Кнопка START
        self.start_button = pygame.Rect(
            self.screen_width // 2 - button_width // 2,
            self.screen_height // 2 - 30,
            button_width, button_height
        )

        # Кнопка EXIT
        self.exit_button = pygame.Rect(
            self.screen_width // 2 - button_width // 2,
            self.screen_height // 2 + 50,
            button_width, button_height
        )

        # Состояния кнопок (цвета по умолчанию)
        self.start_color = self.white
        self.exit_color = self.white
        self.start_hover = False
        self.exit_hover = False

        # Создаем звезды
        self.stars = [MovingStar(self.screen_width, self.screen_height) for _ in range(150)]

    def update(self, dt):
        """Обновление меню (звезды)"""
        for star in self.stars:
            star.update(dt)

    def handle_event(self, event, mouse_pos):
        """Обработка событий в меню"""
        # Обновляем состояние при движении мыши
        if event.type == pygame.MOUSEMOTION:
            # Проверяем наведение на START
            if self.start_button.collidepoint(mouse_pos):
                if not self.start_hover:
                    self.start_hover = True
                    self.start_color = self.yellow
            else:
                if self.start_hover:
                    self.start_hover = False
                    self.start_color = self.white

            # Проверяем наведение на EXIT
            if self.exit_button.collidepoint(mouse_pos):
                if not self.exit_hover:
                    self.exit_hover = True
                    self.exit_color = self.yellow
            else:
                if self.exit_hover:
                    self.exit_hover = False
                    self.exit_color = self.white

            return None

        # Обработка клика мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(mouse_pos):
                return "start"
            elif self.exit_button.collidepoint(mouse_pos):
                return "exit"

        # Убираем запуск по пробелу (теперь только кнопка)
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         return "start"
        #     elif event.key == pygame.K_ESCAPE:
        #         return "exit"

        return None

    def render(self, screen):
        """Отрисовка меню"""
        # 1. Рисуем звезды
        for star in self.stars:
            star.draw(screen)

        # 2. Заголовок
        title = self.font_title.render("VOID HUNTER", True, self.white)
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        screen.blit(title, title_rect)

        # 3. Кнопка START
        # Рисуем рамку кнопки
        pygame.draw.rect(screen, self.start_color, self.start_button, 3)
        # Рисуем текст
        start_text = self.font_button.render("START", True, self.start_color)
        start_text_rect = start_text.get_rect(center=self.start_button.center)
        screen.blit(start_text, start_text_rect)

        # 4. Кнопка EXIT
        pygame.draw.rect(screen, self.exit_color, self.exit_button, 3)
        exit_text = self.font_button.render("EXIT", True, self.exit_color)
        exit_text_rect = exit_text.get_rect(center=self.exit_button.center)
        screen.blit(exit_text, exit_text_rect)

        # 5. Подсказка (теперь просто управление)
        hint = pygame.font.Font(None, 28).render("Click START to begin", True, self.gray)
        hint_rect = hint.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        screen.blit(hint, hint_rect)


class UI:
    """Класс игрового интерфейса"""

    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)

    def render(self, screen, player, score):
        if player:
            hp_text = self.font.render(f"HP: {player.hp}", True, self.white)
            screen.blit(hp_text, (20, 20))

            charge_text = self.font.render(f"Charge: {player.charge_level}", True, self.white)
            screen.blit(charge_text, (20, 50))

        score_text = self.font.render(f"Score: {score}", True, self.white)
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        screen.blit(score_text, score_rect)

    def render_game_over(self, screen, score):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        game_over_text = self.font_large.render("GAME OVER", True, self.red)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        score_text = self.font.render(f"Final Score: {score}", True, self.white)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(score_text, score_rect)

        restart_text = self.font.render("Press R to restart", True, self.white)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(restart_text, restart_rect)
