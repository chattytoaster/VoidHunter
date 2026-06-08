import pygame
import math
from config import (
    COLOR_PLAYER, PLAYER_SPEED, PLAYER_HP, PLAYER_SIZE,
    SCREEN_WIDTH, SCREEN_HEIGHT
)

class Player:
    def __init__(self, x, y):
        """
        Initialize the player.
        
        Args:
            x (float): Initial x coordinate
            y (float): Initial y coordinate
        """
        self.pos = [x, y]
        self.hp = PLAYER_HP
        self.radius = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.charge_level = 0
        self.angle = 0.0  # Angle in radians, pointing towards mouse

    def update(self, keys, mouse_pos, dt):
        """
        Update player position based on keys, rotation based on mouse,
        and handle shooting logic.
        
        Args:
            keys (sequence): State of all keyboard buttons from pygame.key.get_pressed()
            mouse_pos (tuple): (x, y) coordinates of the mouse
            dt (float): Delta time in seconds
            
        Returns:
            bool: True if player wants to shoot, False otherwise
        """
        # --- Movement logic (WASD) ---
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
            
        # Normalize diagonal movement
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length
            
        self.pos[0] += dx * self.speed * dt
        self.pos[1] += dy * self.speed * dt
        
        # Constrain to screen bounds
        self.pos[0] = max(self.radius, min(SCREEN_WIDTH - self.radius, self.pos[0]))
        self.pos[1] = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.pos[1]))
        
        # --- Rotation logic ---
        mouse_dx = mouse_pos[0] - self.pos[0]
        mouse_dy = mouse_pos[1] - self.pos[1]
        self.angle = math.atan2(mouse_dy, mouse_dx)
        
        # --- Shooting logic ---
        # Returns True if SPACE is pressed or Left Mouse Button is clicked
        mouse_buttons = pygame.mouse.get_pressed()
        is_shooting = keys[pygame.K_SPACE] or mouse_buttons[0]
        
        return is_shooting

    def take_damage(self, amount):
        """
        Reduce player HP.
        
        Args:
            amount (int): Amount of damage to take
        """
        self.hp -= amount
        
    def add_charge(self, amount=1):
        """
        Increase player charge level.
        
        Args:
            amount (int): Amount of charge to add
        """
        self.charge_level += amount

    def render(self, screen):
        """
        Render the player as a triangle pointing towards the mouse.
        
        Args:
            screen (pygame.Surface): The game screen surface
        """
        x, y = self.pos[0], self.pos[1]
        
        # Calculate triangle vertices based on angle
        # Nose of the ship
        p1_x = x + math.cos(self.angle) * self.radius * 1.5
        p1_y = y + math.sin(self.angle) * self.radius * 1.5
        
        # Bottom left
        p2_x = x + math.cos(self.angle + 2.5) * self.radius
        p2_y = y + math.sin(self.angle + 2.5) * self.radius
        
        # Bottom right
        p3_x = x + math.cos(self.angle - 2.5) * self.radius
        p3_y = y + math.sin(self.angle - 2.5) * self.radius
        
        points = [(p1_x, p1_y), (p2_x, p2_y), (p3_x, p3_y)]
        
        pygame.draw.polygon(screen, COLOR_PLAYER, points)