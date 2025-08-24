import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    
    GRAVITY = 1
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_speed = 0
        self.y_speed = 0
        self.mask = None
        self.direction = LEFT  # -1 for left, 1 for right
        self.animation_count = 0
        self.color = PLAYER_COLOR
        self.gravity_count = 0
        
    
    def move(self, dx, dy):
        # Move player by x or y amount of distance 
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self, speed):
        # Set player movement to the left
        self.x_speed = -speed
        if self.direction != LEFT:
            self.direction = LEFT
            self.animation_count = 0
    
    def move_right(self, speed):
        # Set player movement to right
        self.x_speed = speed
        if self.direction != RIGHT:
            self.direction = RIGHT
            self.animation_count = 0
    
    def stop_horizontal_movement(self):
        # Stop horizontal movement
        self.x_speed = 0
    
    def update(self, fps):
        self.y_speed += min(1, (self.gravity_count / fps) * self.GRAVITY)
        self.move(self.x_speed, self.y_speed)
        self.animation_count += 1 # TEMPORARY WORK IN PROGRESS
        self.gravity_count += 1
    
    def draw(self, surface):
        # Draw player on screen for every frame
        pygame.draw.rect(surface, self.color, self.rect)
    
    def get_position(self):
        return (self.rect.x, self.rect.y)
    
    def get_rect(self):
        return self.rect