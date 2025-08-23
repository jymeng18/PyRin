import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Rinn")
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load('2D-Platformer-Game-/data/images/clouds/cloud_1.png').convert_alpha()
        self.image.set_colorkey((0, 0, 0)) # Remove black background on imgs
        self.image_position = [160, 260]
        self.movement = [0, 0]

    def run(self):
        while(True):
            self.screen.fill((14, 219, 248))
            self.image_position[1] += self.movement[1] - self.movement[0]
            self.screen.blit(self.image, self.image_position)
            
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                    
                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_UP):
                        self.movement[0] = 1
                    if(event.key == pygame.K_DOWN):
                        self.movement[1] = 1
                if(event.type == pygame.KEYUP):
                    if(event.key == pygame.K_UP):
                        self.movement[0] = 0
                    if(event.key == pygame.K_DOWN):
                        self.movement[1] = 0
                        
            pygame.display.update()
            self.clock.tick(60)
            
if(__name__ == '__main__'):
    game = Game()
    game.run()