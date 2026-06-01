import pygame
import sys
import random
from config import *
from src.player import Player
from src.projectile import Bullet
from src.enemy import Drone, Meteorite, Gunship
from src.utils import circle_collision
from src.spawner import WaveSpawner
from src.void_core import VoidCore
from src.particle import Particle, create_explosion
from src.ui import HUD
from src.sound import SoundManager
from src.camera import Camera
from src.background import SpaceBackground
from src.menu import MainMenu


class Game:
    """Главный класс игры, управляющий игровым циклом"""
    
    def __init__(self):
        """Инициализация игры"""
        pygame.init()
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        
        # Создание окна
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption(WINDOW_TITLE)
        
        # Часы для контроля FPS
        self.clock = pygame.time.Clock()
        
        # Состояние игры
        self.running = True
        self.game_state = "MENU"  # MENU, PLAYING или GAME_OVER
        
        # Игровые объекты
        self.player = Player(self.screen_width // 2, self.screen_height // 2)
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        self.void_cores = []
        self.particles = []
        
        # Система спавна волн
        self.spawner = WaveSpawner()
        
        # UI
        self.hud = HUD()
        
        # Главное меню
        self.menu = MainMenu()
        
        # Звуковая система
        self.sound = SoundManager()
        
        # Камера (для тряски экрана)
        self.camera = Camera()

        # Фон (звезды и планеты)
        self.background = SpaceBackground(self.screen_width, self.screen_height)
        
        # Игровая статистика
        self.score = 0
        
        # Void Flash эффект
        self.void_flash_timer = 0
        
    def handle_events(self):
        """Обработка событий (клавиатура, мышь, закрытие окна)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.VIDEORESIZE:
                # Минимальные размеры, чтобы UI и игра оставались читаемыми
                self.screen_width = max(640, event.w)
                self.screen_height = max(360, event.h)
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height),
                    pygame.RESIZABLE
                )
                self.background.resize(self.screen_width, self.screen_height)
            
            # Обработка событий меню
            if self.game_state == "MENU":
                mouse_pos = pygame.mouse.get_pos()
                action = self.menu.handle_event(event, mouse_pos)
                if action == "start":
                    self.start_game()
                elif action == "exit":
                    self.running = False
            
            elif self.game_state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "MENU"
                
                    # Перезапуск игры по R на экране Game Over
                    if event.key == pygame.K_r and self.game_state == "GAME_OVER":
                        self.reset()
                    
                    # Void Flash по Q
                    if event.key == pygame.K_q and self.game_state == "PLAYING":
                        if self.player.activate_void_flash():
                            # Уничтожаем всех врагов
                            for enemy in self.enemies:
                                self.score += enemy.score
                            self.enemies.clear()
                            # Активируем визуальный эффект
                            self.void_flash_timer = VOID_FLASH_DURATION
                            # Звук Void Flash
                            self.sound.play('void_flash')
                    
                    # Стрельба по Пробелу
                    if event.key == pygame.K_SPACE and self.game_state == "PLAYING":
                        mouse_pos = pygame.mouse.get_pos()
                        if self.player.shoot(mouse_pos):
                            # Создание пули
                            damage = BULLET_DAMAGE * self.player.get_damage_multiplier()
                            bullet = Bullet(
                                self.player.position.x,
                                self.player.position.y,
                                mouse_pos[0],
                                mouse_pos[1],
                                damage
                            )
                            self.bullets.append(bullet)
                            # Звук выстрела
                            self.sound.play('shoot')
                
                # Стрельба по ЛКМ
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.game_state == "PLAYING":
                        mouse_pos = pygame.mouse.get_pos()
                        if self.player.shoot(mouse_pos):
                            # Создание пули
                            damage = BULLET_DAMAGE * self.player.get_damage_multiplier()
                            bullet = Bullet(
                                self.player.position.x,
                                self.player.position.y,
                                mouse_pos[0],
                                mouse_pos[1],
                                damage
                            )
                            self.bullets.append(bullet)
                            # Звук выстрела
                            self.sound.play('shoot')
            
            elif self.game_state == "GAME_OVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "MENU"
    
    def update(self, dt):
        """Обновление игровой логики"""
        if self.game_state == "MENU":
            # Обновление меню
            mouse_pos = pygame.mouse.get_pos()
            self.menu.update(mouse_pos, self.screen_width, self.screen_height)
            # Обновление фона в меню
            self.background.update(dt, 0)
        
        elif self.game_state == "PLAYING":
            # Получение состояния клавиатуры и мыши
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            
            # Обновление игрока
            self.player.update(dt, keys, mouse_pos, self.screen_width, self.screen_height)

            # Обновление фона
            self.background.update(dt, self.player.charge_level)
            
            # Обновление камеры (тряска от заряда)
            self.camera.update(dt, self.player.charge_level)
            
            # Обновление таймера Void Flash
            if self.void_flash_timer > 0:
                self.void_flash_timer -= dt
            
            # Обновление пуль
            for bullet in self.bullets[:]:
                bullet.update(dt)
                # Удаление пуль за экраном или с истекшим временем
                if bullet.is_off_screen(self.screen_width, self.screen_height) or bullet.is_expired():
                    self.bullets.remove(bullet)

            # Обновление вражеских пуль
            for enemy_bullet in self.enemy_bullets[:]:
                enemy_bullet.update(dt)
                if enemy_bullet.is_dead(self.screen_width, self.screen_height):
                    self.enemy_bullets.remove(enemy_bullet)
            
            # Обновление врагов
            for enemy in self.enemies[:]:
                enemy.update(
                    dt,
                    (self.player.position.x, self.player.position.y),
                    self.screen_width,
                    self.screen_height
                )

                # Метеориты исчезают, улетая за левую границу
                if enemy.type == "meteorite" and enemy.position.x < -enemy.size - 40:
                    self.enemies.remove(enemy)
                    continue

                # Стрельба редких кораблей
                if enemy.type == "gunship":
                    shot = enemy.try_shoot((self.player.position.x, self.player.position.y))
                    if shot is not None:
                        self.enemy_bullets.append(shot)
            
            # Обновление Void Cores
            for core in self.void_cores[:]:
                core.update(dt)
            
            # Обновление частиц
            for particle in self.particles[:]:
                particle.update(dt)
                if particle.is_dead():
                    self.particles.remove(particle)
            
            # Обновление системы спавна волн
            new_enemies = self.spawner.update(
                dt,
                self.player.charge_level,
                self.screen_width,
                self.screen_height,
            )
            self.enemies.extend(new_enemies)
            
            # Проверка коллизий: пули vs враги
            for bullet in self.bullets[:]:
                for enemy in self.enemies[:]:
                    if circle_collision(
                        (bullet.position.x, bullet.position.y), bullet.size,
                        (enemy.position.x, enemy.position.y), enemy.size
                    ):
                        # Враг получает урон
                        enemy.take_damage(bullet.damage)
                        # Удаляем пулю
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        
                        # Если враг умер
                        if enemy.is_dead():
                            self.score += enemy.score
                            
                            # Звук взрыва
                            self.sound.play('explosion')
                            
                            # Создание частиц взрыва
                            explosion = create_explosion(
                                enemy.position.x, 
                                enemy.position.y, 
                                COLOR_METEORITE if enemy.type == "meteorite" else (
                                    COLOR_GUNSHIP if enemy.type == "gunship" else COLOR_DRONE
                                )
                            )
                            self.particles.extend(explosion)
                            
                            # Дроп Void Core с шансом
                            if random.random() < VOID_CORE_DROP_CHANCE:
                                core = VoidCore(enemy.position.x, enemy.position.y)
                                self.void_cores.append(core)
                            
                            if enemy in self.enemies:
                                self.enemies.remove(enemy)
                        break
            
            # Проверка коллизий: Void Cores vs игрок
            for core in self.void_cores[:]:
                if core.is_collected_by(self.player):
                    self.player.collect_void_core()
                    self.void_cores.remove(core)
                    # Звук сбора
                    self.sound.play('collect')
            
            # Проверка коллизий: враги vs игрок
            for enemy in self.enemies[:]:
                if circle_collision(
                    (self.player.position.x, self.player.position.y), self.player.size,
                    (enemy.position.x, enemy.position.y), enemy.size
                ):
                    # Игрок получает урон
                    if self.player.take_damage(enemy.damage):
                        # Звук попадания
                        self.sound.play('hit')
                        # Враг тоже умирает при столкновении
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)

            # Проверка коллизий: вражеские пули vs игрок
            for enemy_bullet in self.enemy_bullets[:]:
                if circle_collision(
                    (self.player.position.x, self.player.position.y), self.player.size,
                    (enemy_bullet.position.x, enemy_bullet.position.y), enemy_bullet.size
                ):
                    if self.player.take_damage(enemy_bullet.damage):
                        self.sound.play('hit')
                    self.enemy_bullets.remove(enemy_bullet)
            
            # Проверка смерти игрока
            if self.player.is_dead():
                self.game_over()
        
    def render(self):
        """Отрисовка всех объектов"""
        # Заливка фона
        self.screen.fill(COLOR_BG)
        
        if self.game_state == "MENU":
            # Отрисовка фона в меню
            self.background.render(self.screen)
            self.background.render_stars(self.screen, 0)
            
            # Отрисовка меню
            self.menu.render(self.screen, self.screen_width, self.screen_height)
        
        elif self.game_state == "PLAYING":
            # Создаем временную поверхность для эффекта тряски
            game_surface = pygame.Surface((self.screen_width, self.screen_height))
            game_surface.fill(COLOR_BG)

            # Планета и дальний фон
            self.background.render(game_surface)

            # Звезды (полоски при высоком заряде)
            self.background.render_stars(game_surface, self.player.charge_level)
            
            # Отрисовка частиц (под всем остальным)
            for particle in self.particles:
                particle.render(game_surface)
            
            # Отрисовка врагов
            for enemy in self.enemies:
                enemy.render(game_surface)
            
            # Отрисовка Void Cores
            for core in self.void_cores:
                core.render(game_surface)
            
            # Отрисовка пуль
            for bullet in self.bullets:
                bullet.render(game_surface)

            # Отрисовка вражеских пуль
            for enemy_bullet in self.enemy_bullets:
                enemy_bullet.render(game_surface)
            
            # Отрисовка игрока
            if self.player:
                self.player.render(game_surface)
            
            # Применяем смещение камеры (тряска)
            offset = self.camera.get_offset()
            self.screen.blit(game_surface, offset)
            
            # Отрисовка UI (без тряски)
            self.hud.render(self.screen, self.player, self.score, self.screen_width, self.screen_height)
            
            # Эффект Void Flash (белая вспышка)
            if self.void_flash_timer > 0:
                alpha = int(255 * (self.void_flash_timer / VOID_FLASH_DURATION))
                flash_surface = pygame.Surface((self.screen_width, self.screen_height))
                flash_surface.set_alpha(alpha)
                flash_surface.fill(VOID_FLASH_COLOR)
                self.screen.blit(flash_surface, (0, 0))
        
        elif self.game_state == "GAME_OVER":
            # Отрисовка экрана Game Over
            self.hud.render_game_over(self.screen, self.score, self.screen_width, self.screen_height)
        
        # Обновление экрана
        pygame.display.flip()
    
    def reset(self):
        """Перезапуск игры"""
        self.game_state = "PLAYING"
        self.score = 0
        self.enemies.clear()
        self.bullets.clear()
        self.enemy_bullets.clear()
        self.void_cores.clear()
        self.particles.clear()
        # Пересоздание игрока
        self.player = Player(self.screen_width // 2, self.screen_height // 2)
        # Сброс спавнера
        self.spawner.reset()
    
    def start_game(self):
        """Начало новой игры из меню"""
        self.reset()
        self.game_state = "PLAYING"
    
    def game_over(self):
        """Переход в состояние Game Over"""
        self.game_state = "GAME_OVER"
    
    def run(self):
        """Главный игровой цикл"""
        while self.running:
            # Вычисление delta time (время между кадрами)
            dt = self.clock.tick(FPS) / 1000.0  # Конвертируем в секунды
            
            # Обработка событий
            self.handle_events()
            
            # Обновление логики
            self.update(dt)
            
            # Отрисовка
            self.render()
        
        # Завершение работы
        pygame.quit()
        sys.exit()
