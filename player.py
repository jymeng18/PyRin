import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    
    GRAVITY = 1
    
    def __init__(self, x, y, width, height, sprites):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_speed = 0
        self.y_speed = 0
        self.mask = None
        self.direction = LEFT  # -1 for left, 1 for right
        self.animation_count = 0
        self.color = PLAYER_COLOR
        self.gravity_count = 0
        self.sprite_dict = sprites 
        self.sprite = None
        
        # Animation state management
        self.animation_state = "idle" # Default is idle
        self.animation_speed = 8
    
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
        
    def update_animation_state(self):
        if self.x_speed != 0:
            self.animation_state = "run"
        elif self.y_speed < 0:
            self.animation_state = "jump"
        elif self.y_speed > 0:
            self.animation_state = "fall"
        else:
            self.animation_state = "idle"
    
    def update(self, fps):
        self.y_speed += min(1, (self.gravity_count / fps) * self.GRAVITY)
        self.move(self.x_speed, self.y_speed)
        
        self.update_animation_state()
        
        self.animation_count += 1 # TEMPORARY WORK IN PROGRESS
        #self.gravity_count += 1
    
    def update_animation_sprite(self):
        if self.direction == LEFT:
            direction_suffix = "_left"
        else:
            direction_suffix = "_right"
        
        # Form the sprites key in the dict.
        sprite_key = self.animation_state + direction_suffix
        
        # Check if there exists matching key value pairs, and that the sprite animations exist
        if sprite_key in self.sprite_dict and len(self.sprite_dict[sprite_key]) > 0:
            sprite_list = self.sprite_dict[sprite_key]
             
            # Calculate current frame for animation
            frame_index = ((self.animation_count // self.animation_speed) % len(sprite_list))
             
            # For each frame, pick out our sprite
            self.sprite = sprite_list[frame_index]
            self.animation_count += 1
            
    def update_sprite_rect(self):
        # Update player's sprite rect
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    
    def draw(self, surface):
        self.update_animation_sprite()
        self.update_sprite_rect()
        surface.blit(self.sprite, (self.rect.x, self.rect.y))
        
                
        
    
    def get_position(self):
        return (self.rect.x, self.rect.y)
    
    def get_rect(self):
        return self.rect