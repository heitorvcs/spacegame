import pygame

class Asteroid(pygame.sprite.Sprite):

    def __init__(self, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('src/images/asteroid.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60,60))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = 800 - ypos

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= 10