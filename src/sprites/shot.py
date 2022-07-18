import pygame

class Shot(pygame.sprite.Sprite):

    def __init__(self, x, y, shot_type, speed = 10):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('src/images/Shot.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20,20))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = x+ 25
        self.rect[1] = y+ 10
        self.shot_type = shot_type
        self.speed = speed

    def update(self, *sprite_pos):       
        if self.shot_type == 'ship':
            self.rect[0] += self.speed

        elif self.shot_type == 'enemy':
            self.rect[0] -= self.speed
            self.enemy_aimbot(sprite_pos[0], sprite_pos[1])

    def enemy_aimbot(self, sprite_x, sprite_y):
        if self.rect[1] != sprite_y:

            
            if self.rect[1] > sprite_y:
                self.rect[1] -= self.speed 

                if (self.rect[1] < sprite_y):
                    self.rect[1] = sprite_y
            
            else:
                self.rect[1] += self.speed

                if (self.rect[1] > sprite_y):
                    self.rect[1] = sprite_y