import pygame
import sys
from settings import *
from player import Player
from level import Level
from objects import *
from renderer import Renderer
from collision import Collision
from ui import StartScreen, GameOverScreen

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Rin 2D Platformer')
       
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.game_state = GAME_STATE_MENU
       
        # Create game objects
        self.renderer = Renderer(self.screen)
        self.level = Level()
        self.player = Player(0, 500)
        self.collision = Collision()
        
        # Create UI screens
        self.start_screen = StartScreen(self.screen)
        self.game_over_screen = GameOverScreen(self.screen)

    def reset_game(self):
        """Reset the game to initial state"""
        self.player = Player(0, 500)
        self.game_state = GAME_STATE_PLAYING
    
    def check_game_over(self):
        """Check if player has died or fallen off the map"""
        if self.player.rect.y >= SCREEN_HEIGHT:
            self.game_state = GAME_STATE_GAME_OVER
            return True
        return False

    # Handle user input
    def handle_input(self, events):
        if self.game_state == GAME_STATE_PLAYING:
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
           
    # Handle collision
    def handle_collision(self):
        self.collision.check_all_collisions(self.player, self.level)
        # Apply movement after collision detection
        self.player.apply_movement()
   
    # Updates player animations and movements
    def update(self):
        if self.game_state == GAME_STATE_PLAYING:
            self.player.update(FPS)
            self.check_game_over()
   
    # Handles all sprites and objects being drawn on the screen
    def draw(self):
        if self.game_state == GAME_STATE_PLAYING:
            self.renderer.render_frame(self.level, self.player)
        elif self.game_state == GAME_STATE_MENU:
            self.start_screen.draw()
        elif self.game_state == GAME_STATE_GAME_OVER:
            self.game_over_screen.draw()
   
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
            
            # Handle UI events for different screens
            if self.game_state == GAME_STATE_MENU:
                new_state = self.start_screen.handle_events(events)
                if new_state == GAME_STATE_PLAYING:
                    self.reset_game()
            elif self.game_state == GAME_STATE_GAME_OVER:
                new_state = self.game_over_screen.handle_events(events)
                if new_state == GAME_STATE_PLAYING:
                    self.reset_game()
                elif new_state == "quit":
                    self.running = False
            
            # Handle game input and updates
            self.handle_input(events)
            self.update()
            
            # Only handle collision and movement when playing
            if self.game_state == GAME_STATE_PLAYING:
                self.handle_collision()
            
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()