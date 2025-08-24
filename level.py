import pygame
from settings import *

class Level:
    def __init__(self):
        self.background_image = None
        self.load_background()
    
    def load_background(self):
        # Load background img
        try:
            self.background_image = pygame.image.load(BACKGROUND_PATH).convert_alpha()
            self.background_image = pygame.transform.smoothscale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            # Create fallback background if image fails to load
            self.background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background_image.fill((135, 206, 235))  # Sky blue
            
    # Handle game input
    def handle_input(self, player):
        keys = pygame.key.get_pressed()
        
        # Reset horizontal movement for each frame
        player.xspeed = player.stop_horizontal_movement()
        
        # Handle movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move_left(PLAYER_SPEED)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move_right(PLAYER_SPEED)
    
    def draw_background(self, surface):
        surface.blit(self.background_image, (0, 0))