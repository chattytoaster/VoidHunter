# Developer lynx

## 1. Player Class (`src/player.py`)

The `Player` class handles movement, rotation, and input handling for the user's ship.

### How it works
- **Movement:** It uses WASD keys to modify the position. The diagonal movement is normalized so the player doesn't move faster diagonally.
- **Rotation:** The player constantly faces the mouse cursor using `math.atan2()`, which calculates the angle between the player's coordinate and the mouse coordinate.
- **Shooting:** Checks if `SPACE` or the left mouse button is pressed and returns a boolean for the main game loop to spawn a bullet.

### Why it works
Normalizing diagonal movement is crucial to maintain a consistent speed (`PLAYER_SPEED`). `math.atan2` is the standard mathematical approach in 2D games to find the correct radian angle to rotate a point towards a target. 

### Snippet
```python
# Normalize diagonal movement to maintain consistent speed
if dx != 0 or dy != 0:
    length = math.hypot(dx, dy)
    dx /= length
    dy /= length
    
self.pos[0] += dx * self.speed * dt
self.pos[1] += dy * self.speed * dt

# Rotation logic using atan2 for accurate angle to cursor
mouse_dx = mouse_pos[0] - self.pos[0]
mouse_dy = mouse_pos[1] - self.pos[1]
self.angle = math.atan2(mouse_dy, mouse_dx)
```

---

## 2. Enemy Classes (`src/enemy.py`)

This file contains the base `Enemy` class and two specialized enemy types: `Drone` and `Meteorite`.

### How it works
- **Base Enemy:** Handles generic properties like health, taking damage, and tracking if the enemy is active. If `hp <= 0`, it is marked inactive.
- **Drone:** Constantly calculates the distance to the player and moves directly towards them.
- **Meteorite:** Spawns moving from left to right. It reverses its vertical velocity when hitting the top or bottom of the screen (bouncing). It automatically deactivates if it travels completely off the right edge of the screen.

### Why it works
The `Drone` uses Euclidean distance (`math.hypot`) to find the exact vector to the player, allowing it to seamlessly track the player. The `Meteorite` is a simpler obstacle, relying on screen boundary collision checks to create a bouncing effect without needing complex physics.

### Snippet
```python
# Drone pursuit logic
if player_pos:
    dx = player_pos[0] - self.pos[0]
    dy = player_pos[1] - self.pos[1]
    dist = math.hypot(dx, dy) # Euclidean distance
    
    if dist > 0:
        # Normalize direction and multiply by speed and delta time
        self.pos[0] += (dx / dist) * self.speed * dt
        self.pos[1] += (dy / dist) * self.speed * dt

# Meteorite bounce logic
if self.pos[1] - self.radius < 0:
    self.pos[1] = self.radius
    self.vel[1] *= -1 # Reverse Y velocity
```

---

## 3. Projectile Class (`src/projectile.py`)

Handles the bullets fired by the player.

### How it works
When instantiated, the bullet is given an initial position and a normalized direction. It continuously moves in that direction during its `update()` method. It checks its coordinates against `SCREEN_WIDTH` and `SCREEN_HEIGHT` to deactivate itself when off-screen to save memory.

### Why it works
By taking a normalized direction (calculated in the main game loop based on the player's angle), the bullet only needs basic linear multiplication (`direction * speed * dt`) to travel correctly. Removing it when it goes off-screen prevents a memory leak.

### Snippet
```python
# Move in the specified direction
self.pos[0] += self.dir[0] * self.speed * dt
self.pos[1] += self.dir[1] * self.speed * dt

# Check if the bullet goes off screen bounds
if (self.pos[0] < 0 or self.pos[0] > SCREEN_WIDTH or
    self.pos[1] < 0 or self.pos[1] > SCREEN_HEIGHT):
    self.active = False
```

---

## 4. Utilities (`src/utils.py`)

Contains helper functions, specifically for collision.

### How it works
The `circle_collision` function checks if the distance between two central points is less than or equal to the sum of their radii. 

### Why it works
Instead of using `math.sqrt` to find the exact distance (which is computationally expensive), it compares the squared distance against the squared sum of the radii. This significantly optimizes collision checks, which is essential when the game loop runs 60 times a second and checks multiple bullets against multiple enemies.

### Snippet
```python
def circle_collision(pos1, radius1, pos2, radius2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    
    # Use squared distance to avoid expensive square root operations
    distance_squared = dx**2 + dy**2
    radii_sum_squared = (radius1 + radius2)**2
    
    return distance_squared <= radii_sum_squared
```
