import pygame
from settings import *
from os import listdir
from os.path import isfile, join

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
        player.stop_horizontal_movement()
        
        # Handle movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move_left(PLAYER_SPEED)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move_right(PLAYER_SPEED)
    
    # Draw backgrond img
    def draw_background(self, surface):
        surface.blit(self.background_image, (0, 0))
        
    # Flip a sprite horizontally 
    def flip_sprite_horizontal(self, sprites):
        flipped_sprites = []
        
        # Loop through each sprite frame in the spritesheet, flip them horizontally
        for sprite in sprites:
            flipped_sprites.append(pygame.transform.flip(sprite, True, False))
        return flipped_sprites
    
    # Load our sprites from spritesheet, *folders allows infinite many arbitrary arguments
    # We use *folders as we have many directories for our assets
    def load_sprite_sheets(self, *folders, width, height, need_flip = False):
        sprite_img_files = []
        
        # Build full path to assets folder
        assets_path = join('2D-Platformer-Game-/assets', *folders)
        
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
                sprite = pygame.transform.scale2x(sprite)
                sprites.append(sprite)
                
                sprite_rect_x += width
                
            sprite_rect_y += height
            sprite_rect_x = start_pos[0] # Reset starting position after each row
            
        return sprites