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