import pygame
from settings import *
from os import listdir
from os.path import isfile, join


class Player(pygame.sprite.Sprite):
    
    GRAVITY = 1
    
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.x_speed = 0
        self.y_speed = 0
        self.mask = None
        self.direction = LEFT  # -1 for left, 1 for right
        self.stamina = MAX_STAMINA
        self.is_tired = False 
        self.animation_count = 0
        self.gravity_count = 0
        self.jump_count = 0
        self.is_grounded = True # Player is on Ground
        
        # Animation state management
        self.animation_state = "idle" # Default is idle
        self.animation_speed = 10
    
        # Load sprites
        self.sprite_dict = self.load_player_sprites()
        self.sprite = None
        
    def load_player_sprites(self):
        return self.load_player_sprite_sheets('MainCharacters', 'Explorer', width=32, height=32, need_flip=True)
    
    # Load our sprites from spritesheet, *folders allows infinite many arbitrary arguments
    # We use *folders as we have many directories for our assets
    def load_player_sprite_sheets(self, *folders, width, height, need_flip = False):
        sprite_img_files = []
        
        # Build full path to assets folder
        assets_path = join('assets', *folders)
        
        # Loops through every file in the target folder
        for file_name in listdir(assets_path):
            full_path = join(assets_path, file_name)
            # Error check
            if(isfile(full_path)):
                sprite_img_files.append(file_name)
        
        # Use dictionary for key value pairs for each file name and sprite
        all_sprites = {}  
        
        for sprite in sprite_img_files:
            # Load our sprite sheet 
            sprite_sheet = pygame.image.load(join(assets_path, sprite)).convert_alpha()

            sprites = self.extract_sprites_from_sheet(sprite_sheet, width, height)
                
            if(need_flip):
                # Note: Not changing file name, we are just creating a key
                all_sprites[sprite.replace(".png", "") + "_right"] = sprites
                all_sprites[sprite.replace(".png", "") + "_left"] = self.flip_sprite_horizontal(sprites)
            else:
                all_sprites[sprite.replace(".png", "")] = sprites
                
        return all_sprites
    
    # Helper method to extract individual sprites frokm a spritesheet
    def extract_sprites_from_sheet(self, sprite_sheet, width, height, start_pos = (0, 0)):
        
        sprites = []
        
        # Initialize sprite sheet dimensions
        sheet_width = sprite_sheet.get_width()
        sheet_height = sprite_sheet.get_height()
        
        # Default at (0, 0)
        sprite_rect_x, sprite_rect_y = start_pos
        
        # Loop through each row, column and 'frame' each target sprite, 
        # copy it to a subsurface with exact width and height of target sprite
        
        for row in range(0,  sheet_height - height + 1, height):
            for col in range(0, sheet_width - width + 1, width):
                
                # Set clip region for target sprite
                sprite_sheet.set_clip(pygame.Rect(sprite_rect_x, sprite_rect_y, width, height))
                
                # Extract the sprite using a subsurface
                sprite = sprite_sheet.subsurface(sprite_sheet.get_clip())
                
                # Scale sprite to match current behaviour
                #sprite = pygame.transform.scale2x(sprite)
                sprites.append(sprite)
                
                sprite_rect_x += width
                
            sprite_rect_y += height
            sprite_rect_x = start_pos[0] # Reset starting position after each row
            
        return sprites
    
    # Flip a sprite horizontally 
    def flip_sprite_horizontal(self, sprites):
        
    
        flipped_sprites = []
        
        # Loop through each sprite frame in the spritesheet, flip them horizontally
        for sprite in sprites:
            flipped_sprites.append(pygame.transform.flip(sprite, True, False))
        return flipped_sprites
    
    def move(self, dx, dy):
        # Move player by x or y amount of distance 
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self, speed):
        # Set player movement to the left
        if not self.is_tired:
            self.x_speed = -speed
            if self.direction != LEFT:
                self.direction = LEFT
                self.animation_count = 0
    
    def move_right(self, speed):
        # Set player movement to right
        if not self.is_tired:
            self.x_speed = speed
            if self.direction != RIGHT:
                self.direction = RIGHT
                self.animation_count = 0
            
    def jump(self):
        if self.can_jump():
            self.y_speed = -5
            self.jump_count += 1
            self.gravity_count = 0
            self.animation_count = 0
            self.stamina -= 2
            self.is_grounded = False
    
    def can_jump(self):
        return self.is_grounded and not self.is_tired
        
    def stop_horizontal_movement(self):
        # Stop horizontal movement
        self.x_speed = 0
        
    def tired(self):
        if self.stamina <= 0:
            self.x_speed = 0
            self.is_tired = True
            
    def update_stamina(self):
        
        # Player is moving on ground
        if self.x_speed != 0 and self.is_grounded:
            self.stamina -= STAMINA_DRAIN_RATE
            if self.stamina <= 0:
                self.stamina = 0
                self.tired()
                
        # Player is standing still 
        elif self.x_speed == 0 and self.is_grounded:
            self.stamina += STAMINA_RECOVERY_RATE
            if self.stamina >= MAX_STAMINA:
                self.stamina = MAX_STAMINA
            if self.stamina >= MIN_STAMINA:
                self.is_tired = False
        
    def landed(self):
        self.y_speed = 0
        self.jump_count = 0
        self.is_grounded = True
        self.gravity_count = 0 # Reset gravity count    
    
    def hit_head(self):
        self.y_speed *= -1
        self.animation_count = 0
        
    def update_animation_state(self):
        if self.x_speed != 0:
            self.animation_state = "run"
        elif self.y_speed < 0:
            self.animation_state = "jump"
        elif self.y_speed > self.GRAVITY * 2:
            self.animation_state = "fall"
        elif self.is_tired:
            self.animation_state = "tired"
        else:
            self.animation_state = "idle"
    
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
        
    def update(self, fps):
        self.y_speed += min(1, (self.gravity_count / fps) * self.GRAVITY)
        self.move(self.x_speed, self.y_speed)
        self.update_stamina()
        self.check_died()
        
        self.update_animation_state()
        self.update_animation_sprite()
        self.update_sprite_rect()
        
        self.gravity_count += 1
        self.animation_count += 1
    
    def get_vertical_speed(self):
        return self.y_speed
    
    def get_horizontal_speed(self):
        return self.x_speed
    
    def draw(self, surface):
        if self.sprite:
            surface.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(surface, (100, 100, 100), self.rect)
   
    def check_died(self):
        if self.rect.y >= SCREEN_HEIGHT:
            self.rect.x = 0
            self.rect.y = 500