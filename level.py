import pygame
import pytmx
from settings import *
from objects import *
from os.path import join

class Level:
    def __init__(self):
        self.tmx_data = None
        self.sprite_group = pygame.sprite.Group()
        self.collision_objects = []  # Store collision objects
        self.load_tmx_map()
        self.create_level()
   
    def create_level(self):
        self.load_tiles()
        self.load_collision_objects()
   
    def load_tmx_map(self):
        self.tmx_data = pytmx.load_pygame(join('assets', 'Map', 'map2.tmx'))
        return self.tmx_data
   
    def load_tiles(self):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    position = (x * TILE_SIZE, y * TILE_SIZE)
                    tile = GameObject(pos=position, surf=surf, groups=self.sprite_group)
                    # Don't draw here - let the renderer handle drawing
    
    def load_collision_objects(self):
        for obj in self.tmx_data.objects:
            if hasattr(obj, 'type'):
     
                # Create a simple surface for collision object
                surf = pygame.Surface((obj.width, obj.height))
                collision_obj = GameObject(pos=(obj.x, obj.y), surf=surf, groups=[])
                self.collision_objects.append(collision_obj)
                
    def get_collision_objects(self):
        return self.collision_objects

    def print_data(self):
        print(self.tmx_data.layernames)