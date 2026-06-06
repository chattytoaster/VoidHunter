# План: Переработка VoidHunter в командной разработке

Перенесите текущий код в папку OLD для истории, затем распределите переработку по 3 разработчикам. 
Начните с минимального функционала (только Drone + Meteorite, без Gunship и эффектов) 
чтобы явно отличалась от оригинала.

## Распределение по ролям (3 человека)

### Developer A — Core Game & Physics (≈150-200 строк)
**Ответственность:**
- Переписать `main.py` и основной Game class (упрощенный)
- Реализовать базовый update/render цикл
- Система коллизий (упростить если нужно)
- Управление игроком (WASD + мышь для стрельбы)
- Эта роль — фундамент, остальные зависят от него

**Основные файлы:**
- `main.py`
- `src/game.py` (основной класс Game)

---

### Developer B — Entities & Rendering (≈250-300 строк)
**Ответственность:**
- Player класс (простой треугольник, движение, жизни)
- Enemy классы — только Drone и Meteorite (без Gunship)
- Projectile (пули игрока) — максимум простой
- Render функции (базовая графика без частиц и сложных эффектов)
- Убрать: Particle систему, Void Flash, сложные эффекты камеры

**Основные файлы:**
- `src/player.py`
- `src/enemy.py`
- `src/projectile.py`
- `src/utils.py` (draw функции)

---

### Developer C — Game Systems (≈150-200 строк)
**Ответственность:**
- Menu (простое меню с кнопками Start/Exit)
- UI (счет, HP, уровень заряда)
- Spawner (спавн врагов волнами)
- Sound система (остаточно простая)
- VoidCore сбор (система прокачки через cores)

**Основные файлы:**
- `src/menu.py`
- `src/ui.py`
- `src/spawner.py`
- `src/sound.py`
- `src/void_core.py`

---

## Упрощения для "видимой переделки"

### Убрать полностью:
1. **Gunship** — враги что стреляют (убрать из enemy.py)
2. **Particle система** — убрать create_explosion, никаких взрывов
3. **Void Flash способность** — убрать Q клавишу и белую вспышку
4. **Camera shake эффекты** — просто статичная камера
5. **Background звезды** — упростить до простого цвета
6. **Enemy bullets** — враги не стреляют

### Оставить & упростить:
- 2 типа врагов (Drone + Meteorite) — но с **переписанным кодом**
- VoidCore система — но более простая механика
- Sound (но без музыки, только звуки)
- UI — база без красивых эффектов
- Меню — простое, без анимаций

---

## Структура файлов (новая)

```
VoidHunter/
│
├── OLD/                          # Старый код для истории
│   ├── config.py
│   ├── main.py
│   ├── requirements.txt
│   └── src/
│       ├── __init__.py
│       ├── background.py
│       ├── camera.py
│       ├── enemy.py
│       ├── game.py
│       ├── menu.py
│       ├── particle.py
│       ├── player.py
│       ├── projectile.py
│       ├── sound.py
│       ├── spawner.py
│       ├── ui.py
│       ├── utils.py
│       └── void_core.py
│
├── PLAN.md                       # Этот файл
├── config.py                     # Упрощенные константы
├── main.py                       # Точка входа (Dev A)
├── requirements.txt              # pygame только
│
└── src/
    ├── __init__.py
    ├── game.py                   # Game loop (Dev A)
    ├── player.py                 # Простой Player (Dev B)
    ├── enemy.py                  # Drone + Meteorite (Dev B)
    ├── projectile.py             # Bullet (Dev B)
    ├── ui.py                     # Menu + HUD (Dev C)
    ├── spawner.py                # Wave spawner (Dev C)
    ├── sound.py                  # Sound manager (Dev C)
    ├── utils.py                  # Collisions, helper functions (общий)
    └── void_core.py              # VoidCore система (Dev C)
```

---

## Шаги реализации (скоординировано)

### Фаза 0: Подготовка (15-20 минут)
1. **Переместить старый код в OLD/**
   ```bash
   mkdir OLD
   move src OLD/src 2>nul
   move config.py OLD/config.py 2>nul
   move main.py OLD/main.py 2>nul
   move requirements.txt OLD/requirements.txt 2>nul
   ```

2. **Создать базовую структуру**
   - Новый `config.py` с упрощенными константами
   - Новый `main.py` (Dev A)
   - Папка `src/` с пустыми файлами

---

### Фаза 1: Инфраструктура (2-3 часа)

**Dev A (ПРИОРИТЕТ 1):**
- [ ] Написать костяк Game класса
- [ ] Основной game loop (handle_events, update, render)
- [ ] Инициализация pygame
- [ ] Пустые методы для остальных компонентов

**Dev B (ПРИОРИТЕТ 2):**
- [ ] Написать Player класс с заглушками
- [ ] Написать базовый Enemy класс
- [ ] Создать Drone и Meteorite (простые версии)
- [ ] Написать Bullet класс
- [ ] Базовые render функции

**Dev C (ПРИОРИТЕТ 3):**
- [ ] Написать Menu класс (заглушка)
- [ ] Написать UI класс (заглушка)
- [ ] Написать Spawner класс (заглушка)
- [ ] Написать Sound класс (заглушка)
- [ ] Написать VoidCore класс (заглушка)

**Результат:** Игра запускается, не падает, нет ошибок импортов

---

### Фаза 2: Основной геймплей (4-5 часов)

**Dev A:**
- [ ] Полный `update()` метод
  - Обновление Player
  - Обновление врагов
  - Обновление пуль
  - Обновление Void Cores
- [ ] Базовая система коллизий
  - Пули vs враги
  - Враги vs игрок
  - VoidCore vs игрок
- [ ] Спавн врагов (вызов Spawner)
- [ ] Game Over логика

**Dev B:**
- [ ] Player:
  - Движение WASD
  - Поворот к мыши
  - Стрельба (SPACE или LMB)
  - Получение урона
  - Сбор VoidCore
- [ ] Enemy (Drone):
  - Простое преследование (движение к игроку)
  - Анимация (ромб)
- [ ] Enemy (Meteorite):
  - Движение слева направо
  - Слабый отскок от стен
- [ ] Projectile (Bullet):
  - Движение в направлении мыши
  - Исчезновение за экраном
- [ ] Utils:
  - `circle_collision()` функция

**Dev C:**
- [ ] Menu:
  - Кнопка "Start Game"
  - Кнопка "Exit"
- [ ] UI:
  - Отображение HP
  - Отображение Score
  - Отображение уровня заряда
- [ ] Spawner:
  - Спавн волн врагов каждые N секунд
  - Увеличение количества врагов
  - Только Drone и Meteorite
- [ ] Sound:
  - Загрузка звуков из assets
  - Функция play(sound_name)
- [ ] VoidCore:
  - Спавнится при убийстве врага
  - Собирается игроком
  - Увеличивает уровень заряда

**Результат:** Полная игра, можно играть, убивать врагов, собирать cores

---

### Фаза 3: Полировка & Баланс (2-3 часа)

1. **Баланс:**
   - [ ] Сложность врагов
   - [ ] Урон и HP
   - [ ] Скорость спавна
   - [ ] Стоимость VoidCore уровней

2. **Баги:**
   - [ ] Враги не вылетают за экран
   - [ ] Пули не зависают
   - [ ] Коллизии работают правильно
   - [ ] Нет утечек памяти

3. **Доп. фичи (если время):**
   - [ ] Звуки (если не добавили)
   - [ ] Сообщение при Game Over
   - [ ] Рестарт игры (R клавиша)

---

## Ключевые упрощения в коде

### Dev A (Game.py) — ~150 строк
```python
class Game:
    def __init__(self):
        # pygame.init(), создание экрана
        # self.player, self.enemies, self.bullets, self.void_cores
        # self.sound, self.menu, self.ui, self.spawner
        # self.score, self.game_state
        
    def handle_events(self):
        # Обработка QUIT, KEYDOWN (SPACE стрельба, ESC меню)
        # Нет сложной логики abilities
        
    def update(self, dt):
        # Обновление player, enemies, bullets, cores
        # Проверка коллизий (простой круг-круг)
        # Спавн врагов
        # Game over check
        
    def render(self):
        # Заливка экрана
        # Отрисовка фона (простой цвет)
        # Отрисовка объектов
        # Отрисовка UI
        # flip()
        
    def run(self):
        # Основной цикл (handle_events, update, render)
```

### Dev B (Player/Enemy/Projectile) — ~250 строк
```python
class Player:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.vel = [0, 0]
        self.hp = 5
        self.charge_level = 0
        
    def update(self, keys, mouse_pos):
        # WASD движение
        # Поворот к мыши
        # Возврат стрельбы (True/False)
        
    def render(self, screen):
        # pygame.draw.polygon() треугольник

class Drone(Enemy):
    def update(self, player_pos):
        # dx, dy к игроку
        # Движение в сторону игрока
        
    def render(self, screen):
        # pygame.draw.polygon() ромб

class Meteorite(Enemy):
    def update(self):
        # Движение слева направо
        # Отскок от верх/низ
        
    def render(self, screen):
        # pygame.draw.polygon() многоугольник

class Bullet:
    def update(self):
        # Движение в направлении
        # Проверка выхода за экран
        
    def render(self, screen):
        # pygame.draw.circle() точка
```

### Dev C (Systems) — ~200 строк
```python
class Menu:
    def render(self, screen):
        # Текст "Start" и "Exit"
        # Рects для кликов
        
    def handle_click(self, pos):
        # Возврат "start" или "exit"

class UI:
    def render(self, screen, player, score):
        # font.render() HP, Score, Charge level
        # screen.blit() на углы экрана

class Spawner:
    def update(self, dt, current_wave):
        # Каждые wave_interval секунд
        # Возврат list новых врагов
        # Только Drone и Meteorite (!)

class Sound:
    def play(self, name):
        # mixer.Sound(...).play()

class VoidCore:
    def __init__(self, x, y):
        self.pos = (x, y)
        
    def is_collected(self, player_pos):
        # distance < collect_range
```

---

## Дополнительные рекомендации

### Синхронизация
- **Используйте гит** (даже локально в одной папке)
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  ```
- **Не трогайте чужие файлы** без согласования
- **Dev A заканчивает первым** — это фундамент

### Разработка
- **Тестируйте каждые 30 минут** — запускайте игру
- **Логируйте ошибки** — print() в стратегических местах
- **Комментируйте код** — используйте русский, чтобы было понятно свой код
- **Упрощайте математику** — Vector2 вместо сложных формул

### Git коммиты примеры
```
Dev A: "Game loop основной"
Dev A: "Добавил коллизии"
Dev B: "Player и движение"
Dev B: "Enemy классы"
Dev C: "Menu и UI"
Dev C: "Spawner система"
Объединено: "Первая рабочая версия"
```

### Константы для упрощения (config.py)
```python
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

PLAYER_SPEED = 300
PLAYER_HP = 5

DRONE_SPEED = 150
DRONE_HP = 1

METEORITE_SPEED = 100
METEORITE_HP = 5

BULLET_SPEED = 600

WAVE_INTERVAL = 5.0
```

---

## Контрольный лист

### До начала разработки
- [ ] Перемещен старый код в OLD/
- [ ] Созданы пустые файлы в src/
- [ ] Все могут запустить main.py без ошибок
- [ ] Люди прочитали этот план

### После каждой фазы
- [ ] Фаза 1: Игра запускается, не падает
- [ ] Фаза 2: Можно играть (убивать врагов, собирать cores)
- [ ] Фаза 3: Баланс ок, нет очевидных багов

### Перед сдачей
- [ ] Игра полностью рабочая
- [ ] Код читаемый (комментарии, названия)
- [ ] OLD/ папка сохранена для сравнения
- [ ] Все файлы в репозитории

---

**Начните с Фазы 0 (подготовка), потом запускайте в этом порядке:**
1. Dev A пишет основный game.py
2. Dev B пишет классы сущностей
3. Dev C пишет системы
4. Объединение и тестирование

**Удачи! 🚀**

