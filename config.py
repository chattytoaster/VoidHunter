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
COLOR_ASTEROID = (150, 150, 150)   # Серый для астероидов
COLOR_DRONE = (255, 50, 50)        # Красный для дронов
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
BULLET_DAMAGE = 1                  # Базовый урон
BULLET_LIFETIME = 2.0              # Секунды до исчезновения
FIRE_RATE = 0.10                   # Секунды между выстрелами (базовая)

# === ВРАГИ ===
# Астероид
ASTEROID_SIZE = 30
ASTEROID_HP = 3
ASTEROID_SPEED = 80
ASTEROID_DAMAGE = 1
ASTEROID_SCORE = 10

# Дрон
DRONE_SIZE = 15
DRONE_HP = 1
DRONE_SPEED = 180
DRONE_DAMAGE = 1
DRONE_SCORE = 25
DRONE_CHASE_RANGE = 600            # Дистанция, на которой дрон начинает преследование

# === VOID CORES ===
VOID_CORE_SIZE = 8
VOID_CORE_DROP_CHANCE = 0.6        # 60% шанс дропа
VOID_CORE_COLLECT_RANGE = 40       # Радиус сбора
VOID_CORE_MAX_LEVEL = 5            # Максимальный уровень заряда
VOID_CORES_PER_LEVEL = [0, 3, 7, 12, 18, 25]  # Кумулятивно

# Бонусы за уровень заряда
CHARGE_DAMAGE_BONUS = 0.20         # +20% урона за уровень
CHARGE_FIRE_RATE_BONUS = 0.15      # +15% скорострельности за уровень
CHARGE_SPAWN_MULTIPLIER = 0.3      # +30% спавна врагов за уровень

# === VOID FLASH ===
VOID_FLASH_DURATION = 0.3          # Длительность вспышки в секундах
VOID_FLASH_COLOR = (255, 255, 255) # Белая вспышка

# === СИСТЕМА СПАВНА ===
WAVE_INTERVAL = 10.0               # Секунды между волнами
BASE_ENEMIES_PER_WAVE = 3          # Базовое количество врагов
ENEMIES_INCREASE_PER_WAVE = 2      # Увеличение за волну
ASTEROID_SPAWN_WEIGHT = 0.7        # 70% астероиды
DRONE_SPAWN_WEIGHT = 0.3           # 30% дроны
SPAWN_MARGIN = 100                 # Отступ от края экрана для спавна

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
