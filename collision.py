import pygame
from settings import *

class Collision:
    def __init__(self):
        pass
    
    def check_horizontal_collision(self, player, collision_objects, dx):
        if dx == 0:
            return
            
        # Create a test rect for the horizontal movement
        test_rect = player.rect.copy()
        test_rect.x += dx
        
        # Check collision with all objects
        for obj in collision_objects:
            collision_detected = False
            
            # Handle polygon collision objects (triangles)
            if hasattr(obj, 'collides_with_rect'):
                collision_detected = obj.collides_with_rect(test_rect)
            else:
                # Handle regular rectangular collision objects
                collision_detected = test_rect.colliderect(obj.rect)
            
            if collision_detected:
                if dx > 0:  # Moving right
                    player.rect.right = obj.rect.left
                elif dx < 0:  # Moving left
                    player.rect.left = obj.rect.right
                player.stop_horizontal_movement()
                break  # Stop checking after first collision
    
    def check_vertical_collision(self, player, collision_objects, dy):
        if dy == 0:
            return
            
        # Create a test rect for the vertical movement
        test_rect = player.rect.copy()
        test_rect.y += dy
        
        # Check collision with all objects
        for obj in collision_objects:
            collision_detected = False
            
            # Handle polygon collision objects (triangles)
            if hasattr(obj, 'collides_with_rect'):
                collision_detected = obj.collides_with_rect(test_rect)
            else:
                # Handle regular rectangular collision objects
                collision_detected = test_rect.colliderect(obj.rect)
            
            if collision_detected:
                if dy > 0:  # Falling down
                    player.rect.bottom = obj.rect.top
                    player.landed()
                elif dy < 0:  # Moving up (jumping)
                    player.rect.top = obj.rect.bottom
                    player.hit_head()
                break  # Stop checking after first collision
    
    def check_all_collisions(self, player, level):
        collision_objs = level.get_collision_objects()
        dy = player.get_vertical_speed()
        dx = player.get_horizontal_speed()
        
        # Check both horizontal and vertical collisions
        self.check_horizontal_collision(player, collision_objs, dx)
        self.check_vertical_collision(player, collision_objs, dy)