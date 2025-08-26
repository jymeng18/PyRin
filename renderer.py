import pygame
from settings import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.background_images = self.load_backgrounds()
        
    def load_backgrounds(self):
    # Load background img
        backgrounds = []
        for bg_path in BACKGROUND_PATH:
            try:
                bg_img = pygame.image.load(bg_path).convert_alpha()
                bg_img = pygame.transform.smoothscale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                backgrounds.append(bg_img)
                
            except pygame.error:
                # Create fallback background if image fails to load
                fallback = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fallback.fill((135, 206, 235))  # Sky blue
                backgrounds.append(fallback)
        return backgrounds
    
    def draw_backgrounds(self):
        for bg in self.background_images:
            self.screen.blit(bg, (0, 0))
    
    # Draws every sprite and object onto the screen       
    def render_frame(self, level, player):
        # Clear screen first
        self.screen.fill((0, 0, 0))
        
        self.draw_backgrounds()
        level.draw_platforms(self.screen)
        player.draw(self.screen)