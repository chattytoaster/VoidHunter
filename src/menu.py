import pygame
import sys
import random

# Инициализация
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("VoidHunter")
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Шрифты
font_title = pygame.font.Font(None, 74)
font_button = pygame.font.Font(None, 36)

# Кнопки
start_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 30, 200, 50)
exit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 40, 200, 50)

start_hover = False
exit_hover = False


# Класс для движущейся звезды (слева направо)
class MovingStar:
    def __init__(self):
        self.x = random.randint(-100, screen_width)
        self.y = random.randint(0, screen_height)
        self.radius = random.randint(1, 3)
        self.speed = random.uniform(20, 60)
        self.brightness = random.randint(100, 255)
        self.twinkle_speed = random.uniform(0.3, 1)
        self.twinkle_direction = 1

    def update(self, dt):
        # Движение слева направо
        self.x += self.speed * dt

        # Мерцание
        self.brightness += self.twinkle_speed * dt * 30 * self.twinkle_direction
        if self.brightness >= 255:
            self.brightness = 255
            self.twinkle_direction = -1
        elif self.brightness <= 80:
            self.brightness = 80
            self.twinkle_direction = 1

        # Если звезда ушла за правый край, возвращаем слева
        if self.x > screen_width + 50:
            self.x = -50
            self.y = random.randint(0, screen_height)
            self.speed = random.uniform(20, 60)

    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)


# Создаем звезды (150 штук для плавного движения)
stars = [MovingStar() for _ in range(150)]

running = True
while running:
    dt = clock.tick(60) / 1000.0
    mouse_pos = pygame.mouse.get_pos()

    # Обновление звезд
    for star in stars:
        star.update(dt)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(mouse_pos):
                print("START clicked!")

            elif exit_button.collidepoint(mouse_pos):
                print("EXIT clicked!")
                running = False

    # Обновление hover
    start_hover = start_button.collidepoint(mouse_pos)
    exit_hover = exit_button.collidepoint(mouse_pos)

    # Отрисовка
    screen.fill(BLACK)

    # Рисуем звезды
    for star in stars:
        star.draw(screen)

    # Заголовок
    title = font_title.render("Void Hunter", True, WHITE)
    title_rect = title.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(title, title_rect)

    # Кнопка START
    start_color = GRAY if start_hover else WHITE
    pygame.draw.rect(screen, start_color, start_button, 2)
    start_text = font_button.render("START", True, start_color)
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)

    # Кнопка EXIT
    exit_color = GRAY if exit_hover else WHITE
    pygame.draw.rect(screen, exit_color, exit_button, 2)
    exit_text = font_button.render("EXIT", True, exit_color)
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, exit_text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
