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
from src.utils import circle_collision


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
        
    def circle_collision(self, pos1, radius1, pos2, radius2):
        """Проверка столкновения двух кругов с использованием pygame.math.Vector2 (от Dev B)"""
        return circle_collision(pos1, radius1, pos2, radius2)
        
    def handle_events(self):
        """Обработка событий клавиатуры и мыши"""

        # pygame.event.get() возвращает все события, которые произошли с прошлого кадра.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Обработка событий в меню
            if self.game_state == "MENU" and hasattr(self, 'menu'):
                mouse_pos = pygame.mouse.get_pos()
                menu_action = self.menu.handle_event(event, mouse_pos)
                if menu_action == "start":
                    self.start_game()
                elif menu_action == "exit":
                    self.running = False
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # начать игру из меню (резервный запуск)
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
                            if hasattr(self, 'sound'):
                                self.sound.play("shoot")
                        
            # клик мыши для стрельбы
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.game_state == "PLAYING":
                    if self.player and hasattr(self.player, 'shoot'):
                        mouse_pos = pygame.mouse.get_pos()
                        bullet = self.player.shoot(mouse_pos[0], mouse_pos[1])
                        if bullet:
                            self.bullets.append(bullet)
                            if hasattr(self, 'sound'):
                                self.sound.play("shoot")
    
    def spawn_enemies(self, dt):
        """Спавн врагов волнами с помощью Spawner"""
        if hasattr(self, 'spawner'):
            new_enemies = self.spawner.update(dt)
            self.enemies.extend(new_enemies)
            # Синхронизируем wave_number с Spawner
            self.wave_number = self.spawner.wave_number
    
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
                        if hasattr(self, 'sound'):
                            self.sound.play("shoot")

            # спавним врагов
            self.spawn_enemies(dt)
            
            # обновляем врагов
            for enemy in self.enemies[:]:
                if not hasattr(enemy, "update"):
                    continue
                try:
                    if self.player and hasattr(self.player, 'pos'):
                        enemy.update(dt, self.player.pos)
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
                if not hasattr(bullet, "update"):
                    continue
                bullet.update(dt)
                
                # проверка выхода пули за экран с учетом логики Dev B (bullet.active = False)
                is_off_screen = False
                if hasattr(bullet, "is_off_screen"):
                    is_off_screen = bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
                elif hasattr(bullet, "active"):
                    is_off_screen = not bullet.active
                
                if is_off_screen:
                    self.bullets.remove(bullet)
                
            # обновляем void cores
            for core in self.void_cores[:]:
                if hasattr(core, 'update'):
                    core.update(dt)
            
            # КОЛЛИЗИИ
            
            # 1. Проверка коллизий: пули vs враги
            for bullet in self.bullets[:]:
                for enemy in self.enemies[:]:
                    b_pos = getattr(bullet, 'pos', None)
                    b_radius = getattr(bullet, 'radius', getattr(bullet, 'size', 0))
                    e_pos = getattr(enemy, 'pos', None)
                    e_radius = getattr(enemy, 'radius', getattr(enemy, 'size', 0))

                    if b_pos is not None and e_pos is not None:
                        if self.circle_collision(b_pos, b_radius, e_pos, e_radius):
                            # враг получает урон
                            if hasattr(enemy, 'take_damage') and hasattr(bullet, 'damage'):
                                enemy.take_damage(bullet.damage)
                            elif hasattr(enemy, 'take_damage'):
                                # урон пули по умолчанию 1
                                enemy.take_damage(1)

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
                                # начисление очков
                                if hasattr(enemy, 'score'):
                                    self.score += enemy.score
                                elif hasattr(enemy, 'radius'):
                                    # очки зависят от размера врага
                                    self.score += int(enemy.radius)

                                # воспроизведение звука взрыва
                                if hasattr(self, 'sound'):
                                    self.sound.play("explosion")

                                # дроп VoidCore (50% шанс)
                                if random.random() < VOID_CORE_DROP_CHANCE:
                                    core = VoidCore(e_pos.x, e_pos.y)
                                    self.void_cores.append(core)

                                if enemy in self.enemies:
                                    self.enemies.remove(enemy)
                            break
            
            # 2. Проверка коллизий: враги vs игрок
            if self.player:
                for enemy in self.enemies[:]:
                    p_pos = getattr(self.player, 'pos', None)
                    p_radius = getattr(self.player, 'radius', getattr(self.player, 'size', 0))
                    e_pos = getattr(enemy, 'pos', None)
                    e_radius = getattr(enemy, 'radius', getattr(enemy, 'size', 0))

                    if p_pos is not None and e_pos is not None:
                        if self.circle_collision(p_pos, p_radius, e_pos, e_radius):
                            # игрок получает урон
                            damage = getattr(enemy, 'damage', 1)  # урон по умолчанию 1
                            if hasattr(self.player, 'take_damage'):
                                self.player.take_damage(damage)
                                if hasattr(self, 'sound'):
                                    self.sound.play("player_hit")

                            # враг умирает при столкновении
                            if enemy in self.enemies:
                                self.enemies.remove(enemy)
                                if hasattr(self, 'sound'):
                                    self.sound.play("explosion")
            
            # 3. Проверка коллизий: void cores vs игрок
            if self.player:
                for core in self.void_cores[:]:
                    p_pos = getattr(self.player, 'pos', None)
                    p_radius = getattr(self.player, 'radius', getattr(self.player, 'size', 0))
                    c_pos = getattr(core, 'pos', None)
                    c_radius = getattr(core, 'radius', getattr(core, 'size', 0))
                    
                    is_collected = False
                    if hasattr(core, 'is_collected'):
                        try:
                            if p_pos is not None:
                                is_collected = core.is_collected(p_pos.x, p_pos.y, p_radius)
                        except Exception:
                            pass
                    elif p_pos is not None and c_pos is not None:
                        # если метод is_collected не определен, используем коллизию кругов
                        is_collected = self.circle_collision(p_pos, p_radius, c_pos, c_radius)
                    
                    if is_collected:
                        # логика прокачки
                        if hasattr(self.player, 'add_charge'):
                            self.player.add_charge()
                        elif hasattr(self.player, 'collect_void_core'):
                            self.player.collect_void_core()
                        
                        if hasattr(self, 'sound'):
                            self.sound.play("pickup")
                        
                        if core in self.void_cores:
                            self.void_cores.remove(core)
            
            # 4. Проверка Game Over
            if self.player:
                is_dead = False
                if hasattr(self.player, 'is_dead'):
                    is_dead = self.player.is_dead()
                elif hasattr(self.player, 'hp'):
                    is_dead = self.player.hp <= 0
                
                if is_dead:
                    self.game_state = "GAME_OVER"
                    
        elif self.game_state == "MENU":
            if hasattr(self, 'menu'):
                self.menu.update(dt)
    
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
        
        if hasattr(self, 'spawner'):
            self.spawner.reset()
        
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
