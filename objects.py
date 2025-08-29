import pygame
import pytmx
from settings import *

class GameObject(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        # Remove the sprites_group reference - not needed