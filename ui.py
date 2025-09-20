import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), hover_color=(150, 150, 150), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, screen, font):
        # Draw button background with gradient effect
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw button border with different colors for hover
        border_color = (255, 255, 255) if self.is_hovered else (200, 200, 200)
        pygame.draw.rect(screen, border_color, self.rect, 3)
        
        # Draw inner shadow for depth
        inner_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4)
        pygame.draw.rect(screen, (0, 0, 0, 50), inner_rect, 1)
        
        # Draw button text
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 84)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Create buttons with better styling
        button_width = 250
        button_height = 70
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        center_y = SCREEN_HEIGHT // 2 + 20
        
        self.play_button = Button(center_x, center_y, button_width, button_height, "START GAME", 
                                 color=(50, 150, 50), hover_color=(70, 170, 70), text_color=(255, 255, 255))
        
    def handle_events(self, events):
        for event in events:
            if self.play_button.handle_event(event):
                return GAME_STATE_PLAYING
        return GAME_STATE_MENU
    
    def draw(self):
        # Clear screen with green gradient background
        self.screen.fill((30, 80, 30))  # Dark green base
        
        # Draw decorative elements
        pygame.draw.rect(self.screen, (50, 120, 50), (0, 0, SCREEN_WIDTH, 100))
        pygame.draw.rect(self.screen, (40, 100, 40), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        # Draw title with shadow effect
        title_text = self.font_large.render("RIN 2D PLATFORMER", True, (0, 0, 0))
        title_shadow = self.font_large.render("RIN 2D PLATFORMER", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 120))
        title_shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(title_text, title_rect)
        self.screen.blit(title_shadow, title_shadow_rect)
        
        # Draw subtitle
        subtitle_text = self.font_medium.render("Adventure Awaits!", True, (255, 255, 200))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw controls with better formatting
        controls_lines = [
            "Use WASD or Arrow Keys to move",
            "Press SPACE to jump",
            "Don't fall off the map!"
        ]
        
        for i, line in enumerate(controls_lines):
            controls_text = self.font_small.render(line, True, (200, 255, 200))
            controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100 + i * 35))
            self.screen.blit(controls_text, controls_rect)
        
        # Draw play button
        self.play_button.draw(self.screen, self.font_medium)

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 84)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Create buttons with better styling
        button_width = 200
        button_height = 60
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        restart_y = SCREEN_HEIGHT // 2 + 30
        quit_y = SCREEN_HEIGHT // 2 + 110
        
        self.restart_button = Button(center_x, restart_y, button_width, button_height, "TRY AGAIN", 
                                    color=(50, 150, 50), hover_color=(70, 170, 70), text_color=(255, 255, 255))
        self.quit_button = Button(center_x, quit_y, button_width, button_height, "QUIT", 
                                 color=(150, 50, 50), hover_color=(170, 70, 70), text_color=(255, 255, 255))
        
    def handle_events(self, events):
        for event in events:
            if self.restart_button.handle_event(event):
                return GAME_STATE_PLAYING
            elif self.quit_button.handle_event(event):
                return "quit"
        return GAME_STATE_GAME_OVER
    
    def draw(self):
        # Clear screen with red gradient background
        self.screen.fill((60, 20, 20))  # Dark red base
        
        # Draw decorative elements
        pygame.draw.rect(self.screen, (80, 30, 30), (0, 0, SCREEN_WIDTH, 100))
        pygame.draw.rect(self.screen, (70, 25, 25), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        # Draw game over text with shadow effect
        game_over_text = self.font_large.render("GAME OVER", True, (0, 0, 0))
        game_over_shadow = self.font_large.render("GAME OVER", True, (255, 100, 100))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 100))
        game_over_shadow_rect = game_over_shadow.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(game_over_shadow, game_over_shadow_rect)
        
        # Draw restart message
        restart_text = self.font_medium.render("Better luck next time!", True, (255, 200, 200))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(restart_text, restart_rect)
        
        # Draw buttons
        self.restart_button.draw(self.screen, self.font_medium)
        self.quit_button.draw(self.screen, self.font_medium)
