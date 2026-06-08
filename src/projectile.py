import pygame
import math
from config import BULLET_SPEED, BULLET_SIZE, COLOR_BULLET, SCREEN_WIDTH, SCREEN_HEIGHT

class Bullet:
    def __init__(self, x, y, direction_x, direction_y):
        """
        Initialize the bullet.
        
        Args:
            x (float): Initial x coordinate
            y (float): Initial y coordinate
            direction_x (float): Normalized direction x component
            direction_y (float): Normalized direction y component
        """
        self.pos = [x, y]
        self.dir = [direction_x, direction_y]
        self.speed = BULLET_SPEED
        self.radius = BULLET_SIZE
        self.active = True

    def update(self, dt):
        """
        Update the bullet position.
        
        Args:
            dt (float): Delta time in seconds
        """
        # Move in the specified direction
        self.pos[0] += self.dir[0] * self.speed * dt
        self.pos[1] += self.dir[1] * self.speed * dt
        
        # Check if the bullet goes off screen
        if (self.pos[0] < 0 or self.pos[0] > SCREEN_WIDTH or
            self.pos[1] < 0 or self.pos[1] > SCREEN_HEIGHT):
            self.active = False

    def render(self, screen):
        """
        Render the bullet as a simple circle.
        
        Args:
            screen (pygame.Surface): The game screen surface
        """
        pygame.draw.circle(
            screen, 
            COLOR_BULLET, 
            (int(self.pos[0]), int(self.pos[1])), 
            self.radius
        )
