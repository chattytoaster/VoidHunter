import pygame
import sys
import random
import math
from config import *

from src.player import Player
from src.enemy import Drone, Meteorite
from src.void_core import VoidCore
from src.ui import Menu, UI
from src.sound import SoundManager
from src.spawner import Spawner


class Game:
    """Главный класс игры"""
    
    def __init__(self):
        # инициализация pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("VoidHunter")
        self.clock = pygame.time.Clock()
        
        # состояние игры
        self.running = True
        self.game_state = "MENU"  # MENU, PLAYING, GAME_OVER
        
        # создаем игрока
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # списки для объектов
        self.enemies = []  # будет заполняться в spawn_enemies()
        self.bullets = []  # будет заполняться при стрельбе
        self.void_cores = []  # будет заполняться при смерти врагов

        self.menu = Menu()
        self.ui = UI()
        self.sound = SoundManager()
        self.spawner = Spawner()
        
        # счет
        self.score = 0
        
        # таймер для спавна врагов
        self.spawn_timer = 0
        self.wave_number = 0
        
    def circle_collision(self, x1, y1, r1, x2, y2, r2):
        """Проверка столкновения двух кругов"""
        # расстояние между центрами
        dx = x1 - x2
        dy = y1 - y2
        distance = math.sqrt(dx * dx + dy * dy)
        
        # если расстояние меньше суммы радиусов - есть столкновение
        return distance < (r1 + r2)
        
    def handle_events(self):
        """Обработка событий клавиатуры и мыши"""

        # pygame.event.get() возвращает все события, которые произошли с прошлого кадра.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # начать игру из меню
                if event.key == pygame.K_SPACE and self.game_state == "MENU":
                    self.start_game()
                
                # рестарт из Game Over
                if event.key == pygame.K_r and self.game_state == "GAME_OVER":
                    self.start_game()
                    
                # стрельба по пробелу
                if event.key == pygame.K_SPACE and self.game_state == "PLAYING":
                    if self.player and hasattr(self.player, 'shoot'):
                        mouse_pos = pygame.mouse.get_pos()
                        bullet = self.player.shoot(mouse_pos[0], mouse_pos[1])
                        if bullet:
                            self.bullets.append(bullet)
                        
            # клик мыши для стрельбы
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.game_state == "PLAYING":
                    if self.player and hasattr(self.player, 'shoot'):
                        mouse_pos = pygame.mouse.get_pos()
                        bullet = self.player.shoot(mouse_pos[0], mouse_pos[1])
                        if bullet:
                            self.bullets.append(bullet)
    
    def spawn_enemies(self, dt):
        """Спавн врагов волнами"""
        self.spawn_timer += dt
        
        # если прошло достаточно времени - создаем новую волну
        if self.spawn_timer >= WAVE_INTERVAL:
            self.spawn_timer = 0
            self.wave_number += 1
            
            # количество врагов в волне растет
            num_enemies = BASE_ENEMIES_PER_WAVE + self.wave_number
            
            for i in range(num_enemies):
                # выбираем случайный тип врага
                enemy_type = random.choice(['drone', 'meteorite'])
                
                # случайная позиция на краю экрана
                side = random.randint(0, 3)
                if side == 0:  # верх
                    x = random.randint(0, SCREEN_WIDTH)
                    y = 0
                elif side == 1:  # право
                    x = SCREEN_WIDTH
                    y = random.randint(0, SCREEN_HEIGHT)
                elif side == 2:  # низ
                    x = random.randint(0, SCREEN_WIDTH)
                    y = SCREEN_HEIGHT
                else:  # лево
                    x = 0
                    y = random.randint(0, SCREEN_HEIGHT)
                
                # создаем врага
                if enemy_type == 'drone':
                    enemy = Drone(x, y)
                else:
                    enemy = Meteorite(x, y)
                self.enemies.append(enemy)
    
    def update(self, dt):
        """Обновление логики игры"""

        if self.game_state == "PLAYING":
            # обновляем игрока
            if self.player:
                # массив состояния клавиш
                keys = pygame.key.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                try:
                    is_shooting = self.player.update(keys, mouse_pos, dt)
                except Exception:

                    is_shooting = False

                if is_shooting and hasattr(self.player, 'shoot'):
                    mouse_pos = pygame.mouse.get_pos()
                    bullet = self.player.shoot(mouse_pos[0], mouse_pos[1])
                    if bullet:
                        self.bullets.append(bullet)

            # спавним врагов
            self.spawn_enemies(dt)
            
            # обновляем врагов
            for enemy in self.enemies[:]:
                if not hasattr(enemy, "update"):
                    continue
                try:
                    if self.player and hasattr(self.player, 'pos'):
                        player_pos = (self.player.pos[0], self.player.pos[1])
                        enemy.update(dt, player_pos)
                    else:
                        enemy.update(dt)
                except TypeError:
                    # резервный вызов — только dt
                    try:
                        enemy.update(dt)
                    except Exception:
                        pass
            # обновляем пули
            for bullet in self.bullets[:]:
                if not hasattr(bullet, "update") or not hasattr(bullet, "is_off_screen"):
                    continue
                bullet.update(dt)
                if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    self.bullets.remove(bullet)
                
            # обновляем void cores
            for core in self.void_cores[:]:
                if hasattr(core, 'update'):
                    core.update(dt)
            
            # КОЛЛИЗИИ

            # 1. Проверка коллизий: пули vs враги
            for bullet in self.bullets[:]:
                for enemy in self.enemies[:]:
                    # Попытка получить координаты/размеры для пули и врага
                    def _get_xy_size(o):
                        if hasattr(o, 'x') and hasattr(o, 'y') and hasattr(o, 'size'):
                            return o.x, o.y, o.size
                        if hasattr(o, 'pos') and hasattr(o, 'radius'):
                            return o.pos[0], o.pos[1], o.radius
                        if hasattr(o, 'pos') and hasattr(o, 'size'):
                            return o.pos[0], o.pos[1], o.size
                        return None

                    b = _get_xy_size(bullet)
                    e = _get_xy_size(enemy)
                    if not b or not e:
                        continue

                    if self.circle_collision(b[0], b[1], b[2], e[0], e[1], e[2]):
                        # враг получает урон
                        if hasattr(enemy, 'take_damage') and hasattr(bullet, 'damage'):
                            enemy.take_damage(bullet.damage)

                        # удаляем пулю
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

                        # считаем врага мёртвым по нескольким критериям
                        enemy_dead = False
                        if hasattr(enemy, 'is_dead') and enemy.is_dead():
                            enemy_dead = True
                        elif hasattr(enemy, 'active') and not enemy.active:
                            enemy_dead = True
                        elif hasattr(enemy, 'hp') and enemy.hp <= 0:
                            enemy_dead = True

                        if enemy_dead:
                            if hasattr(enemy, 'score'):
                                self.score += enemy.score

                            # дроп VoidCore (50% шанс)
                            if random.random() < VOID_CORE_DROP_CHANCE:
                                # пытаемся взять координаты врага для спауна
                                ex, ey, _ = e
                                core = VoidCore(ex, ey)
                                self.void_cores.append(core)

                            if enemy in self.enemies:
                                self.enemies.remove(enemy)
                        break
            
            # 2. Проверка коллизий: враги vs игрок
            if self.player:
                for enemy in self.enemies[:]:
                    # Получаем координаты игрока и врага
                    def _get_xy_size(o):
                        if hasattr(o, 'x') and hasattr(o, 'y') and hasattr(o, 'size'):
                            return o.x, o.y, o.size
                        if hasattr(o, 'pos') and hasattr(o, 'radius'):
                            return o.pos[0], o.pos[1], o.radius
                        if hasattr(o, 'pos') and hasattr(o, 'size'):
                            return o.pos[0], o.pos[1], o.size
                        return None

                    p = _get_xy_size(self.player)
                    e = _get_xy_size(enemy)
                    if not p or not e:
                        continue

                    if self.circle_collision(p[0], p[1], p[2], e[0], e[1], e[2]):
                        # игрок получает урон
                        if hasattr(self.player, 'take_damage') and hasattr(enemy, 'damage'):
                            self.player.take_damage(enemy.damage)

                        # враг умирает при столкновении
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
            
            # 3. Проверка коллизий: void cores vs игрок
            if self.player:
                for core in self.void_cores[:]:
                    if (hasattr(self.player, 'x') and hasattr(self.player, 'y') and hasattr(self.player, 'size') and
                        hasattr(core, 'is_collected')):
                        
                        if core.is_collected(self.player.x, self.player.y, self.player.size):
                            # логика прокачки
                            if hasattr(self.player, 'collect_void_core'):
                                self.player.collect_void_core()
                            
                            if core in self.void_cores:
                                self.void_cores.remove(core)
            
            # 4. Проверка Game Over
            if self.player and hasattr(self.player, 'is_dead'):
                if self.player.is_dead():
                    self.game_state = "GAME_OVER"
    
    def render(self):
        """Отрисовка"""
        # заливка фона
        self.screen.fill(COLOR_BG)
        
        if self.game_state == "MENU":
             if hasattr(self, 'menu'):
                 self.menu.render(self.screen)
             else:
                font = pygame.font.Font(None, 50)
                text = font.render("Press SPACE to start", True, (255, 255, 255))
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(text, text_rect)
            
        elif self.game_state == "PLAYING":
            # рисуем врагов
            for enemy in self.enemies:
                if hasattr(enemy, 'render'):
                    enemy.render(self.screen)

            for core in self.void_cores:
                if hasattr(core, 'render'):
                    core.render(self.screen)
            
            # рисуем пули
            for bullet in self.bullets:
                if hasattr(bullet, 'render'):
                    bullet.render(self.screen)
            
            # рисуем игрока
            if self.player:
                if hasattr(self.player, 'render'):
                    self.player.render(self.screen)
            
            # рисуем UI (счет)
            if hasattr(self, 'ui'):
                self.ui.render(self.screen, self.player, self.score)
            else:
                font = pygame.font.Font(None, 30)
                score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
                self.screen.blit(score_text, (10, 10))
            
        elif self.game_state == "GAME_OVER":
            font = pygame.font.Font(None, 50)
            if hasattr(self, 'ui'):
                self.ui.render_game_over(self.screen, self.score)
            else:
                text = font.render("GAME OVER", True, (255, 0, 0))
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(text, text_rect)
            
            score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(score_text, score_rect)
        
        # обновляем экран
        pygame.display.flip()
    
    def start_game(self):
        """Начало/перезапуск игры"""
        self.game_state = "PLAYING"
        self.score = 0
        self.spawn_timer = 0
        self.wave_number = 0
        
        # очищаем списки
        self.enemies.clear()
        self.bullets.clear()
        self.void_cores.clear()
        
        # создаем игрока
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def game_over(self):
        """Переход в состояние Game Over"""
        self.game_state = "GAME_OVER"
    
    def run(self):
        """Основной игровой цикл"""
        while self.running:
            # delta time в секундах
            dt = self.clock.tick(FPS) / 1000.0
            
            # обработка событий
            self.handle_events()
            
            # обновление логики
            self.update(dt)
            
            # отрисовка
            self.render()
        
        # выход
        pygame.quit()
        sys.exit()
