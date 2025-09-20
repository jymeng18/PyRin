import pygame
from settings import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen

    # Draws every sprite and object onto the screen      
    def render_frame(self, level, player):
        # Clear the screen first (important!)
        self.screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw level tiles
        level.sprite_group.draw(self.screen)
        
        # Draw player
        player.draw(self.screen)
    
    def draw_collision_debug(self, level):
        """Draw collision objects for debugging purposes"""
        for obj in level.get_collision_objects():
            if hasattr(obj, 'collides_with_rect'):  # Polygon collision object
                # Draw triangle outline
                points = [
                    (obj.points[0][0] + obj.x, obj.points[0][1] + obj.y),
                    (obj.points[1][0] + obj.x, obj.points[1][1] + obj.y),
                    (obj.points[2][0] + obj.x, obj.points[2][1] + obj.y)
                ]
                pygame.draw.polygon(self.screen, (255, 0, 0), points, 2)
            else:  # Regular rectangular collision object
                pygame.draw.rect(self.screen, (255, 0, 0), obj.rect, 2)