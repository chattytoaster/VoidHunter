import random
import math


class Camera:
    """Класс камеры для эффекта тряски экрана"""
    
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        
    def update(self, dt, charge_level):
        """Обновление камеры"""
        # Интенсивность зависит от уровня заряда (увеличена в 4 раза)
        shake_intensity = 0.5 + (charge_level * 1.5)  # 2.0, 4.0, 6.0, 8.0, 10.0
        angle = random.uniform(0, 2 * math.pi)
        self.offset_x = math.cos(angle) * shake_intensity
        self.offset_y = math.sin(angle) * shake_intensity

    
    def get_offset(self):
        """Получить текущее смещение"""
        return (int(self.offset_x), int(self.offset_y))
