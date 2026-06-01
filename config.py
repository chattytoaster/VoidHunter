# Константы для игры Void Hunter

# === ОКНО И ДИСПЛЕЙ ===
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "Void Hunter"

# === ЦВЕТА (RGB) - Неоновая палитра ===
COLOR_BG = (5, 5, 15)              # Почти черный космос
COLOR_PLAYER = (0, 255, 200)       # Cyan для игрока
COLOR_BULLET = (255, 255, 100)     # Желтый для пуль
COLOR_METEORITE = (120, 90, 70)    # Коричневый для метеоритов
COLOR_DRONE = (255, 50, 50)        # Красный для дронов
COLOR_GUNSHIP = (255, 140, 60)     # Оранжевый для стреляющих кораблей
COLOR_ENEMY_BULLET = (255, 120, 80)
COLOR_VOID_CORE = (200, 0, 255)    # Фиолетовый для ядер
COLOR_UI_TEXT = (255, 255, 255)    # Белый для текста
COLOR_HP_FULL = (0, 255, 100)      # Зеленый для HP
COLOR_HP_LOW = (255, 50, 50)       # Красный для низкого HP
COLOR_CHARGE_BAR = (150, 0, 255)   # Фиолетовый для заряда

# === ИГРОК ===
PLAYER_SIZE = 20                   # Радиус треугольника
PLAYER_MAX_SPEED = 400             # Пикселей в секунду
PLAYER_ACCELERATION = 1200         # Ускорение
PLAYER_DAMPING = 0.92              # Трение (0.92 = 8% потери скорости)
PLAYER_MAX_HP = 5                  # Начальное здоровье
PLAYER_INVULNERABILITY_TIME = 1.5  # Секунды неуязвимости после урона

# === ОРУЖИЕ ===
BULLET_SPEED = 800                 # Скорость пули
BULLET_SIZE = 4                    # Радиус пули
BULLET_DAMAGE = 1.0                # Базовый урон
BULLET_LIFETIME = 2.0              # Секунды до исчезновения
FIRE_RATE = 0.15                   # Секунды между выстрелами (базовая)

# === ВРАГИ ===
# Дрон
DRONE_SIZE = 15
DRONE_HP = 1
DRONE_SPEED = 150
DRONE_DAMAGE = 1
DRONE_SCORE = 10
DRONE_CHASE_RANGE = 10000            # Дистанция, на которой дрон начинает преследование

# Метеорит (крупный, живучий, не преследует)
METEORITE_SIZE = 38
METEORITE_HP = 10
METEORITE_SPEED = 120
METEORITE_DAMAGE = 1
METEORITE_SCORE = 50

# Вражеский корабль (редкий, стреляет медленно)
GUNSHIP_SIZE = 22
GUNSHIP_HP = 5
GUNSHIP_SPEED = 95
GUNSHIP_DAMAGE = 1
GUNSHIP_SCORE = 30
GUNSHIP_FIRE_COOLDOWN = 3
ENEMY_BULLET_SPEED = 340
ENEMY_BULLET_SIZE = 5
ENEMY_BULLET_DAMAGE = 1

# === VOID CORES ===
VOID_CORE_SIZE = 8
VOID_CORE_DROP_CHANCE = 0.6        # 60% шанс дропа
VOID_CORE_COLLECT_RANGE = 40       # Радиус сбора
VOID_CORE_MAX_LEVEL = 20           # Максимальный уровень заряда
VOID_CORES_PER_LEVEL = [
    0,      # Уровень 0
    3,      # Уровень 1 (+3)
    7,      # Уровень 2 (+4)
    12,     # Уровень 3 (+5)
    18,     # Уровень 4 (+6)
    25,     # Уровень 5 (+7)
    33,     # Уровень 6 (+8)
    42,     # Уровень 7 (+9)
    52,     # Уровень 8 (+10)
    63,     # Уровень 9 (+11)
    75,     # Уровень 10 (+12)
    88,     # Уровень 11 (+13)
    102,    # Уровень 12 (+14)
    117,    # Уровень 13 (+15)
    133,    # Уровень 14 (+16)
    150,    # Уровень 15 (+17)
    168,    # Уровень 16 (+18)
    187,    # Уровень 17 (+19)
    207,    # Уровень 18 (+20)
    228,    # Уровень 19 (+21)
    250,    # Уровень 20 (+22)
]

# Бонусы за уровень заряда
CHARGE_DAMAGE_BONUS = 0.20         # +20% урона за уровень
CHARGE_FIRE_RATE_BONUS = 0.15      # +15% скорострельности за уровень
CHARGE_SPAWN_MULTIPLIER = 0.1      # +10% спавна врагов за уровень

# === VOID FLASH ===
VOID_FLASH_DURATION = 0.3          # Длительность вспышки в секундах
VOID_FLASH_COLOR = (255, 255, 255) # Белая вспышка

# === СИСТЕМА СПАВНА ===
WAVE_INTERVAL = 6.5                # Секунды между волнами (чаще)
BASE_ENEMIES_PER_WAVE = 2          # Базовое количество врагов
ENEMIES_INCREASE_PER_WAVE = 1      # Увеличение за волну
DRONE_SPAWN_WEIGHT = 0.15          # 56% дроны
GUNSHIP_SPAWN_WEIGHT = 0.05        # 5% стреляющие корабли
METEORITE_SPAWN_WEIGHT = 0.02      # 1% метеориты (очень редко)
SPAWN_MARGIN = 250                 # Отступ от края экрана для спавна

# === ЧАСТИЦЫ ===
PARTICLE_LIFETIME = 0.8            # Секунды жизни частицы
PARTICLE_COUNT_EXPLOSION = 15      # Количество частиц при взрыве
PARTICLE_SPEED_MIN = 50
PARTICLE_SPEED_MAX = 200

# === UI ===
UI_MARGIN = 20                     # Отступ от краев экрана
UI_FONT_SIZE = 32
UI_FONT_SIZE_LARGE = 64
HP_ICON_SIZE = 30                  # Размер иконки сердца
CHARGE_BAR_WIDTH = 200
CHARGE_BAR_HEIGHT = 20

# === ЗВУКИ ===
SOUND_VOLUME = 0.7                 # Громкость звуковых эффектов (0.0 - 1.0)
MUSIC_VOLUME = 0.4                 # Громкость музыки
