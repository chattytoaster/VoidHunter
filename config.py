# Константы для игры

# Окно
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Цвета
COLOR_BG = (5, 5, 15)
COLOR_PLAYER = (0, 255, 200)
COLOR_BULLET = (255, 255, 100)
COLOR_DRONE = (255, 50, 50)
COLOR_METEORITE = (120, 90, 70)
COLOR_VOID_CORE = (200, 0, 255)

# Игрок
PLAYER_SIZE = 20
PLAYER_SPEED = 300
PLAYER_HP = 5
PLAYER_SHOOT_COOLDOWN = 0.2

# Пули
BULLET_SPEED = 600
BULLET_SIZE = 4
BULLET_DAMAGE = 1

# Враги
DRONE_SIZE = 15
DRONE_SPEED = 150
DRONE_HP = 1
DRONE_DAMAGE = 1
DRONE_SCORE = 10

METEORITE_SIZE = 35
METEORITE_SPEED = 100
METEORITE_HP = 5
METEORITE_DAMAGE = 2
METEORITE_SCORE = 50

# Система спавна
WAVE_INTERVAL = 5.0
BASE_ENEMIES_PER_WAVE = 2

# VoidCore
VOID_CORE_SIZE = 8
VOID_CORE_DROP_CHANCE = 0.5

# Пути к ассетам
import os
FONT_PATH = os.path.join("assets", "fonts", "ArcadeJeu-Regular.otf")
IMAGE_PLAYER = os.path.join("assets", "images", "player_ship.png")
IMAGE_DRONE = os.path.join("assets", "images", "drone.png")
IMAGE_METEORITE = os.path.join("assets", "images", "meteorite.png")
IMAGE_BULLET = os.path.join("assets", "images", "bullet.png")
IMAGE_VOID_CORE = os.path.join("assets", "images", "void_core.png")
