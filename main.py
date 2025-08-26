import pygame
import sys
from settings import *
from player import Player
from level import Level
from objects import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Rin 2D Platformer')
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Create game objects
        self.level = Level()
        self.player_sprites = self.level.load_sprite_sheets("MainCharacters", "VirtualGuy", width=32, height=32, need_flip=True)
        self.player = Player(100, 100, PLAYER_WIDTH, PLAYER_HEIGHT, self.player_sprites) # TEMPORARY

    def run(self):
        # Main game loop
        while(True):
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Update player position if input exists
            self.level.handle_input(self.player)
            self.player.update(FPS)    
            
            # Draw onto screen
            self.level.draw_background(self.screen)
            self.level.draw_platforms(self.screen)
            self.player.draw(self.screen)
            
            # Draw game objects
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()