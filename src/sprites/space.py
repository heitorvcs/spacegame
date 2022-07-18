import pygame

class Space(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('src/images/newbackground.jpg').convert_alpha()
        self.image = pygame.transform.scale(self.image, (800, 800))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = 0
    
    def update(self):
        self.rect[0] -= 10
