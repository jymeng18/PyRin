import pygame
from settings import *
from objects import *

class Level:
    def __init__(self):
        self.platforms = []
        self.create_level()
    
    def create_level(self):
        # Create level geometry and format
        self.create_platforms_floor()
        self.fill_ground(GROUND_LEVEL, 64, 64, 'Terrain_dirt')            
            
    # Create platforms by calling platform class methods
    def create_platforms_floor(self):
        for i in range(0, SCREEN_WIDTH // PLATFORM_WIDTH + 1):
            
            # 48, 64 represent the width and height of the sprite on the spritesheet
            platform = Platform(i * PLATFORM_WIDTH, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT, 'Terrain2')
            self.platforms.append(platform)
            
    def fill_ground(self, ground_level, tile_width, tile_height, ground_tile=None):
    
        # Calculate how many tiles we need horizontally and vertically
        tiles_horizontal = (SCREEN_WIDTH // tile_width) + 1  # +1 to ensure full coverage
        tiles_vertical = ((SCREEN_HEIGHT - ground_level) // tile_height) + 1
        
        # Create ground tiles
        for row in range(tiles_vertical):
            for col in range(tiles_horizontal):
                # Calculate tile position
                x = col * tile_width
                y = ground_level + (row * tile_height)
                
                # Only create tile if it's within screen bounds
                if y < SCREEN_HEIGHT:
                    # Create a ground tile (you could make a GroundTile class or reuse Platform)
                    ground_tile_obj = Platform(x, y, tile_width, tile_height, ground_tile)
                    self.platforms.append(ground_tile_obj)
            
    def draw_platforms(self, surface):
        for platform in self.platforms:
            platform.draw_obj(surface)
            
    def update(self):
        pass

    
