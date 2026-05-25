import math
import random
import pygame


class Star:
    def __init__(self, width, height):
        self.reset(width, height)

    def reset(self, width, height):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.base_speed = random.uniform(20, 90)
        self.size = random.randint(1, 2)
        self.brightness = random.randint(120, 255)

    def update(self, dt, width, height, charge_level):
        speed = self.base_speed + charge_level * 120
        self.x -= speed * dt
        if self.x < -20:
            self.x = width + random.uniform(0, 40)
            self.y = random.uniform(0, height)

    def render(self, surface, charge_level):
        streak = int(charge_level * 6)
        color = (self.brightness, self.brightness, self.brightness)
        if streak > 0:
            start = (int(self.x), int(self.y))
            end = (int(self.x + streak), int(self.y))
            pygame.draw.line(surface, color, start, end, self.size)
        else:
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)


class Planet:
    COLORS = [
        ((38, 48, 68), (24, 30, 44)),
        ((52, 42, 34), (30, 24, 20)),
        ((34, 50, 42), (22, 30, 26)),
        ((44, 38, 58), (28, 24, 36)),
    ]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._spawn(start_anywhere=True)

    def _spawn(self, start_anywhere=False):
        self.x = random.uniform(0, self.width) if start_anywhere else self.width + random.uniform(80, 220)
        self.y = random.uniform(self.height * 0.1, self.height * 0.55)
        self.radius = random.randint(35, 75)
        self.speed = random.uniform(10, 30)
        self.color_a, self.color_b = random.choice(self.COLORS)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self._spawn(start_anywhere=True)

    def update(self, dt, charge_level):
        self.x -= (self.speed + charge_level * 10) * dt
        if self.x < -self.radius * 3:
            self._spawn(start_anywhere=False)

    def render(self, surface):
        r = self.radius
        glow = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        for i in range(3, 0, -1):
            alpha = 8 * i
            pygame.draw.circle(glow, (*self.color_a, alpha), (r * 2, r * 2), r + i * 12)
        pygame.draw.circle(glow, self.color_a, (r * 2, r * 2), r)
        pygame.draw.circle(glow, self.color_b, (r * 2 - r // 4, r * 2 - r // 4), int(r * 0.45))
        surface.blit(glow, (self.x - r * 2, self.y - r * 2))


class SpaceBackground:
    def __init__(self, width, height, stars_count=90):
        self.width = width
        self.height = height
        self.stars = [Star(width, height) for _ in range(stars_count)]
        self.planet = Planet(width, height)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.planet.resize(width, height)
        for star in self.stars:
            star.reset(width, height)

    def update(self, dt, charge_level):
        self.planet.update(dt, charge_level)
        for star in self.stars:
            star.update(dt, self.width, self.height, charge_level)

    def render(self, surface):
        self.planet.render(surface)

    def render_stars(self, surface, charge_level):
        for star in self.stars:
            star.render(surface, charge_level)
