import pygame
from os.path import join

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, object_type = None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.object_type = object_type
        self.image = None
        self.mask = None
        
    def draw_obj(self, screen):
        if self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, (100, 100, 100), self.rect)
            
class Platform(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "platform")
        self.load_platform()
    
    def load_platform(self):
        # Get our platform sprite first
        self.image = self.get_platform(self.width, self.height)
        self.mask = pygame.mask.from_surface(self.image)
        return self.image
        
    def get_platform(self, width, height):
        path = join('2D-Platformer-Game-/assets', 'Terrain', 'Terrain.png')
        
        # Load our terrain sprite sheet
        try:
            terrain_sheet = pygame.image.load(path).convert_alpha()
            
        except pygame.error:
            print(f"Could not load terrain sheet at {path}")
            fallback = pygame.Surface((width, height))
            fallback.fill((100, 100, 100))
            return fallback
        
        # Define a surface of equal width and height of the sprite terrain
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        
        # Define the area to extract from terrain sprite sheet
        rect = pygame.Rect(96, 0, width, height)
        surface.blit(terrain_sheet, (0, 0), rect)
        return pygame.transform.scale2x(surface)