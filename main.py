import pygame
import sys
from settings import *
from player import Player
from level import Level
from objects import *
from renderer import Renderer
from collision import Collision

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
        self.player = Player(SCREEN_WIDTH // 2, PLAYER_SPAWN - 100)
        self.collision = Collision() 

    # Handle user input
    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.player.jump()
        
        keys = pygame.key.get_pressed()
        
        # Reset horizontal movement for each frame
        self.player.stop_horizontal_movement()
        
        # Handle movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left(PLAYER_SPEED)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right(PLAYER_SPEED)
            
    # Handle collision dddd
    def handle_collision(self):
        self.collision.check_all_collisions(self.player, self.level)
    
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
            events = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    self.running = False
                events.append(event)
            self.handle_input(events)
            self.draw()
            self.update()
            self.handle_collision()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()