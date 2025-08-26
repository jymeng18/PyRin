import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, object_type = None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.object_type = object_type
        self.image = None
        
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            
class Platform(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "platform")