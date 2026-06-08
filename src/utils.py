import math

def circle_collision(pos1, radius1, pos2, radius2):
    """
    Check if two circles collide.
    
    Args:
        pos1 (tuple): (x, y) coordinates of the first circle's center
        radius1 (float): Radius of the first circle
        pos2 (tuple): (x, y) coordinates of the second circle's center
        radius2 (float): Radius of the second circle
        
    Returns:
        bool: True if circles collide, False otherwise
    """
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    distance_squared = dx**2 + dy**2
    radii_sum_squared = (radius1 + radius2)**2
    
    return distance_squared <= radii_sum_squared
