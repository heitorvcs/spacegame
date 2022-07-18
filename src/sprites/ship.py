import pygame

class Ship(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('src/images/Ship.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (45,40))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = 400 / 2
        self.rect[1] = 800 / 2
    
    def down(self):
        self.rect[1] += 40

    def up(self):
        self.rect[1] -= 40
    
    def left(self):
        self.rect[0] -= 40
    
    def right(self):
        self.rect[0] += 40