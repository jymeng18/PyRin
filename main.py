import pygame
from pygame.locals import *
import sys

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Rins Platformer')
clock = pygame.time.Clock()

# Background image
bg_img = pygame.image.load('2D-Platformer-Game-/graphics/Background/Background.png').convert_alpha()
bg_img = pygame.transform.smoothscale(bg_img, (screen_width, screen_height))

# Level system
TILE_SIZE = 80

# Level 1 - Small tutorial level
level_1_data = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

# Level data storage
levels = {
    1: level_1_data
}

class World:
    def __init__(self, level_data):
        self.level_data = level_data
        self.tile_list = []
        self.load_level()
    
    
    # Loops through the data of each map level and creates a rectangle 
    # scaled to TILE_SIZE at each position where value is 1
    def load_level(self):
        self.tile_list = []
        row_count = 0
        for row in self.level_data:
            col_count = 0
            for tile in row:
                if(tile == 1):
                    # Create a tile for each '1'
                    img_rect = pygame.Rect(col_count * TILE_SIZE, row_count * TILE_SIZE, TILE_SIZE, TILE_SIZE)   
                    tile_data = (img_rect.x, img_rect.y)
                    self.tile_list.append(tile_data)
                col_count += 1
            row_count += 1
    
    #   
    def draw(self, screen):
        for tile in self.tile_list:
            tile_rect = pygame.Rect(tile[0], tile[1], TILE_SIZE, TILE_SIZE)
            
            # TEMPORARY 
            pygame.draw.rect(screen, (139, 69, 19), tile_rect)
            pygame.draw.rect(screen, (101, 67, 33), tile_rect, 2)

# Game state
current_lvl = 1
world = World(levels[current_lvl])

while True:
    
    screen.blit(bg_img, (0, 0))
    world.draw(screen)

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
    
    clock.tick(60)        
    pygame.display.update()
