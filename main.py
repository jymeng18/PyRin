import pygame
import sys
from settings import *
from player import Player
from level import Level
from objects import *
from renderer import Renderer

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Rin 2D Platformer')
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create game objects
        self.renderer = Renderer(self.screen)
        self.level = Level()
        self.player = Player(SCREEN_WIDTH // 2, PLAYER_SPAWN) 

    # Handle user input
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Reset horizontal movement for each frame
        self.player.stop_horizontal_movement()
        
        # Handle movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left(PLAYER_SPEED)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right(PLAYER_SPEED)
    
    # Updates player animations and movements
    def update(self):
        self.player.update(FPS)
        self.level.update() # WORK IN PROGRESS NOT BEING USED RIGHT NOW
    
    # Handles all sprites and objects being drawn on the screen
    def draw(self):
        self.renderer.render_frame(self.level, self.player)
    
    # Main game event loop
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    self.running = False

            self.handle_input()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()