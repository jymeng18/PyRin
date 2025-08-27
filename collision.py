import pygame
from settings import *

class Collision:
    def __init__(self):
        pass
    
    def check_all_collisions(self, player, level):
        dy = player.get_vertical_speed()
        objects = level.get_platforms()
        self.check_collision_vertical(player, objects, dy)
        
    def check_collision_vertical(self, player, objects, dy):
        collided_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(player, obj):
                if dy > 0:
                    player.rect.bottom = obj.rect.top
                    player.landed()
                elif dy < 0:
                    player.rect.top = obj.rect.bottom
                    player.hit_head()
                    
                collided_objects.append(obj)
        return collided_objects