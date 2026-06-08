import pygame
import math
from config import (
    COLOR_DRONE, COLOR_METEORITE, 
    DRONE_SPEED, DRONE_SIZE, DRONE_HP,
    METEORITE_SPEED, METEORITE_SIZE, METEORITE_HP,
    SCREEN_WIDTH, SCREEN_HEIGHT
)

class Enemy:
    def __init__(self, x, y):
        """
        Base Enemy class.
        
        Args:
            x (float): Initial x coordinate
            y (float): Initial y coordinate
        """
        self.pos = [x, y]
        self.hp = 1
        self.radius = 10
        self.active = True

    def take_damage(self, amount):
        """
        Reduce HP and mark as inactive if HP <= 0.
        
        Args:
            amount (int): Amount of damage to take
        """
        self.hp -= amount
        if self.hp <= 0:
            self.active = False

    def update(self, dt, player_pos=None):
        """
        Update logic to be overridden by subclasses.
        """
        pass

    def render(self, screen):
        """
        Render logic to be overridden by subclasses.
        """
        pass


class Drone(Enemy):
    def __init__(self, x, y):
        """
        Drone enemy that chases the player.
        """
        super().__init__(x, y)
        self.hp = DRONE_HP
        self.radius = DRONE_SIZE
        self.speed = DRONE_SPEED

    def update(self, dt, player_pos=None):
        """
        Update the drone to move towards the player.
        
        Args:
            dt (float): Delta time in seconds
            player_pos (tuple): (x, y) coordinates of the player
        """
        if player_pos:
            dx = player_pos[0] - self.pos[0]
            dy = player_pos[1] - self.pos[1]
            dist = math.hypot(dx, dy)
            
            if dist > 0:
                # Normalize direction and move
                self.pos[0] += (dx / dist) * self.speed * dt
                self.pos[1] += (dy / dist) * self.speed * dt

    def render(self, screen):
        """
        Render the drone as a rhombus.
        """
        x, y = int(self.pos[0]), int(self.pos[1])
        r = self.radius
        
        # Rhombus points (top, right, bottom, left)
        points = [
            (x, y - r),
            (x + r, y),
            (x, y + r),
            (x - r, y)
        ]
        pygame.draw.polygon(screen, COLOR_DRONE, points)


class Meteorite(Enemy):
    def __init__(self, x, y):
        """
        Meteorite enemy that moves from left to right and bounces off top/bottom.
        """
        super().__init__(x, y)
        self.hp = METEORITE_HP
        self.radius = METEORITE_SIZE
        self.speed = METEORITE_SPEED
        # Default movement direction: right, with a slight vertical movement
        self.vel = [self.speed, self.speed * 0.5]

    def update(self, dt, player_pos=None):
        """
        Update the meteorite movement and handle bouncing.
        
        Args:
            dt (float): Delta time in seconds
            player_pos (tuple): Ignored for Meteorite, kept for signature compatibility
        """
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        
        # Bounce off top and bottom screen edges
        if self.pos[1] - self.radius < 0:
            self.pos[1] = self.radius
            self.vel[1] *= -1
        elif self.pos[1] + self.radius > SCREEN_HEIGHT:
            self.pos[1] = SCREEN_HEIGHT - self.radius
            self.vel[1] *= -1
            
        # Deactivate if it goes too far off the right edge
        if self.pos[0] > SCREEN_WIDTH + self.radius * 2:
            self.active = False

    def render(self, screen):
        """
        Render the meteorite as a simple polygon (hexagon or square for simplicity).
        We'll use a slightly irregular octagon for a 'rocky' look.
        """
        x, y = int(self.pos[0]), int(self.pos[1])
        r = self.radius
        
        # Simple rocky shape points
        points = [
            (x - r*0.5, y - r),
            (x + r*0.5, y - r),
            (x + r, y - r*0.5),
            (x + r, y + r*0.5),
            (x + r*0.5, y + r),
            (x - r*0.5, y + r),
            (x - r, y + r*0.5),
            (x - r, y - r*0.5)
        ]
        pygame.draw.polygon(screen, COLOR_METEORITE, points)
