import pygame
from settings import *

class Collision:
    def __init__(self):
        pass
    
    def check_horizontal_collision(self, player, collision_objects, dx):
        for obj in collision_objects:
            if player.rect.colliderect(obj.rect):
                if dx > 0:  # Moving right
                    player.rect.right = obj.rect.left
                    print("Moving!")
                elif dx < 0:  # Moving left
                    player.rect.left = obj.rect.right
                player.stop_horizontal_movement()
    
    def check_vertical_collision(self, player, collision_objects, dy):
        for obj in collision_objects:
            if player.rect.colliderect(obj.rect):
                if dy > 0:  # Falling down
                    print("1000")
                    player.rect.bottom = obj.rect.top
                    player.landed()
                elif dy < 0:  # Moving up (jumping)
                    player.rect.top = obj.rect.bottom
                    player.hit_head()
    
    def check_all_collisions(self, player, level):
        
        collision_objs = level.get_collision_objects()
        dy = player.get_vertical_speed()
        dx = player.get_horizontal_speed()
        
        #self.check_horizontal_collision(player, collision_objs, dx)
        self.check_vertical_collision(player, collision_objs, dy)