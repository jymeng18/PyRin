import pygame
from os.path import join

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, object_type=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.object_type = object_type
        self.image = None
        self.mask = None
    
    def load_image_from_path(self, file_path, scale=True):
        try:
            # Load the image
            image = pygame.image.load(file_path).convert_alpha()
            
            # Scale to match object dimensions
            if scale:
                image = pygame.transform.smoothscale(image, (self.width * 3, self.height * 3))
            
            return image
            
        except pygame.error:
            print(f"Could not load image at {file_path}")
            # Return fallback colored rectangle
            fallback = pygame.Surface((self.width, self.height))
            fallback.fill((100, 100, 100))  # Gray
            return fallback
    
    def draw_obj(self, screen):
        if self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, (100, 100, 100), self.rect)


class Platform(GameObject):
    def __init__(self, x, y, width, height, platform_type=None):
        super().__init__(x, y, width, height, "platform")
        self.platform_type = platform_type
        self.load_platform()
    
    def load_platform(self):
    
        # Build path to platform image
        file_path = join('2D-Platformer-Game-/assets', 'Terrain', f'{self.platform_type}.png')
        
        # Load the image using the generic method
        self.image = self.load_image_from_path(file_path, scale=True)
        
        # Create mask for collision detection
        if self.image:
            self.mask = pygame.mask.from_surface(self.image)
        
        return self.image