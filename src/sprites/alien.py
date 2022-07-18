from .shot import Shot

import pygame

class Alien(pygame.sprite.Sprite):

    def __init__(self, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('src/images/alien.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (65,60))

        self.mask = pygame.mask.from_surface(self.image)


        self.ypos = ypos

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = ypos
        self.operator = '-'

        self.shot_timer = pygame.time.get_ticks()
        self.shot_delay = 1000
    
    def update(self, shot_group):
        self.rect[0] -= 2
        
        self.rect[1] = eval(f'self.rect[1] {self.operator} 2')

        if  self.rect[1] ==  self.ypos + 100:
             self.operator = '-'
        elif self.rect[1] ==  self.ypos - 100: 
            self.operator = '+'

        shot = self.create_shot()

        if shot:
            shot_group.add(shot)

    def create_shot(self):
        now = pygame.time.get_ticks()
        if now - self.shot_timer > self.shot_delay:
            self.shot_timer = now
            return Shot(self.rect[0]+15, self.rect[1], 'enemy', 5)
        return None